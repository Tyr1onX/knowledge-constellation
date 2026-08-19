#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "harness" / "goal_pipeline.py"


def run_json(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        payload = json.loads(proc.stdout)
    except Exception:
        payload = {"status": "tool_error", "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    return proc, payload


def runner_command(template, packet):
    ws = Path(packet["workspace"])
    mapping = {
        "{workspace}": str(ws),
        "{task}": str(ws / "TASK.md"),
        "{output}": str(ws / "output.json"),
        "{stage}": packet["stage"],
    }
    parts = shlex.split(template)
    rendered = []
    for part in parts:
        for key, value in mapping.items():
            part = part.replace(key, value)
        rendered.append(part)
    return rendered


def execute_runner(template, packet):
    ws = Path(packet["workspace"])
    env = os.environ.copy()
    env.update({
        "KC_WORKSPACE": str(ws),
        "KC_TASK": str(ws / "TASK.md"),
        "KC_OUTPUT": str(ws / "output.json"),
        "KC_STAGE": packet["stage"],
        "KC_MODE": packet["mode"],
    })
    proc = subprocess.run(runner_command(template, packet), cwd=ws, env=env)
    output = ws / "output.json"
    if proc.returncode != 0:
        raise RuntimeError(f"goal semantic runner failed for {packet['stage']} with exit code {proc.returncode}")
    if not output.exists():
        raise RuntimeError(f"goal semantic runner did not write {output}")


def load_state(run_dir: Path):
    return json.loads((run_dir / "state.json").read_text(encoding="utf-8"))


def ensure_init(current_run: Path, goal_input: Path, run_dir: Path):
    if (run_dir / "state.json").exists():
        return
    run_dir.mkdir(parents=True, exist_ok=True)
    proc, payload = run_json([
        sys.executable, str(PIPELINE), "init",
        "--current-run", str(current_run),
        "--goal-input", str(goal_input),
        "--run", str(run_dir),
    ])
    if proc.returncode != 0:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False, indent=2))


def semantic_loop(run_dir: Path, runner: str):
    while True:
        state = load_state(run_dir)
        if state["status"] == "complete":
            return
        if state["status"] == "failed":
            raise RuntimeError(f"goal pipeline failed: {state.get('failure')}")
        proc, packet = run_json([sys.executable, str(PIPELINE), "next", "--run", str(run_dir)])
        if proc.returncode != 0:
            raise RuntimeError(json.dumps(packet, ensure_ascii=False, indent=2))
        execute_runner(runner, packet)
        _, result = run_json([sys.executable, str(PIPELINE), "validate", "--run", str(run_dir)])
        state = load_state(run_dir)
        if state["status"] == "failed":
            raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Run Knowledge Constellation Goal → Target → Gap → Next Steps")
    parser.add_argument("--current-run", required=True)
    parser.add_argument("--goal-input", required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--runner-command", required=True)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()

    current_run = Path(args.current_run).resolve()
    goal_input = Path(args.goal_input).resolve()
    run_dir = Path(args.run).resolve()
    if args.fresh and run_dir.exists():
        shutil.rmtree(run_dir)

    ensure_init(current_run, goal_input, run_dir)
    semantic_loop(run_dir, args.runner_command)

    accepted = run_dir / "accepted"
    print(json.dumps({
        "status": "complete",
        "run": str(run_dir),
        "target": str(accepted / "target.json"),
        "gap": str(accepted / "gap.json"),
        "plan": str(accepted / "plan.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

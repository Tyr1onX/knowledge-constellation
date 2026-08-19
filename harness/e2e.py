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
PIPELINE = ROOT / "harness" / "pipeline.py"
COMPOSER = ROOT / "harness" / "compose_scene.py"
BUILDER = ROOT / "harness" / "build_site.py"
DELIVERY_VERIFIER = ROOT / "harness" / "verify_delivery.py"


def run_json(cmd, *, cwd=None, env=None):
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    try:
        payload = json.loads(proc.stdout)
    except Exception:
        payload = {"status": "tool_error", "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    return proc, payload


def load_state(run_dir):
    return json.loads((run_dir / "state.json").read_text(encoding="utf-8"))


def runner_command(template, packet):
    ws = Path(packet["workspace"])
    mapping = {"{workspace}": str(ws), "{task}": str(ws / "TASK.md"), "{output}": str(ws / "output.json"), "{stage}": packet["stage"]}
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
        raise RuntimeError(f"semantic runner failed for {packet['stage']} with exit code {proc.returncode}")
    if not output.exists():
        raise RuntimeError(f"semantic runner returned success but did not write {output}; read TASK.md and write JSON to KC_OUTPUT")


def ensure_init(input_path, run_dir):
    if (run_dir / "state.json").exists():
        return
    run_dir.mkdir(parents=True, exist_ok=True)
    proc, payload = run_json([sys.executable, str(PIPELINE), "init", "--input", str(input_path), "--run", str(run_dir)])
    if proc.returncode != 0:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False, indent=2))


def semantic_loop(run_dir, runner):
    while True:
        state = load_state(run_dir)
        if state["status"] == "complete":
            return
        if state["status"] == "failed":
            raise RuntimeError(f"pipeline failed: {state.get('failure')}")
        proc, packet = run_json([sys.executable, str(PIPELINE), "next", "--run", str(run_dir)])
        if proc.returncode != 0:
            raise RuntimeError(json.dumps(packet, ensure_ascii=False, indent=2))
        execute_runner(runner, packet)
        _, result = run_json([sys.executable, str(PIPELINE), "validate", "--run", str(run_dir)])
        state = load_state(run_dir)
        if state["status"] == "failed":
            raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))


def compose(run_dir, dist_dir):
    accepted = run_dir / "accepted"
    scene = dist_dir / "scene.json"
    dist_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, str(COMPOSER),
        "--input", str(accepted / "input.json"),
        "--evidence", str(accepted / "evidence.json"),
        "--model", str(accepted / "model.json"),
        "--structure", str(accepted / "structure.json"),
        "--visual", str(accepted / "visual.json"),
        "--schema", str(ROOT / "contracts" / "scene.schema.json"),
        "--output", str(scene),
    ]
    if subprocess.run(cmd).returncode != 0:
        raise RuntimeError("Scene Composer failed")
    return scene


def build_site(scene, dist_dir):
    if subprocess.run([sys.executable, str(BUILDER), "--scene", str(scene), "--output", str(dist_dir)]).returncode != 0:
        raise RuntimeError("Site builder failed")


def verify_delivery(run_dir, dist_dir):
    accepted_input = run_dir / "accepted" / "input.json"
    proc, payload = run_json([
        sys.executable, str(DELIVERY_VERIFIER),
        "--input", str(accepted_input),
        "--dist", str(dist_dir),
    ])
    if proc.returncode != 0:
        raise RuntimeError("Delivery verification failed:\n" + json.dumps(payload, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Run Knowledge Constellation from accepted raw input to an interactive v0.1 site.")
    ap.add_argument("--input", required=True, help="Input JSON matching contracts/input.schema.json")
    ap.add_argument("--run", required=True, help="Persistent run directory for Pass artifacts and repairs")
    ap.add_argument("--dist", required=True, help="Generated site directory")
    ap.add_argument("--runner-command", required=True, help="Semantic runner command. Runs inside each isolated Pass workspace and must write JSON to KC_OUTPUT. Supports {workspace}, {task}, {output}, {stage} placeholders.")
    ap.add_argument("--fresh", action="store_true", help="Delete an existing run directory before starting")
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    run_dir = Path(args.run).resolve()
    dist_dir = Path(args.dist).resolve()
    if args.fresh and run_dir.exists():
        shutil.rmtree(run_dir)

    ensure_init(input_path, run_dir)
    semantic_loop(run_dir, args.runner_command)
    scene = compose(run_dir, dist_dir)
    build_site(scene, dist_dir)
    verify_delivery(run_dir, dist_dir)
    print(json.dumps({
        "status": "complete",
        "run": str(run_dir),
        "scene": str(scene),
        "site": str(dist_dir / "index.html"),
        "share": str(dist_dir / "share.html"),
        "serve": f"{sys.executable} -m http.server 8000 --directory {shlex.quote(str(dist_dir))}",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["target", "gap", "plan"]
STAGE_META = {
    "target": {
        "prompt": ROOT / "prompts" / "pass-e-target.md",
        "schema": ROOT / "contracts" / "target.schema.json",
        "output": "target.json",
        "needs": ["goal_input"],
    },
    "gap": {
        "prompt": ROOT / "prompts" / "pass-f-gap.md",
        "schema": ROOT / "contracts" / "gap.schema.json",
        "output": "gap.json",
        "needs": ["goal_input", "target", "current_input", "current_evidence", "current_model"],
    },
    "plan": {
        "prompt": ROOT / "prompts" / "pass-g-plan.md",
        "schema": ROOT / "contracts" / "plan.schema.json",
        "output": "plan.json",
        "needs": ["goal_input", "target", "gap", "current_model"],
    },
}
MAX_REPAIRS = 2


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat()


def accepted_path(run: Path, name: str):
    return run / "accepted" / f"{name}.json"


def candidate_path(run: Path, stage: str):
    return run / "candidate" / STAGE_META[stage]["output"]


def workspace_path(run: Path, stage: str, attempt: int):
    return run / "workspaces" / f"{stage}-attempt-{attempt}"


def load_state(run: Path):
    return read_json(run / "state.json")


def save_state(run: Path, state):
    state["updated_at"] = now()
    write_json(run / "state.json", state)


def current_stage(state):
    index = state.get("stage_index", 0)
    return None if index >= len(STAGES) else STAGES[index]


def validate_json(file_path: Path, schema: Path):
    proc = subprocess.run([
        sys.executable,
        str(ROOT / "harness" / "validate.py"),
        "--stage", "input",
        "--file", str(file_path),
        "--schema", str(schema),
    ], capture_output=True, text=True)
    return proc


def require_completed_current_run(current_run: Path):
    state_path = current_run / "state.json"
    if not state_path.exists():
        raise SystemExit("--current-run must point to a completed Knowledge Constellation run")
    state = read_json(state_path)
    if state.get("status") != "complete":
        raise SystemExit("--current-run is not complete")
    required = ["input", "evidence", "model"]
    for name in required:
        if not (current_run / "accepted" / f"{name}.json").exists():
            raise SystemExit(f"--current-run is missing accepted/{name}.json")


def cmd_init(args):
    run = Path(args.run).resolve()
    current_run = Path(args.current_run).resolve()
    goal_input = Path(args.goal_input).resolve()
    require_completed_current_run(current_run)

    check = validate_json(goal_input, ROOT / "contracts" / "goal-input.schema.json")
    if check.returncode != 0:
        raise SystemExit("Invalid goal input contract:\n" + check.stdout + check.stderr)

    payload = read_json(goal_input)
    current_input = read_json(current_run / "accepted" / "input.json")
    if payload.get("subject_id") != current_input.get("subject", {}).get("id"):
        raise SystemExit("goal input subject_id must match the completed current Recognition run")

    if run.exists() and any(run.iterdir()):
        raise SystemExit(f"Goal run directory is not empty: {run}")
    for name in ["accepted", "candidate", "validation", "packets", "rejected", "workspaces", "current"]:
        (run / name).mkdir(parents=True, exist_ok=True)

    shutil.copy2(goal_input, accepted_path(run, "goal_input"))
    for name in ["input", "evidence", "model"]:
        shutil.copy2(current_run / "accepted" / f"{name}.json", run / "current" / f"{name}.json")

    state = {
        "version": "kc.goal-run.v1",
        "status": "running",
        "stage_index": 0,
        "repair_attempts": {stage: 0 for stage in STAGES},
        "current_run": str(current_run),
        "created_at": now(),
        "updated_at": now(),
        "history": [{"event": "init", "at": now(), "goal_id": payload["goal"]["id"]}],
    }
    save_state(run, state)
    print(json.dumps({"run": str(run), "stage": current_stage(state), "status": "running"}, ensure_ascii=False, indent=2))


def source_for_need(run: Path, need: str):
    if need.startswith("current_"):
        return run / "current" / f"{need.removeprefix('current_')}.json"
    return accepted_path(run, need)


def build_packet(run: Path, state):
    stage = current_stage(state)
    if not stage:
        return {"status": "complete"}
    meta = STAGE_META[stage]
    attempt = state["repair_attempts"].get(stage, 0)
    validation_file = run / "validation" / f"{stage}.json"
    errors = read_json(validation_file).get("errors", []) if validation_file.exists() else []

    packet = {
        "version": "kc.goal-packet.v1",
        "stage": stage,
        "mode": "repair" if attempt else "generate",
        "repair_attempt": attempt,
        "max_repairs": MAX_REPAIRS,
        "files": {
            "skill": str(ROOT / "SKILL.md"),
            "orchestration": str(ROOT / "skill" / "GOAL_ORCHESTRATION.md"),
            "prompt": str(meta["prompt"]),
            "schema": str(meta["schema"]),
            **{need: str(source_for_need(run, need)) for need in meta["needs"]},
        },
        "validation_errors": errors if attempt else [],
        "instruction": "Perform only this isolated Goal/Gap semantic pass. Do not inspect tests, baselines, other subjects, or renderer files.",
    }
    if attempt:
        previous = run / "rejected" / f"{stage}-attempt-{attempt}.json"
        if previous.exists():
            packet["files"]["previous_candidate"] = str(previous)
    return packet


def materialize_workspace(run: Path, packet):
    stage = packet["stage"]
    attempt = packet["repair_attempt"]
    ws = workspace_path(run, stage, attempt)
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True, exist_ok=True)

    copies = {
        "skill": (ROOT / "SKILL.md", "SKILL.md"),
        "orchestration": (ROOT / "skill" / "GOAL_ORCHESTRATION.md", "GOAL_ORCHESTRATION.md"),
        "prompt": (STAGE_META[stage]["prompt"], "PROMPT.md"),
        "schema": (STAGE_META[stage]["schema"], "schema.json"),
    }
    for need in STAGE_META[stage]["needs"]:
        copies[need] = (source_for_need(run, need), f"{need}.json")
    if attempt:
        previous = run / "rejected" / f"{stage}-attempt-{attempt}.json"
        if previous.exists():
            copies["previous_candidate"] = (previous, "previous_candidate.json")

    safe_files = {}
    for key, (src, name) in copies.items():
        dst = ws / name
        shutil.copy2(src, dst)
        safe_files[key] = str(dst)

    if packet.get("validation_errors"):
        error_path = ws / "validation_errors.json"
        write_json(error_path, {"errors": packet["validation_errors"]})
        safe_files["validation_errors"] = str(error_path)

    output = ws / "output.json"
    safe_files["output"] = str(output)
    (ws / "TASK.md").write_text(
        f"# Knowledge Constellation goal pass\n\nStage: {stage}\nMode: {packet['mode']}\nRepair attempt: {attempt}/{MAX_REPAIRS}\n\n"
        "Read only files in this workspace. Start with SKILL.md and PROMPT.md. Write only valid JSON matching schema.json to output.json.\n",
        encoding="utf-8",
    )
    safe_files["task"] = str(ws / "TASK.md")

    result = dict(packet)
    result["workspace"] = str(ws)
    result["files"] = safe_files
    result["instruction"] = "Work only inside the isolated workspace and write ONLY JSON to output.json."
    return result


def cmd_next(args):
    run = Path(args.run).resolve()
    state = load_state(run)
    if state["status"] != "running":
        print(json.dumps({"status": state["status"], "reason": state.get("failure")}, ensure_ascii=False, indent=2))
        return
    packet = materialize_workspace(run, build_packet(run, state))
    write_json(run / "packets" / f"{packet['stage']}-attempt-{packet['repair_attempt']}.json", packet)
    print(json.dumps(packet, ensure_ascii=False, indent=2))


def validator_command(run: Path, stage: str):
    cmd = [
        sys.executable,
        str(ROOT / "harness" / "validate_goal.py"),
        "--stage", stage,
        "--file", str(candidate_path(run, stage)),
        "--schema", str(STAGE_META[stage]["schema"]),
        "--goal-input", str(accepted_path(run, "goal_input")),
    ]
    if stage in {"gap", "plan"}:
        cmd += ["--target", str(accepted_path(run, "target"))]
    if stage == "gap":
        cmd += [
            "--current-model", str(run / "current" / "model.json"),
            "--current-evidence", str(run / "current" / "evidence.json"),
        ]
    if stage == "plan":
        cmd += [
            "--gap", str(accepted_path(run, "gap")),
            "--current-model", str(run / "current" / "model.json"),
        ]
    return cmd


def cmd_validate(args):
    run = Path(args.run).resolve()
    state = load_state(run)
    if state["status"] != "running":
        print(json.dumps({"status": state["status"], "reason": state.get("failure")}, ensure_ascii=False, indent=2))
        return
    stage = current_stage(state)
    attempt = state["repair_attempts"].get(stage, 0)
    ws_output = workspace_path(run, stage, attempt) / "output.json"
    if not ws_output.exists():
        raise SystemExit(f"missing semantic output: {ws_output}")
    shutil.copy2(ws_output, candidate_path(run, stage))

    proc = subprocess.run(validator_command(run, stage), capture_output=True, text=True)
    try:
        result = json.loads(proc.stdout)
    except Exception:
        result = {"pass": False, "errors": [proc.stdout + proc.stderr]}
    write_json(run / "validation" / f"{stage}.json", result)

    if result.get("pass"):
        shutil.copy2(candidate_path(run, stage), accepted_path(run, stage))
        state["history"].append({"event": "accepted", "stage": stage, "attempt": attempt, "at": now()})
        state["stage_index"] += 1
        if state["stage_index"] >= len(STAGES):
            state["status"] = "complete"
    else:
        rejected = run / "rejected" / f"{stage}-attempt-{attempt + 1}.json"
        shutil.copy2(candidate_path(run, stage), rejected)
        state["repair_attempts"][stage] = attempt + 1
        state["history"].append({"event": "rejected", "stage": stage, "attempt": attempt, "at": now(), "errors": result.get("errors", [])})
        if state["repair_attempts"][stage] > MAX_REPAIRS:
            state["status"] = "failed"
            state["failure"] = {"stage": stage, "errors": result.get("errors", [])}

    save_state(run, state)
    print(json.dumps({**result, "status": state["status"], "next_stage": current_stage(state)}, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("pass") else 1)


def main():
    parser = argparse.ArgumentParser(description="Knowledge Constellation Goal → Target → Gap → Plan pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--current-run", required=True)
    p_init.add_argument("--goal-input", required=True)
    p_init.add_argument("--run", required=True)
    p_init.set_defaults(func=cmd_init)

    p_next = sub.add_parser("next")
    p_next.add_argument("--run", required=True)
    p_next.set_defaults(func=cmd_next)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--run", required=True)
    p_validate.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

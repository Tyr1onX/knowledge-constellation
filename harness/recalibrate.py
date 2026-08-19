#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2E = ROOT / "harness" / "e2e.py"
CALIBRATION_KIND = "user_calibration"
CALIBRATION_VERSION = "kc.calibration.v1"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def calibration_source(feedback: str):
    text = feedback.strip()
    if not text:
        raise ValueError("calibration feedback must not be empty")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return {
        "id": f"CAL-{digest}",
        "kind": CALIBRATION_KIND,
        "title": "User calibration",
        "uri": None,
        "content": text,
        "observed_at": None,
    }


def build_calibrated_input(base_input, feedback: str):
    if not isinstance(base_input, dict) or not isinstance(base_input.get("sources"), list):
        raise ValueError("accepted input is missing sources[]")
    result = json.loads(json.dumps(base_input, ensure_ascii=False))
    source = calibration_source(feedback)
    existing = next((item for item in result["sources"] if item.get("id") == source["id"]), None)
    if existing:
        if existing.get("kind") != CALIBRATION_KIND or existing.get("content") != source["content"]:
            raise ValueError(f"calibration source id collision: {source['id']}")
    else:
        result["sources"].append(source)
    return result, source


def load_completed_input(from_run: Path):
    state_path = from_run / "state.json"
    accepted_input = from_run / "accepted" / "input.json"
    if not state_path.exists() or not accepted_input.exists():
        raise ValueError("--from-run must point to a completed Knowledge Constellation run")
    state = read_json(state_path)
    if state.get("status") != "complete":
        raise ValueError("--from-run is not complete; calibration must start from an accepted run")
    return read_json(accepted_input)


def recalibration_command(input_path: Path, run_dir: Path, dist_dir: Path, runner_command: str, fresh: bool):
    cmd = [
        sys.executable,
        str(E2E),
        "--input", str(input_path),
        "--run", str(run_dir),
        "--dist", str(dist_dir),
        "--runner-command", runner_command,
    ]
    if fresh:
        cmd.append("--fresh")
    return cmd


def main():
    ap = argparse.ArgumentParser(description="Re-run Knowledge Constellation from user feedback without patching Recognition or Scene artifacts in place.")
    ap.add_argument("--from-run", required=True, help="Completed prior run containing accepted/input.json")
    feedback_group = ap.add_mutually_exclusive_group(required=True)
    feedback_group.add_argument("--feedback", help="Natural-language correction or representativeness feedback from the subject")
    feedback_group.add_argument("--feedback-file", help="UTF-8 file containing the subject's feedback")
    ap.add_argument("--run", required=True, help="New run directory for the calibrated revision")
    ap.add_argument("--dist", required=True, help="New generated site directory")
    ap.add_argument("--runner-command", required=True, help="Semantic runner command forwarded to harness/e2e.py")
    ap.add_argument("--fresh", action="store_true", help="Delete an existing target run directory before recalibration")
    args = ap.parse_args()

    from_run = Path(args.from_run).resolve()
    run_dir = Path(args.run).resolve()
    dist_dir = Path(args.dist).resolve()
    if run_dir == from_run:
        raise SystemExit("--run must be a new revision directory; never overwrite --from-run")
    feedback = args.feedback if args.feedback is not None else Path(args.feedback_file).read_text(encoding="utf-8")

    try:
        base_input = load_completed_input(from_run)
        calibrated_input, source = build_calibrated_input(base_input, feedback)
    except ValueError as exc:
        raise SystemExit(str(exc))

    with tempfile.TemporaryDirectory(prefix="kc-calibration-") as td:
        input_path = Path(td) / "input.json"
        write_json(input_path, calibrated_input)
        proc = subprocess.run(recalibration_command(input_path, run_dir, dist_dir, args.runner_command, args.fresh))
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)

    calibration_count = sum(1 for item in calibrated_input["sources"] if item.get("kind") == CALIBRATION_KIND)
    lineage = {
        "version": CALIBRATION_VERSION,
        "parent_run": str(from_run),
        "feedback_source_id": source["id"],
        "revision": calibration_count,
        "rule": "feedback is appended as first-party Source evidence; semantic passes are rerun from Pass A; accepted Model/Structure/Scene are never patched in place",
    }
    write_json(run_dir / "calibration.json", lineage)
    print(json.dumps({
        "status": "complete",
        "calibration": lineage,
        "site": str(dist_dir / "index.html"),
        "share": str(dist_dir / "share.html"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

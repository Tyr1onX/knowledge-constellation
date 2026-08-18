#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate import schema_errors, semantic_errors

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "evidence": ROOT / "contracts" / "evidence.schema.json",
    "model": ROOT / "contracts" / "model.schema.json",
    "structure": ROOT / "contracts" / "structure.schema.json",
    "visual": ROOT / "contracts" / "visual.schema.json",
}
FILES = {
    "evidence": "pass-a.json",
    "model": "pass-b.json",
    "structure": "pass-c.json",
    "visual": "pass-d.json",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def synthetic_input(manifest):
    subject = manifest.get("subject")
    if not isinstance(subject, dict) or not subject.get("id") or not subject.get("label"):
        raise ValueError("v2 source-manifest.json requires subject.id and subject.label")
    sources = []
    for src in manifest.get("sources", []):
        sid = src.get("id")
        if not sid:
            raise ValueError("every frozen source requires an id")
        sources.append({
            "id": sid,
            "kind": src.get("kind", "frozen_source"),
            "title": src.get("title") or src.get("repo") or src.get("url") or sid,
            "content": src.get("observation") or src.get("frozen_excerpt") or "frozen source",
        })
    if not sources:
        raise ValueError("v2 source-manifest.json requires at least one source")
    return {"subject": subject, "sources": sources}


def verify_case(case_dir: Path):
    case_dir = case_dir.resolve()
    metadata = load(case_dir / "metadata.json")
    if metadata.get("protocol_version") != "kc.cleanroom.v2":
        return {"pass": False, "errors": ["metadata.protocol_version must be kc.cleanroom.v2"]}
    if metadata.get("validation_mode") != "harness":
        return {"pass": False, "errors": ["metadata.validation_mode must be harness"]}

    manifest = load(case_dir / "source-manifest.json")
    input_obj = synthetic_input(manifest)
    runner = case_dir / "runner"

    data = {}
    errors = []
    stage_results = {}
    for stage, filename in FILES.items():
        path = runner / filename
        if not path.exists():
            errors.append(f"missing runner/{filename}")
            continue
        data[stage] = load(path)

    if errors:
        return {"pass": False, "errors": errors, "stages": stage_results}

    upstream = {
        "evidence": {"input": input_obj},
        "model": {"evidence": data["evidence"]},
        "structure": {"evidence": data["evidence"], "model": data["model"]},
        "visual": {"input": input_obj, "structure": data["structure"]},
    }

    for stage in ["evidence", "model", "structure", "visual"]:
        stage_errors = schema_errors(data[stage], SCHEMAS[stage])
        stage_errors += semantic_errors(stage, data[stage], upstream[stage])
        stage_results[stage] = {"pass": not stage_errors, "errors": stage_errors}
        errors.extend(f"{stage}: {msg}" for msg in stage_errors)

    proof = runner / "validation-proof.json"
    if not proof.exists():
        errors.append("missing runner/validation-proof.json")
    else:
        stored = load(proof)
        if stored.get("validator") != "harness/verify_eval_case.py":
            errors.append("validation-proof.json has unexpected validator")
        if stored.get("pass") is not True:
            errors.append("validation-proof.json does not record pass=true")

    return {"pass": not errors, "errors": errors, "stages": stage_results}


def main():
    parser = argparse.ArgumentParser(description="Verify a kc.cleanroom.v2 case against active contracts")
    parser.add_argument("case_dir")
    args = parser.parse_args()
    try:
        result = verify_case(Path(args.case_dir))
    except Exception as exc:
        result = {"pass": False, "errors": [f"verification exception: {exc}"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("pass") else 1)


if __name__ == "__main__":
    main()

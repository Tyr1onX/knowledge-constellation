#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:
    raise SystemExit(
        "jsonschema is required for Knowledge Constellation validation. "
        "Install dependencies with: pip install -r requirements.txt"
    ) from exc


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def schema_errors(data, schema_path):
    validator = jsonschema.Draft202012Validator(load(schema_path))
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda x: list(x.path)):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path)
        errors.append(f"schema {path}: {error.message}")
    return errors


def duplicates(values):
    seen, dup = set(), set()
    for value in values:
        if value in seen:
            dup.add(value)
        seen.add(value)
    return sorted(dup)


def semantic_errors(stage, data, upstream):
    errors = []
    goal_input = upstream.get("goal_input", {})
    goal = goal_input.get("goal", {})
    goal_id = goal.get("id")

    if data.get("goal_id") != goal_id:
        errors.append(f"goal_id must equal accepted goal id {goal_id!r}")

    if stage == "target":
        source_ids = {source.get("id") for source in goal_input.get("target_sources", [])}
        requirements = data.get("requirements", [])
        ids = [item.get("id") for item in requirements]
        if duplicates(ids):
            errors.append(f"duplicate requirement ids: {duplicates(ids)}")
        for requirement in requirements:
            missing = set(requirement.get("source_ids", [])) - source_ids
            if missing:
                errors.append(f"{requirement.get('id')}: unknown target source ids {sorted(missing)}")
            if requirement.get("kind") == "eligibility" and requirement.get("dimension") not in (None, "eligibility"):
                errors.append(f"{requirement.get('id')}: eligibility requirement should not masquerade as a learning dimension")

    elif stage == "gap":
        target = upstream["target"]
        requirement_ids = {item["id"] for item in target.get("requirements", [])}
        items = data.get("items", [])
        item_ids = [item.get("requirement_id") for item in items]
        if duplicates(item_ids):
            errors.append(f"duplicate gap requirement ids: {duplicates(item_ids)}")
        if set(item_ids) != requirement_ids:
            missing = sorted(requirement_ids - set(item_ids))
            extra = sorted(set(item_ids) - requirement_ids)
            errors.append(f"gap must account for every target requirement exactly once; missing={missing}, extra={extra}")

        model = upstream["current_model"]
        evidence = upstream["current_evidence"]
        node_ids = {node["id"] for node in model.get("nodes", [])}
        claim_ids = {claim["id"] for claim in model.get("claims", [])}
        evidence_ids = {item["id"] for item in evidence.get("evidence", [])}

        for item in items:
            rid = item.get("requirement_id")
            unknown_nodes = (set(item.get("current_node_ids", [])) | set(item.get("bridge_from_node_ids", []))) - node_ids
            unknown_claims = set(item.get("current_claim_ids", [])) - claim_ids
            unknown_evidence = set(item.get("current_evidence_ids", [])) - evidence_ids
            if unknown_nodes:
                errors.append(f"{rid}: unknown current node ids {sorted(unknown_nodes)}")
            if unknown_claims:
                errors.append(f"{rid}: unknown current claim ids {sorted(unknown_claims)}")
            if unknown_evidence:
                errors.append(f"{rid}: unknown current evidence ids {sorted(unknown_evidence)}")

            status = item.get("status")
            direct_evidence = item.get("current_evidence_ids", [])
            if status in {"supported", "partial"} and not direct_evidence:
                errors.append(f"{rid}: {status} status requires current evidence")
            if status == "not_observed" and direct_evidence:
                errors.append(f"{rid}: not_observed must not cite direct supporting evidence; use bridge_from_node_ids for adjacent footholds")
            if status == "unresolved" and not item.get("verification_needed"):
                errors.append(f"{rid}: unresolved status should state what evidence would resolve it")

    elif stage == "plan":
        target = upstream["target"]
        gap = upstream["gap"]
        model = upstream["current_model"]
        requirements = {item["id"]: item for item in target.get("requirements", [])}
        gap_by_requirement = {item["requirement_id"]: item for item in gap.get("items", [])}
        node_ids = {node["id"] for node in model.get("nodes", [])}

        ranks = [item.get("rank") for item in data.get("priorities", [])]
        if duplicates(ranks):
            errors.append(f"duplicate priority ranks: {duplicates(ranks)}")
        if sorted(ranks) != list(range(1, len(ranks) + 1)):
            errors.append("priority ranks must be contiguous starting at 1")

        used_requirements = set()
        for priority in data.get("priorities", []):
            pids = set(priority.get("requirement_ids", []))
            unknown = pids - set(requirements)
            if unknown:
                errors.append(f"{priority.get('id')}: unknown requirement ids {sorted(unknown)}")
                continue
            used_requirements |= pids
            eligibility = sorted(rid for rid in pids if requirements[rid].get("kind") == "eligibility")
            if eligibility:
                errors.append(f"{priority.get('id')}: eligibility constraints cannot be learning priorities {eligibility}")
            statuses = {gap_by_requirement[rid].get("status") for rid in pids if rid in gap_by_requirement}
            if statuses and statuses <= {"supported", "not_applicable"}:
                errors.append(f"{priority.get('id')}: priority must advance at least one partial/unresolved/not_observed requirement")
            unknown_footholds = set(priority.get("current_foothold_node_ids", [])) - node_ids
            if unknown_footholds:
                errors.append(f"{priority.get('id')}: unknown current foothold nodes {sorted(unknown_footholds)}")

        deferred = set(data.get("deferred_requirement_ids", []))
        unknown_deferred = deferred - set(requirements)
        if unknown_deferred:
            errors.append(f"unknown deferred requirement ids {sorted(unknown_deferred)}")
        if deferred & used_requirements:
            errors.append(f"requirements cannot be both priority and deferred: {sorted(deferred & used_requirements)}")

        constraint_ids = [item.get("requirement_id") for item in data.get("non_learning_constraints", [])]
        if duplicates(constraint_ids):
            errors.append(f"duplicate non-learning constraint ids: {duplicates(constraint_ids)}")
        for rid in constraint_ids:
            if rid not in requirements:
                errors.append(f"non-learning constraint references unknown requirement {rid}")
            elif requirements[rid].get("kind") != "eligibility":
                errors.append(f"{rid}: non-learning constraints may only reference eligibility requirements")

        unresolved_eligibility = {
            rid for rid, requirement in requirements.items()
            if requirement.get("kind") == "eligibility"
            and gap_by_requirement.get(rid, {}).get("status") not in {"supported", "not_applicable"}
        }
        if unresolved_eligibility - set(constraint_ids):
            errors.append(
                "unresolved eligibility requirements must be surfaced as non-learning constraints: "
                + str(sorted(unresolved_eligibility - set(constraint_ids)))
            )

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["target", "gap", "plan"], required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--goal-input", required=True)
    parser.add_argument("--target")
    parser.add_argument("--gap")
    parser.add_argument("--current-model")
    parser.add_argument("--current-evidence")
    args = parser.parse_args()

    data = load(args.file)
    upstream = {"goal_input": load(args.goal_input)}
    for arg_name, key in [
        ("target", "target"),
        ("gap", "gap"),
        ("current_model", "current_model"),
        ("current_evidence", "current_evidence"),
    ]:
        path = getattr(args, arg_name)
        if path:
            upstream[key] = load(path)

    errors = schema_errors(data, args.schema) + semantic_errors(args.stage, data, upstream)
    print(json.dumps({"pass": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()

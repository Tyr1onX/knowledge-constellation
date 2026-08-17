#!/usr/bin/env python3
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

STRONG_DIMS = {"implementation", "independence", "troubleshooting", "transfer"}
STRONG_VALUES = {"established", "high", "supported", "independent", "strong"}
FORBIDDEN_VISUAL_TRUTH = {"known", "unknown", "evidence", "boundary", "claims", "confidence", "reason"}
GENERIC_GALAXY_LABELS = {
    "frontend", "backend", "database", "databases", "programming languages",
    "前端", "后端", "数据库", "编程语言", "技术栈"
}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def schema_errors(data, schema_path):
    validator = jsonschema.Draft202012Validator(load(schema_path))
    errors = []
    for e in sorted(validator.iter_errors(data), key=lambda x: list(x.path)):
        path = "$" + "".join(f"[{x}]" if isinstance(x, int) else f".{x}" for x in e.path)
        errors.append(f"schema {path}: {e.message}")
    return errors


def duplicates(values):
    seen, dup = set(), set()
    for v in values:
        if v in seen:
            dup.add(v)
        seen.add(v)
    return sorted(dup)


def semantic_errors(stage, data, up):
    errors = []

    if stage == "evidence":
        source_ids = {s["id"] for s in up["input"]["sources"]}
        ids = [e["id"] for e in data.get("evidence", [])]
        if duplicates(ids):
            errors.append(f"duplicate evidence ids: {duplicates(ids)}")
        for e in data.get("evidence", []):
            missing = set(e.get("source_ids", [])) - source_ids
            if missing:
                errors.append(f"{e.get('id')}: unknown source ids {sorted(missing)}")
            if not e.get("does_not_support"):
                errors.append(f"{e.get('id')}: evidence requires an explicit boundary")
            if not e.get("supports"):
                errors.append(f"{e.get('id')}: evidence must state what it supports")

    elif stage == "model":
        evidence = {e["id"]: e for e in up["evidence"].get("evidence", [])}
        evidence_ids = set(evidence)
        claims = data.get("claims", [])
        nodes = data.get("nodes", [])
        claim_ids = [c["id"] for c in claims]
        node_ids = [n["id"] for n in nodes]
        if duplicates(claim_ids):
            errors.append(f"duplicate claim ids: {duplicates(claim_ids)}")
        if duplicates(node_ids):
            errors.append(f"duplicate node ids: {duplicates(node_ids)}")
        node_id_set = set(node_ids)

        for c in claims:
            missing = set(c.get("evidence", [])) - evidence_ids
            if missing:
                errors.append(f"{c['id']}: unknown evidence {sorted(missing)}")
            if c.get("subject") not in node_id_set:
                errors.append(f"{c['id']}: claim subject must resolve to a node id")
            if c.get("dimension") in STRONG_DIMS and str(c.get("value")).lower() in STRONG_VALUES:
                refs = [evidence[x] for x in c.get("evidence", []) if x in evidence]
                groups = {
                    r.get("correlation_group") or ("sources:" + ",".join(sorted(r.get("source_ids", []))))
                    for r in refs
                }
                source_union = {sid for r in refs for sid in r.get("source_ids", [])}
                has_external = any(r.get("attribution") == "external" for r in refs)
                if len(refs) < 2 or len(groups) < 2:
                    errors.append(
                        f"{c['id']}: strong {c['dimension']} claim needs multiple independent evidence groups"
                    )
                elif len(source_union) < 2 and not has_external:
                    errors.append(
                        f"{c['id']}: strong {c['dimension']} claim needs multi-source provenance or external validation"
                    )

        claim_id_set = set(claim_ids)
        for n in nodes:
            missing_e = set(n.get("evidence", [])) - evidence_ids
            if missing_e:
                errors.append(f"{n['id']}: unknown evidence {sorted(missing_e)}")
            missing_c = set(n.get("claims", [])) - claim_id_set
            if missing_c:
                errors.append(f"{n['id']}: unknown claims {sorted(missing_c)}")
            if not n.get("unknown"):
                errors.append(f"{n['id']}: node must preserve unresolved dimensions")
            if not n.get("boundary"):
                errors.append(f"{n['id']}: node needs explicit boundary")
            if not n.get("known"):
                errors.append(f"{n['id']}: node needs at least one supported known statement")

    elif stage == "structure":
        node_ids = {n["id"] for n in up["model"].get("nodes", [])}
        evidence_ids = {e["id"] for e in up["evidence"].get("evidence", [])}
        anchors = {a["id"]: a for a in data.get("anchors", [])}
        membership = {}

        if duplicates([a["id"] for a in data.get("anchors", [])]):
            errors.append("duplicate anchor ids")
        if duplicates([g["id"] for g in data.get("galaxies", [])]):
            errors.append("duplicate galaxy ids")

        for a in data.get("anchors", []):
            unknown = set(a.get("nodes", [])) - node_ids
            if unknown:
                errors.append(f"{a['id']}: anchor contains unknown nodes {sorted(unknown)}")

        for r in data.get("relations", []):
            if r["source"] not in node_ids or r["target"] not in node_ids:
                errors.append(f"relation {r['source']}->{r['target']}: unknown node")
            if r["source"] == r["target"]:
                errors.append(f"relation {r['source']}->{r['target']}: self relation is invalid")
            if not r.get("evidence") or set(r.get("evidence", [])) - evidence_ids:
                errors.append(f"relation {r['source']}->{r['target']}: invalid evidence")

        for g in data.get("galaxies", []):
            if g["anchor"] not in anchors:
                errors.append(f"{g['id']}: unknown anchor")
            if g.get("label", "").strip().lower() in GENERIC_GALAXY_LABELS:
                errors.append(f"{g['id']}: generic syllabus label is not acceptable without stronger personalization")
            members = g.get("primary_nodes", []) + g.get("secondary_nodes", [])
            for nid in members:
                if nid not in node_ids:
                    errors.append(f"{g['id']}: unknown node {nid}")
                if nid in membership:
                    errors.append(f"{nid}: appears in multiple galaxies ({membership[nid]}, {g['id']})")
                membership[nid] = g["id"]

        unassigned = node_ids - set(membership)
        if unassigned:
            errors.append(f"unassigned nodes: {sorted(unassigned)}")

        dist = data.get("distillation", {})
        primary = set(dist.get("primary_nodes", []))
        secondary = set(dist.get("secondary_nodes", []))
        if primary & secondary:
            errors.append(f"distillation nodes appear in both layers: {sorted(primary & secondary)}")
        if primary | secondary != node_ids:
            errors.append("distillation must account for every accepted node exactly once")
        galaxy_primary = {x for g in data.get("galaxies", []) for x in g.get("primary_nodes", [])}
        if primary != galaxy_primary:
            errors.append("distillation.primary_nodes must equal the union of Galaxy primary_nodes")

    elif stage == "visual":
        galaxy_ids = {g["id"] for g in up["structure"].get("galaxies", [])}
        visual_ids = {g["id"] for g in data.get("galaxies", [])}
        if galaxy_ids != visual_ids:
            errors.append("visual galaxies must exactly match accepted structure galaxies")

        def walk(x, path="$"):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in FORBIDDEN_VISUAL_TRUTH:
                        errors.append(f"{path}.{k}: recognition truth leaked into visual model")
                    walk(v, f"{path}.{k}")
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    walk(v, f"{path}[{i}]")
        walk(data)

    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["input", "evidence", "model", "structure", "visual"], required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--schema", required=True)
    ap.add_argument("--input")
    ap.add_argument("--evidence")
    ap.add_argument("--model")
    ap.add_argument("--structure")
    args = ap.parse_args()

    data = load(args.file)
    up = {}
    for name in ["input", "evidence", "model", "structure"]:
        p = getattr(args, name)
        if p:
            up[name] = load(p)

    errors = schema_errors(data, args.schema) + semantic_errors(args.stage, data, up)
    result = {"pass": not errors, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()

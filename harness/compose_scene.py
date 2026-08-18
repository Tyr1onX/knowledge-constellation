#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

WORLD_WIDTH = 1000
WORLD_HEIGHT = 760

ARCHETYPE_POINTS = {
    "dominant_core_satellites": [(0.50, 0.43), (0.25, 0.28), (0.76, 0.30), (0.73, 0.70), (0.28, 0.69), (0.50, 0.82)],
    "dual_core": [(0.34, 0.43), (0.67, 0.52), (0.22, 0.72), (0.80, 0.26), (0.56, 0.78), (0.47, 0.20)],
    "three_islands": [(0.29, 0.31), (0.72, 0.34), (0.53, 0.72), (0.18, 0.69), (0.83, 0.70), (0.50, 0.17)],
    "stream": [(0.18, 0.28), (0.35, 0.38), (0.52, 0.48), (0.69, 0.58), (0.84, 0.68), (0.62, 0.77)],
    "sparse_archipelago": [(0.18, 0.26), (0.74, 0.22), (0.82, 0.67), (0.39, 0.76), (0.49, 0.42), (0.18, 0.62)],
    "compact_cluster": [(0.42, 0.39), (0.61, 0.40), (0.54, 0.59), (0.36, 0.57), (0.52, 0.27), (0.68, 0.57)],
    "asymmetric_chain": [(0.20, 0.27), (0.39, 0.35), (0.55, 0.49), (0.68, 0.62), (0.84, 0.70), (0.30, 0.74)],
}

REP_SIZE = {"low": 0.36, "medium": 0.58, "high": 0.79}
RELATION_STYLE = {
    "co_occurrence": (118, 0.10),
    "repeated_context": (102, 0.16),
    "trajectory": (132, 0.12),
    "practice": (94, 0.14),
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stable01(seed):
    raw = hashlib.sha256(seed.encode("utf-8")).digest()[:8]
    return int.from_bytes(raw, "big") / ((1 << 64) - 1)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def galaxy_centers(visual, structure, width=WORLD_WIDTH, height=WORLD_HEIGHT):
    galaxies = structure.get("galaxies", [])
    archetype = visual.get("composition", {}).get("archetype", "sparse_archipelago")
    points = list(ARCHETYPE_POINTS.get(archetype, ARCHETYPE_POINTS["sparse_archipelago"]))
    seed = visual.get("seed", "knowledge-constellation")
    while len(points) < len(galaxies):
        i = len(points)
        angle = i * 2.399963229728653 + stable01(f"{seed}|galaxy-angle|{i}") * 0.42
        radius = 0.22 + 0.19 * stable01(f"{seed}|galaxy-radius|{i}")
        points.append((0.5 + math.cos(angle) * radius, 0.5 + math.sin(angle) * radius))

    visual_by_id = {g["id"]: g for g in visual.get("galaxies", [])}
    result = {}
    for i, g in enumerate(galaxies):
        x, y = points[i]
        mass = visual_by_id.get(g["id"], {}).get("mass", 0.5)
        pad = 0.10 + (1 - mass) * 0.015
        result[g["id"]] = {
            "x": round(clamp(x, pad, 1 - pad) * width, 3),
            "y": round(clamp(y, pad, 1 - pad) * height, 3),
        }
    return result


def node_membership(structure):
    out = {}
    for galaxy in structure.get("galaxies", []):
        for index, nid in enumerate(galaxy.get("primary_nodes", [])):
            out[nid] = {"galaxy": galaxy["id"], "layer": "primary", "primary_index": index, "anchor": galaxy["anchor"]}
        for nid in galaxy.get("secondary_nodes", []):
            out[nid] = {"galaxy": galaxy["id"], "layer": "secondary", "primary_index": None, "anchor": galaxy["anchor"]}
    return out


def node_kind(node, member):
    if member["layer"] == "primary" and member["primary_index"] == 0:
        return "core"
    if node.get("state") in {"observed", "unresolved"}:
        return "trace"
    if node.get("state") == "developing":
        return "soft"
    return "normal"


def node_size(node, member):
    base = REP_SIZE.get(node.get("representativeness"), 0.50)
    if member["layer"] == "primary":
        base += 0.10
    if member["primary_index"] == 0:
        base += 0.08
    return round(clamp(base, 0.28, 0.98), 3)


def initial_node_point(seed, node_id, galaxy_center, layer, primary_index):
    jitter = stable01(f"{seed}|node-jitter|{node_id}")
    angle = stable01(f"{seed}|node-angle|{node_id}") * math.tau
    radius = 26 + (primary_index or 0) * 19 + jitter * 28 if layer == "primary" else 66 + jitter * 88
    return {
        "x": round(galaxy_center["x"] + math.cos(angle) * radius, 3),
        "y": round(galaxy_center["y"] + math.sin(angle) * radius, 3),
    }


def compose_scene(input_data, evidence_data, model, structure, visual):
    centers = galaxy_centers(visual, structure)
    membership = node_membership(structure)
    model_nodes = {n["id"]: n for n in model.get("nodes", [])}
    evidence = {e["id"]: e for e in evidence_data.get("evidence", [])}
    anchors = {a["id"]: a for a in structure.get("anchors", [])}
    visual_anchors = {a["id"]: a for a in visual.get("anchors", [])}
    source_titles = {s["id"]: s.get("title", s["id"]) for s in input_data.get("sources", [])}
    seed = visual["seed"]

    scene_nodes = []
    for nid, node in model_nodes.items():
        member = membership[nid]
        point = initial_node_point(seed, nid, centers[member["galaxy"]], member["layer"], member["primary_index"])
        anchor = anchors.get(member["anchor"], {})
        ev_items = []
        source_ids = []
        for eid in node.get("evidence", []):
            item = evidence.get(eid)
            if not item:
                continue
            ev_items.append({"id": eid, "observation": item.get("observation", ""), "source_ids": item.get("source_ids", [])})
            source_ids.extend(item.get("source_ids", []))
        scene_nodes.append({
            "id": nid,
            "name": node["label"],
            "en": node.get("english_label"),
            "g": member["galaxy"],
            "layer": member["layer"],
            "kind": node_kind(node, member),
            "size": node_size(node, member),
            "x": point["x"],
            "y": point["y"],
            "summary": node.get("summary", ""),
            "project": anchor.get("label", ""),
            "anchor_id": member["anchor"],
            "evidence": ev_items,
            "sources": [{"id": sid, "title": source_titles.get(sid, sid)} for sid in dict.fromkeys(source_ids)],
        })

    scene_relations = []
    for rel in structure.get("relations", []):
        distance, strength = RELATION_STYLE.get(rel["kind"], (112, 0.11))
        scene_relations.append({"source": rel["source"], "target": rel["target"], "kind": rel["kind"], "distance": distance, "strength": strength})

    structure_galaxies = {g["id"]: g for g in structure.get("galaxies", [])}
    visual_galaxies = {g["id"]: g for g in visual.get("galaxies", [])}
    scene_galaxies = []
    for gid, g in structure_galaxies.items():
        vg = visual_galaxies[gid]
        center = centers[gid]
        scene_galaxies.append({
            "id": gid, "name": g["label"], "x": center["x"], "y": center["y"],
            "mass": vg["mass"], "morphology": vg["morphology"], "dominance": vg["dominance"],
            "anchor": g["anchor"], "primary_nodes": g.get("primary_nodes", []), "secondary_nodes": g.get("secondary_nodes", []),
        })

    scene_anchors = []
    for i, anchor in enumerate(structure.get("anchors", [])):
        va = visual_anchors[anchor["id"]]
        galaxies = va["galaxies"]
        if galaxies:
            avg_x = sum(centers[g]["x"] for g in galaxies) / len(galaxies)
            avg_y = sum(centers[g]["y"] for g in galaxies) / len(galaxies)
        else:
            avg_x, avg_y = WORLD_WIDTH / 2, WORLD_HEIGHT / 2
        angle = stable01(f"{seed}|anchor-angle|{anchor['id']}") * math.tau
        radius = 30 + stable01(f"{seed}|anchor-radius|{anchor['id']}") * 24
        scene_anchors.append({
            "id": anchor["id"], "name": anchor["label"], "kind": anchor["kind"], "nodes": anchor.get("nodes", []),
            "galaxies": galaxies, "g": galaxies[0] if galaxies else None, "role": va["role"], "prominence": va["prominence"],
            "x": round(avg_x + math.cos(angle) * radius, 3), "y": round(avg_y + math.sin(angle) * radius, 3), "phaseOffset": i,
        })

    subject = input_data["subject"]
    identity = dict(visual["identity"])
    identity["title"] = subject["label"]
    identity["subtitle"] = identity.get("presence", {}).get("subtitle") or "由作品、经历与学习痕迹生长出的知识星图"
    identity["source"] = subject.get("scope") or "Knowledge Constellation"
    identity["x"] = WORLD_WIDTH / 2
    identity["y"] = WORLD_HEIGHT / 2

    return {
        "version": "kc.scene.v1", "seed": seed,
        "subject": {"id": subject["id"], "label": subject["label"], "language": subject.get("language"), "scope": subject.get("scope")},
        "viewport": {"width": WORLD_WIDTH, "height": WORLD_HEIGHT},
        "identity": identity, "composition": visual["composition"], "field": visual["field"], "stars": visual["stars"], "motion": visual["motion"],
        "nodes": scene_nodes, "relations": scene_relations, "anchors": scene_anchors, "galaxies": scene_galaxies, "motifs": structure.get("motifs", []),
    }


def validate_scene_semantics(scene, input_data, model, structure):
    errors = []
    node_ids = {n["id"] for n in model.get("nodes", [])}
    if {n["id"] for n in scene.get("nodes", [])} != node_ids:
        errors.append("scene nodes must exactly match accepted model nodes")
    expected_rel = {(r["source"], r["target"], r["kind"]) for r in structure.get("relations", [])}
    actual_rel = {(r["source"], r["target"], r["kind"]) for r in scene.get("relations", [])}
    if expected_rel != actual_rel:
        errors.append("scene relations must exactly match accepted structure relations")
    if {a["id"] for a in scene.get("anchors", [])} != {a["id"] for a in structure.get("anchors", [])}:
        errors.append("scene anchors must exactly match accepted structure anchors")
    if {g["id"] for g in scene.get("galaxies", [])} != {g["id"] for g in structure.get("galaxies", [])}:
        errors.append("scene galaxies must exactly match accepted structure galaxies")
    if scene.get("identity", {}).get("label") != input_data["subject"]["label"]:
        errors.append("scene identity.label must preserve exact input subject label")
    return errors


def main():
    ap = argparse.ArgumentParser(description="Compose accepted Knowledge Model + Structure + Visual Model into kc.scene.v1.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--structure", required=True)
    ap.add_argument("--visual", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--schema")
    args = ap.parse_args()

    input_data = read_json(args.input)
    evidence = read_json(args.evidence)
    model = read_json(args.model)
    structure = read_json(args.structure)
    visual = read_json(args.visual)
    scene = compose_scene(input_data, evidence, model, structure, visual)
    errors = validate_scene_semantics(scene, input_data, model, structure)
    if args.schema:
        try:
            import jsonschema
            jsonschema.validate(scene, read_json(args.schema))
        except Exception as exc:
            errors.append(f"scene schema validation failed: {exc}")
    if errors:
        print(json.dumps({"pass": False, "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    write_json(args.output, scene)
    print(json.dumps({"pass": True, "output": str(Path(args.output).resolve()), "nodes": len(scene["nodes"]), "relations": len(scene["relations"]), "anchors": len(scene["anchors"]), "galaxies": len(scene["galaxies"])}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

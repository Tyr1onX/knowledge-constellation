#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

WORLD_WIDTH = 1000
WORLD_HEIGHT = 720
CORE_CLEARANCE = 150

# Quality-gated silhouettes. They describe bounded macro structure only; exact
# node placement still comes from the accepted personal model and d3 physics.
# Every preset keeps the Identity Core's center clear.
ARCHETYPE_POINTS = {
    "dominant_core_satellites": [(0.26, 0.31), (0.73, 0.28), (0.79, 0.61), (0.29, 0.69), (0.51, 0.82), (0.49, 0.16)],
    "dual_core": [(0.28, 0.34), (0.72, 0.39), (0.23, 0.69), (0.78, 0.70), (0.49, 0.82), (0.52, 0.16)],
    "three_islands": [(0.27, 0.34), (0.73, 0.36), (0.50, 0.78), (0.18, 0.69), (0.82, 0.70), (0.50, 0.15)],
    "stream": [(0.18, 0.30), (0.34, 0.23), (0.66, 0.27), (0.81, 0.43), (0.70, 0.70), (0.42, 0.78)],
    "sparse_archipelago": [(0.19, 0.27), (0.75, 0.23), (0.82, 0.66), (0.38, 0.77), (0.18, 0.63), (0.57, 0.16)],
    "compact_cluster": [(0.35, 0.27), (0.65, 0.29), (0.71, 0.61), (0.35, 0.67), (0.50, 0.78), (0.50, 0.16)],
    # A bent chain around the Core, never a straight line through it.
    "asymmetric_chain": [(0.20, 0.30), (0.38, 0.21), (0.67, 0.28), (0.81, 0.47), (0.67, 0.70), (0.38, 0.76)],
}

REP_SIZE = {"low": 0.36, "medium": 0.58, "high": 0.79}
RELATION_STYLE = {
    "co_occurrence": (118, 0.10),
    "repeated_context": (102, 0.16),
    "trajectory": (132, 0.12),
    "practice": (94, 0.14),
}
GALAXY_COLORS = [
    [171, 201, 235],
    [213, 190, 232],
    [178, 222, 214],
    [225, 199, 176],
    [190, 207, 239],
    [207, 194, 226],
]
MORPHOLOGY_SPREAD = {
    "compact": 0.76,
    "elongated": 1.08,
    "stream": 1.16,
    "cloud": 1.00,
    "ring": 1.08,
    "fragmented": 1.22,
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


def _push_from_core(x, y, width, height, clearance=CORE_CLEARANCE):
    cx, cy = width / 2, height / 2
    dx, dy = x - cx, y - cy
    dist = math.hypot(dx, dy)
    if dist >= clearance:
        return x, y
    if dist < 1e-6:
        dx, dy, dist = 1.0, 0.0, 1.0
    scale = clearance / dist
    return cx + dx * scale, cy + dy * scale


def _adjust_norm_point(point, visual, seed, index):
    x, y = point
    dx, dy = x - 0.5, y - 0.5
    openness = clamp(visual.get("composition", {}).get("openness", 0.5), 0, 1)
    asymmetry = clamp(visual.get("composition", {}).get("asymmetry", 0.5), 0, 1)
    axis = visual.get("composition", {}).get("dominant_axis", "none")

    # Openness affects spacing, but only inside a narrow quality-gated band.
    radial = 0.92 + openness * 0.18
    dx *= radial
    dy *= radial

    if axis == "horizontal":
        dx *= 1.07
        dy *= 0.95
    elif axis == "vertical":
        dx *= 0.95
        dy *= 1.07
    elif axis == "diagonal":
        # Subtle skew rather than a literal diagonal line.
        dx2 = dx + dy * 0.07
        dy2 = dy + dx * 0.04
        dx, dy = dx2, dy2
    elif axis == "radial":
        dx *= 1.035
        dy *= 1.035

    jitter = 0.024 * asymmetry
    dx += (stable01(f"{seed}|layout-jx|{index}") - 0.5) * jitter
    dy += (stable01(f"{seed}|layout-jy|{index}") - 0.5) * jitter
    return 0.5 + dx, 0.5 + dy


def galaxy_centers(visual, structure, width=WORLD_WIDTH, height=WORLD_HEIGHT):
    galaxies = structure.get("galaxies", [])
    count = len(galaxies)
    archetype = visual.get("composition", {}).get("archetype", "sparse_archipelago")
    points = list(ARCHETYPE_POINTS.get(archetype, ARCHETYPE_POINTS["sparse_archipelago"]))
    seed = visual.get("seed", "knowledge-constellation")

    if count == 1:
        points = [(0.34, 0.45)]
    elif count == 2:
        points = [(0.28, 0.38), (0.72, 0.42)]

    while len(points) < count:
        i = len(points)
        angle = i * 2.399963229728653 + stable01(f"{seed}|galaxy-angle|{i}") * 0.42
        radius = 0.30 + 0.08 * stable01(f"{seed}|galaxy-radius|{i}")
        points.append((0.5 + math.cos(angle) * radius, 0.5 + math.sin(angle) * radius))

    visual_by_id = {g["id"]: g for g in visual.get("galaxies", [])}
    result = {}
    for i, g in enumerate(galaxies):
        nx, ny = _adjust_norm_point(points[i], visual, seed, i)
        mass = visual_by_id.get(g["id"], {}).get("mass", 0.5)
        pad = 0.10 + (1 - mass) * 0.015
        x = clamp(nx, pad, 1 - pad) * width
        y = clamp(ny, pad, 1 - pad) * height
        x, y = _push_from_core(x, y, width, height)
        result[g["id"]] = {"x": round(x, 3), "y": round(y, 3)}
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


def initial_node_point(seed, node_id, galaxy_center, layer, primary_index, morphology="cloud", openness=0.5):
    jitter = stable01(f"{seed}|node-jitter|{node_id}")
    angle = stable01(f"{seed}|node-angle|{node_id}") * math.tau
    radius = 26 + (primary_index or 0) * 19 + jitter * 28 if layer == "primary" else 66 + jitter * 88
    radius *= MORPHOLOGY_SPREAD.get(morphology, 1.0)
    radius *= 0.92 + clamp(openness, 0, 1) * 0.12
    dx, dy = math.cos(angle) * radius, math.sin(angle) * radius
    if morphology in {"elongated", "stream"}:
        dx *= 1.20
        dy *= 0.82
    return {"x": round(galaxy_center["x"] + dx, 3), "y": round(galaxy_center["y"] + dy, 3)}


def compose_scene(input_data, evidence_data, model, structure, visual):
    centers = galaxy_centers(visual, structure)
    membership = node_membership(structure)
    model_nodes = {n["id"]: n for n in model.get("nodes", [])}
    evidence = {e["id"]: e for e in evidence_data.get("evidence", [])}
    anchors = {a["id"]: a for a in structure.get("anchors", [])}
    visual_anchors = {a["id"]: a for a in visual.get("anchors", [])}
    source_titles = {s["id"]: s.get("title", s["id"]) for s in input_data.get("sources", [])}
    visual_galaxies = {g["id"]: g for g in visual.get("galaxies", [])}
    seed = visual["seed"]
    openness = visual.get("composition", {}).get("openness", 0.5)

    scene_nodes = []
    for nid, node in model_nodes.items():
        member = membership[nid]
        vg = visual_galaxies.get(member["galaxy"], {})
        point = initial_node_point(seed, nid, centers[member["galaxy"]], member["layer"], member["primary_index"], vg.get("morphology", "cloud"), openness)
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
    scene_galaxies = []
    for i, (gid, g) in enumerate(structure_galaxies.items()):
        vg = visual_galaxies[gid]
        center = centers[gid]
        scene_galaxies.append({
            "id": gid,
            "name": g["label"],
            "x": center["x"],
            "y": center["y"],
            "mass": vg["mass"],
            "morphology": vg["morphology"],
            "dominance": vg["dominance"],
            "anchor": g["anchor"],
            "primary_nodes": g.get("primary_nodes", []),
            "secondary_nodes": g.get("secondary_nodes", []),
            "color": GALAXY_COLORS[i % len(GALAXY_COLORS)],
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
        radius = 42 + stable01(f"{seed}|anchor-radius|{anchor['id']}") * 28
        scene_anchors.append({
            "id": anchor["id"],
            "name": anchor["label"],
            "kind": anchor["kind"],
            "nodes": anchor.get("nodes", []),
            "galaxies": galaxies,
            "g": galaxies[0] if galaxies else None,
            "role": va["role"],
            "prominence": va["prominence"],
            "x": round(avg_x + math.cos(angle) * radius, 3),
            "y": round(avg_y + math.sin(angle) * radius, 3),
            "phaseOffset": i,
        })

    subject = input_data["subject"]
    identity = dict(visual["identity"])
    identity["title"] = subject["label"]
    identity["subtitle"] = identity.get("presence", {}).get("subtitle") or "由作品、经历与学习痕迹生长出的知识星图"
    identity["source"] = subject.get("scope") or "Knowledge Constellation"
    identity["x"] = WORLD_WIDTH / 2
    identity["y"] = WORLD_HEIGHT / 2

    return {
        "version": "kc.scene.v1",
        "seed": seed,
        "subject": {"id": subject["id"], "label": subject["label"], "language": subject.get("language"), "scope": subject.get("scope")},
        "viewport": {"width": WORLD_WIDTH, "height": WORLD_HEIGHT},
        "identity": identity,
        "composition": visual["composition"],
        "field": visual["field"],
        "stars": visual["stars"],
        "motion": visual["motion"],
        "nodes": scene_nodes,
        "relations": scene_relations,
        "anchors": scene_anchors,
        "galaxies": scene_galaxies,
        "motifs": structure.get("motifs", []),
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
    cx, cy = scene["viewport"]["width"] / 2, scene["viewport"]["height"] / 2
    for galaxy in scene.get("galaxies", []):
        if math.hypot(galaxy["x"] - cx, galaxy["y"] - cy) < CORE_CLEARANCE - 1:
            errors.append(f"galaxy {galaxy['id']} violates Identity Core clearance")
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

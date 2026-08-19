#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser(description="Verify a generated Knowledge Constellation delivery belongs to the current run rather than a repository preview/showcase.")
    ap.add_argument("--input", required=True, help="Accepted current-run input.json")
    ap.add_argument("--dist", required=True, help="Generated site directory")
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    dist = Path(args.dist).resolve()
    errors = []

    scene_path = dist / "scene.json"
    index_path = dist / "index.html"
    share_path = dist / "share.html"
    manifest_path = dist / "manifest.json"

    for path in [scene_path, index_path, share_path, manifest_path]:
        if not path.exists():
            errors.append(f"missing generated artifact: {path.name}")

    if errors:
        print(json.dumps({"pass": False, "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    accepted_input = read_json(input_path)
    scene = read_json(scene_path)
    manifest = read_json(manifest_path)
    subject_id = accepted_input.get("subject", {}).get("id")
    if scene.get("subject", {}).get("id") != subject_id:
        errors.append("generated scene subject.id must match accepted current-run input subject.id")

    index = index_path.read_text(encoding="utf-8")
    share = share_path.read_text(encoding="utf-8")
    for name, text in [("index.html", index), ("share.html", share)]:
        lowered = text.lower()
        if "preview/scene.json" in lowered:
            errors.append(f"{name} must not load repository preview/scene.json")
        if "<svg" in lowered:
            errors.append(f"{name} must not replace the canonical renderer with an SVG graph")

    if "window.__KC_SCENE__" not in share:
        errors.append("share.html must embed the current-run Scene")

    if manifest.get("scene") != "scene.json":
        errors.append("manifest.scene must point to the current-run scene.json")
    if manifest.get("renderer_contract") != "canonical-runtime":
        errors.append("manifest.renderer_contract must remain canonical-runtime")

    result = {"pass": not errors, "errors": errors, "subject_id": subject_id}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()

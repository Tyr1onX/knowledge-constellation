#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "renderer"


def main():
    ap = argparse.ArgumentParser(description="Build a portable Knowledge Constellation v0.1 site directory.")
    ap.add_argument("--scene", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    scene = Path(args.scene).resolve()
    output = Path(args.output).resolve()
    renderer_out = output / "renderer"
    output.mkdir(parents=True, exist_ok=True)
    renderer_out.mkdir(parents=True, exist_ok=True)

    target_scene = output / "scene.json"
    if scene != target_scene:
        shutil.copy2(scene, target_scene)

    shutil.copy2(RENDERER / "index.template.html", output / "index.html")
    copied = []
    for source in sorted(RENDERER.glob("*.js")):
        shutil.copy2(source, renderer_out / source.name)
        copied.append(source.name)

    manifest = {
        "version": "kc.site.v0.1",
        "scene": "scene.json",
        "entry": "index.html",
        "renderer_modules": copied,
        "note": "Serve this directory over HTTP. index.html loads scene.json and the canonical renderer modules.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": True, "output": str(output), "entry": str(output / "index.html"), "scene": str(target_scene), "renderer_modules": len(copied)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

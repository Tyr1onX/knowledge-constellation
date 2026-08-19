#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "renderer"
CANONICAL_REPO = "Tyr1onX/knowledge-constellation"
D3_URL = "https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"


def detect_renderer_ref(explicit=None):
    if explicit:
        return explicit
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        ref = proc.stdout.strip()
        if re.fullmatch(r"[0-9a-f]{40}", ref):
            return ref
    except Exception:
        pass
    return "main"


def canonical_asset_url(renderer_ref, path):
    return f"https://cdn.jsdelivr.net/gh/{CANONICAL_REPO}@{renderer_ref}/renderer/{path}"


def github_profile_url(scene):
    subject = scene.get("subject", {})
    scope = str(subject.get("scope") or "")
    subject_id = str(subject.get("id") or "")
    if "github" not in scope.lower():
        return None
    if not re.fullmatch(r"[A-Za-z0-9-]+", subject_id):
        return None
    return f"https://github.com/{subject_id}"


def build_share_html(scene, renderer_ref):
    subject = scene.get("subject", {})
    identity = scene.get("identity", {})
    title = str(subject.get("label") or identity.get("title") or identity.get("label") or "Knowledge Constellation")
    scope = str(subject.get("scope") or identity.get("source") or "Knowledge Constellation")
    profile = github_profile_url(scene)
    repo_link = ""
    if profile:
        repo_link = f'\n  <a class="preview-repo" href="{html.escape(profile, quote=True)}" target="_blank" rel="noreferrer">查看 GitHub ↗</a>'

    scene_json = json.dumps(scene, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    css_url = canonical_asset_url(renderer_ref, "shell.css")
    runtime_url = canonical_asset_url(renderer_ref, "runtime.js")
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="dark">
  <title>{html.escape(title)} — Knowledge Constellation</title>
  <link rel="stylesheet" href="{html.escape(css_url, quote=True)}">
</head>
<body>
  <canvas id="universe" aria-label="{html.escape(title, quote=True)} Interactive Knowledge Constellation"></canvas>
  <div class="preview-brand"><b>{html.escape(title.upper())}</b><span>{html.escape(scope)}</span></div>
  <div class="preview-hint">拖动空间 · 拖动星体 · 滚轮缩放 · 点击 Project Anchor 进入 Galaxy · 点击中心返回全景</div>{repo_link}
  <div id="fatal" hidden></div>
  <div class="tooltip" id="tooltip"><strong id="tooltip-title"></strong><small id="tooltip-subtitle"></small></div>
  <aside class="detail-card" id="detail-card">
    <button class="close" id="detail-close" aria-label="关闭">×</button>
    <div class="galaxy" id="detail-galaxy"></div>
    <h2 id="detail-title"></h2>
    <div class="subtitle" id="detail-subtitle"></div>
    <div class="project-row" id="detail-project-row"><span id="detail-project"></span></div>
    <p class="summary" id="detail-summary"></p>
    <div class="related-block" id="detail-related-block"><div class="section-label">相关</div><div class="related-list" id="detail-related"></div></div>
    <details id="detail-disclosure"><summary id="detail-evidence-label">查看依据</summary><div class="evidence-body"><div id="detail-evidence"></div><div class="sources" id="detail-sources"></div><p class="footnote" id="detail-evidence-footnote"></p></div></details>
  </aside>
  <script>window.__KC_SCENE__ = {scene_json};</script>
  <script src="{D3_URL}"></script>
  <script type="module" src="{html.escape(runtime_url, quote=True)}"></script>
</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser(description="Build a portable Knowledge Constellation v0.1 site directory.")
    ap.add_argument("--scene", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--renderer-ref", help="Commit/tag used by share.html for canonical CDN renderer assets. Defaults to the current git HEAD, then main if unavailable.")
    args = ap.parse_args()

    scene = Path(args.scene).resolve()
    output = Path(args.output).resolve()
    renderer_out = output / "renderer"
    output.mkdir(parents=True, exist_ok=True)
    renderer_out.mkdir(parents=True, exist_ok=True)

    target_scene = output / "scene.json"
    if scene != target_scene:
        shutil.copy2(scene, target_scene)

    scene_data = json.loads(target_scene.read_text(encoding="utf-8"))
    shutil.copy2(RENDERER / "index.template.html", output / "index.html")

    copied_modules = []
    copied_assets = []
    for source in sorted(RENDERER.iterdir()):
        if not source.is_file() or source.name in {"index.template.html", "README.md"}:
            continue
        if source.suffix not in {".js", ".css"}:
            continue
        shutil.copy2(source, renderer_out / source.name)
        copied_assets.append(source.name)
        if source.suffix == ".js":
            copied_modules.append(source.name)

    renderer_ref = detect_renderer_ref(args.renderer_ref)
    share_entry = output / "share.html"
    share_entry.write_text(build_share_html(scene_data, renderer_ref), encoding="utf-8")

    manifest = {
        "version": "kc.site.v0.1",
        "scene": "scene.json",
        "entry": "index.html",
        "share_entry": "share.html",
        "renderer_modules": copied_modules,
        "renderer_assets": copied_assets,
        "renderer_contract": "canonical-runtime",
        "share_renderer_ref": renderer_ref,
        "share_requires_network": True,
        "note": "index.html is the fully local site entry and should be served over HTTP. share.html is a one-file share wrapper that embeds the accepted Scene and loads the same canonical renderer from a pinned CDN ref; it must not reimplement the visualization.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "pass": True,
        "output": str(output),
        "entry": str(output / "index.html"),
        "share": str(share_entry),
        "scene": str(target_scene),
        "renderer_ref": renderer_ref,
        "renderer_modules": len(copied_modules),
        "renderer_assets": len(copied_assets),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "harness" / "verify_delivery.py"


class DeliveryGuardTests(unittest.TestCase):
    def write_fixture(self, root: Path, *, preview_ref=False):
        input_path = root / "input.json"
        dist = root / "dist"
        dist.mkdir()
        input_path.write_text(json.dumps({
            "subject": {"id": "alice", "label": "Alice"},
            "sources": [{"id": "S1", "kind": "profile", "title": "Alice", "content": "example"}],
        }), encoding="utf-8")
        (dist / "scene.json").write_text(json.dumps({"subject": {"id": "alice"}}), encoding="utf-8")
        index = '<html data-kc-scene="./scene.json"></html>'
        if preview_ref:
            index = '<html data-kc-scene="https://example.invalid/preview/scene.json"></html>'
        (dist / "index.html").write_text(index, encoding="utf-8")
        (dist / "share.html").write_text('<script>window.__KC_SCENE__ = {"subject":{"id":"alice"}}</script>', encoding="utf-8")
        (dist / "manifest.json").write_text(json.dumps({
            "scene": "scene.json",
            "renderer_contract": "canonical-runtime",
        }), encoding="utf-8")
        return input_path, dist

    def run_verify(self, input_path, dist):
        return subprocess.run([
            sys.executable, str(VERIFY),
            "--input", str(input_path),
            "--dist", str(dist),
        ], cwd=ROOT, capture_output=True, text=True)

    def test_accepts_current_run_scene_delivery(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, dist = self.write_fixture(Path(td))
            proc = self.run_verify(input_path, dist)
            self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)

    def test_rejects_repository_preview_scene_reference(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, dist = self.write_fixture(Path(td), preview_ref=True)
            proc = self.run_verify(input_path, dist)
            self.assertNotEqual(0, proc.returncode)
            self.assertIn("preview/scene.json", proc.stdout)

    def test_skill_forbids_demo_scene_reuse(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Repository preview is demo-only", skill)
        self.assertIn("reusing a previous subject Scene is forbidden", skill)
        self.assertIn("accepted `target.json`, `gap.json`, and `plan.json`", skill)


if __name__ == "__main__":
    unittest.main()

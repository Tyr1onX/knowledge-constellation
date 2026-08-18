import json
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2E = ROOT / "harness" / "e2e.py"
CASE = ROOT / "evals" / "clean-room" / "cases" / "2026-08-18-simonw-02"


def input_from_manifest(manifest):
    sources = []
    for source in manifest["sources"]:
        sources.append({
            "id": source["id"],
            "kind": source.get("kind", "frozen_source"),
            "title": source.get("title") or source.get("repo") or source.get("url") or source["id"],
            "content": source.get("observation") or source.get("frozen_excerpt") or "frozen source",
        })
    return {"subject": manifest["subject"], "sources": sources}


class RealCaseE2EReplayTests(unittest.TestCase):
    def test_simonw_accepted_case_reaches_canonical_runtime_without_scene_repair(self):
        manifest = json.loads((CASE / "source-manifest.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            input_path = temp / "input.json"
            run_dir = temp / "run"
            dist_dir = temp / "dist"
            runner = temp / "replay_runner.py"
            input_path.write_text(json.dumps(input_from_manifest(manifest), ensure_ascii=False), encoding="utf-8")

            fixture_dir = CASE / "runner"
            runner.write_text(textwrap.dedent(f'''
                import os
                from pathlib import Path

                stage_files = {{
                    "evidence": "pass-a.json",
                    "model": "pass-b.json",
                    "structure": "pass-c.json",
                    "visual": "pass-d.json",
                }}
                fixture = Path({str(fixture_dir)!r}) / stage_files[os.environ["KC_STAGE"]]
                Path(os.environ["KC_OUTPUT"]).write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
            '''), encoding="utf-8")

            runner_command = f"{shlex.quote(sys.executable)} {shlex.quote(str(runner))}"
            proc = subprocess.run([
                sys.executable, str(E2E),
                "--input", str(input_path),
                "--run", str(run_dir),
                "--dist", str(dist_dir),
                "--runner-command", runner_command,
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)

            scene = json.loads((dist_dir / "scene.json").read_text(encoding="utf-8"))
            self.assertEqual("kc.scene.v1", scene["version"])
            self.assertEqual("Simon Willison", scene["identity"]["label"])
            self.assertEqual(6, len(scene["nodes"]))
            self.assertEqual(5, len(scene["relations"]))
            self.assertEqual(3, len(scene["anchors"]))
            self.assertEqual(3, len(scene["galaxies"]))
            self.assertEqual({"Datasette", "sqlite-utils", "LLM"}, {anchor["name"] for anchor in scene["anchors"]})
            self.assertTrue((dist_dir / "renderer" / "runtime.js").exists())
            self.assertTrue((dist_dir / "index.html").exists())


if __name__ == "__main__":
    unittest.main()

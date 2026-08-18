import json
import os
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2E = ROOT / "harness" / "e2e.py"


class E2ESmokeTests(unittest.TestCase):
    def test_one_command_reaches_scene_and_site(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            input_path = temp / "input.json"
            run_dir = temp / "run"
            dist_dir = temp / "dist"
            fake_runner = temp / "fake_runner.py"

            input_path.write_text(json.dumps({
                "subject": {"id": "smoke", "label": "Smoke User", "language": "zh-CN", "scope": "test"},
                "sources": [{"id": "S1", "kind": "project", "title": "Smoke Project", "content": "A bounded project artifact exists."}],
            }), encoding="utf-8")

            fake_runner.write_text(textwrap.dedent(r'''
                import json
                import os
                from pathlib import Path

                stage = os.environ["KC_STAGE"]
                payloads = {
                    "evidence": {
                        "evidence": [{
                            "id": "E1", "source_ids": ["S1"], "kind": "artifact",
                            "observation": "A bounded project artifact exists.",
                            "confidence": "high", "attribution": "uncertain",
                            "supports": ["project exposure"],
                            "does_not_support": ["independent mastery"],
                            "correlation_group": "smoke-artifact"
                        }]
                    },
                    "model": {
                        "claims": [{
                            "id": "C1", "subject": "N1", "dimension": "exposure",
                            "value": "supported", "confidence": "high", "evidence": ["E1"],
                            "boundary": "The artifact does not establish independence."
                        }],
                        "nodes": [{
                            "id": "N1", "label": "Smoke project exposure", "english_label": "Smoke project exposure",
                            "state": "observed", "confidence": "high", "resolution": "medium",
                            "representativeness": "high", "activity": "unknown", "claims": ["C1"], "evidence": ["E1"],
                            "summary": "A bounded project-level exposure is visible.",
                            "known": ["The project artifact exists."],
                            "unknown": ["Independent implementation depth."],
                            "reason": "The source directly supports project exposure.",
                            "boundary": ["Artifact is not mastery."],
                            "next_step": {"title": "More evidence", "text": "Look for independent action evidence."}
                        }],
                        "unresolved": []
                    },
                    "structure": {
                        "anchors": [{"id": "A1", "kind": "project", "label": "Smoke Project", "nodes": ["N1"]}],
                        "relations": [], "motifs": [],
                        "galaxies": [{"id": "G1", "label": "Smoke Project practice", "anchor": "A1", "primary_nodes": ["N1"], "secondary_nodes": []}],
                        "distillation": {"primary_nodes": ["N1"], "secondary_nodes": []}
                    },
                    "visual": {
                        "seed": "kc:smoke:v1",
                        "identity": {"family": "quiet_star", "label": "Smoke User", "monogram": None, "avatar": None, "presence": {"mode": "brief_intro", "subtitle": "A bounded knowledge universe"}},
                        "composition": {"archetype": "sparse_archipelago", "asymmetry": 0.2, "openness": 0.8, "dominant_axis": "none"},
                        "field": {"density": "very_sparse", "dust_family": "almost_empty", "temperature_bias": "neutral"},
                        "stars": {"family": "subtle_point", "temperature_variation": "low"},
                        "motion": {"temperament": "quiet"},
                        "anchors": [{"id": "A1", "role": "provenance", "prominence": "low", "galaxies": ["G1"]}],
                        "galaxies": [{"id": "G1", "mass": 0.4, "morphology": "compact", "dominance": 0.6}]
                    }
                }
                Path(os.environ["KC_OUTPUT"]).write_text(json.dumps(payloads[stage]), encoding="utf-8")
            '''), encoding="utf-8")

            runner_command = f"{shlex.quote(sys.executable)} {shlex.quote(str(fake_runner))}"
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
            self.assertEqual(["N1"], [node["id"] for node in scene["nodes"]])
            self.assertTrue((dist_dir / "index.html").exists())
            self.assertTrue((dist_dir / "manifest.json").exists())
            self.assertTrue((dist_dir / "renderer" / "runtime.js").exists())
            self.assertEqual("complete", json.loads((run_dir / "state.json").read_text(encoding="utf-8"))["status"])


if __name__ == "__main__":
    unittest.main()

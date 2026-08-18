import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "harness" / "validate.py"
SCHEMA = ROOT / "contracts" / "structure.schema.json"


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class SparseStructureTests(unittest.TestCase):
    def test_truthful_one_node_galaxy_is_valid(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            evidence = td / "evidence.json"
            model = td / "model.json"
            structure = td / "structure.json"

            dump(evidence, {
                "evidence": [{
                    "id": "E1",
                    "source_ids": ["S1"],
                    "kind": "artifact",
                    "observation": "One isolated but representative project theme is evidenced.",
                    "confidence": "high",
                    "attribution": "direct",
                    "supports": ["one representative theme"],
                    "does_not_support": ["a fabricated second theme"],
                }]
            })
            dump(model, {
                "nodes": [{"id": "N1"}]
            })
            dump(structure, {
                "anchors": [{"id": "A1", "kind": "project", "label": "One Project", "nodes": ["N1"]}],
                "relations": [],
                "motifs": [],
                "galaxies": [{
                    "id": "G1",
                    "label": "One real project theme",
                    "anchor": "A1",
                    "primary_nodes": ["N1"],
                    "secondary_nodes": [],
                }],
                "distillation": {"primary_nodes": ["N1"], "secondary_nodes": []},
            })

            proc = subprocess.run([
                sys.executable, str(VALIDATE),
                "--stage", "structure",
                "--file", str(structure),
                "--schema", str(SCHEMA),
                "--evidence", str(evidence),
                "--model", str(model),
            ], capture_output=True, text=True)
            self.assertEqual(0, proc.returncode, proc.stdout + "\n" + proc.stderr)
            self.assertTrue(json.loads(proc.stdout)["pass"])

    def test_skill_forbids_fabricated_companion_nodes(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        prompt = (ROOT / "prompts" / "pass-c-structure.md").read_text(encoding="utf-8")
        self.assertIn("one-node Galaxy", skill)
        self.assertIn("one-node Galaxies", prompt)
        self.assertIn("Never fabricate a companion node", skill)


if __name__ == "__main__":
    unittest.main()

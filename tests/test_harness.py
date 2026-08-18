import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "harness" / "pipeline.py"


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


INPUT = {
    "subject": {
        "id": "case-x",
        "label": "Case X",
        "language": "en",
        "scope": "software-development",
    },
    "sources": [
        {
            "id": "S1",
            "kind": "project",
            "title": "Project Atlas",
            "content": "Maintained project with documented test runs.",
        }
    ],
}

EVIDENCE = {
    "evidence": [
        {
            "id": "E1",
            "source_ids": ["S1"],
            "kind": "artifact",
            "observation": "A maintained project with documented test runs exists.",
            "confidence": "high",
            "attribution": "uncertain",
            "supports": ["project-practice"],
            "does_not_support": ["independent-implementation"],
            "correlation_group": "atlas",
        }
    ]
}


class HarnessTests(unittest.TestCase):
    def run_cmd(self, *args, expected=0):
        proc = subprocess.run(
            [sys.executable, str(PIPELINE), *args],
            capture_output=True,
            text=True,
        )
        self.assertEqual(expected, proc.returncode, proc.stdout + "\n" + proc.stderr)
        return json.loads(proc.stdout)

    def test_architecture_boundary(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        validator = (ROOT / "harness" / "validate.py").read_text(encoding="utf-8")
        pipeline = (ROOT / "harness" / "pipeline.py").read_text(encoding="utf-8")
        self.assertIn("You are the semantic engine", skill)
        for forbidden in ["synthesize_nodes", "build_evidence", "keyword_catalog"]:
            self.assertNotIn(forbidden, validator)
        self.assertIn("forbidden_runtime_inputs", pipeline)
        self.assertNotIn("cmd_render", pipeline)

    def test_recognition_hardening_contracts_are_executable(self):
        model_schema = json.loads((ROOT / "contracts" / "model.schema.json").read_text(encoding="utf-8"))
        structure_schema = json.loads((ROOT / "contracts" / "structure.schema.json").read_text(encoding="utf-8"))
        visual_schema = json.loads((ROOT / "contracts" / "visual.schema.json").read_text(encoding="utf-8"))
        pipeline = (ROOT / "harness" / "pipeline.py").read_text(encoding="utf-8")
        validator = (ROOT / "harness" / "validate.py").read_text(encoding="utf-8")

        claim_schema = model_schema["properties"]["claims"]["items"]
        self.assertIn("attribution_evidence", claim_schema["properties"])
        self.assertIn("motifs", structure_schema["required"])
        relation_schema = structure_schema["properties"]["relations"]["items"]
        self.assertIn("temporal_basis", relation_schema["properties"])
        self.assertIn("anchors", visual_schema["required"])
        self.assertIn("presence", visual_schema["properties"]["identity"]["required"])
        self.assertIn('"needs": ["input", "model", "structure"]', pipeline)
        self.assertIn("action-bearing claim requires explicit attribution_evidence", validator)
        self.assertIn("visual anchors must exactly match accepted structure anchors", validator)
        self.assertIn("trajectory requires earlier and later evidence", validator)

    def test_isolated_evidence_pass_and_repair(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            inp = td / "input.json"
            run = td / "run"
            dump(inp, INPUT)

            self.run_cmd("init", "--input", str(inp), "--run", str(run))
            packet = self.run_cmd("next", "--run", str(run))
            ws = Path(packet["workspace"])
            self.assertEqual(
                {"SKILL.md", "ORCHESTRATION.md", "PROMPT.md", "schema.json", "input.json", "TASK.md"},
                {p.name for p in ws.iterdir()},
            )

            broken = json.loads(json.dumps(EVIDENCE))
            broken["evidence"][0]["does_not_support"] = []
            dump(Path(packet["files"]["output"]), broken)
            rejected = self.run_cmd("validate", "--run", str(run), expected=1)
            self.assertFalse(rejected["pass"])

            repair = self.run_cmd("next", "--run", str(run))
            self.assertEqual("repair", repair["mode"])
            dump(Path(repair["files"]["output"]), EVIDENCE)
            accepted = self.run_cmd("validate", "--run", str(run))
            self.assertTrue(accepted["pass"])
            self.assertEqual("model", accepted["next"])


if __name__ == "__main__":
    unittest.main()

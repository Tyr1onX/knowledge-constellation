import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCENE_PATH = ROOT / "preview" / "scene.json"
SCHEMA_PATH = ROOT / "contracts" / "scene.schema.json"


class BlindVisualBaselineTests(unittest.TestCase):
    def load_scene(self):
        return json.loads(SCENE_PATH.read_text(encoding="utf-8"))

    def test_accepted_blind_scene_matches_active_scene_contract(self):
        scene = self.load_scene()
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(scene), key=lambda error: list(error.path))
        self.assertEqual([], [error.message for error in errors])

    def test_accepted_blind_scene_checkpoint_is_not_silently_replaced(self):
        scene = self.load_scene()
        self.assertEqual("kc.scene.v1", scene["version"])
        self.assertEqual("kc:Tyr1onX:github:2026-08-19:v1", scene["seed"])
        self.assertEqual("Tyr1onX", scene["subject"]["id"])
        self.assertEqual("栖白 · Tyr1onX", scene["subject"]["label"])
        self.assertEqual(29, len(scene["nodes"]))
        self.assertEqual(29, len(scene["relations"]))
        self.assertEqual(6, len(scene["anchors"]))
        self.assertEqual(5, len(scene["galaxies"]))

    def test_accepted_blind_scene_keeps_evidence_disclosure_material(self):
        scene = self.load_scene()
        for node in scene["nodes"]:
            self.assertTrue(node["evidence"], node["id"])
            self.assertTrue(node["sources"], node["id"])


if __name__ == "__main__":
    unittest.main()

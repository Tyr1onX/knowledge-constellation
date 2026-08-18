import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class E2EContractTests(unittest.TestCase):
    def test_e2e_orchestrator_keeps_semantic_work_external(self):
        text = (ROOT / "harness" / "e2e.py").read_text(encoding="utf-8")
        self.assertIn("--runner-command", text); self.assertIn("KC_OUTPUT", text); self.assertIn("pipeline.py", text); self.assertIn("compose_scene.py", text)
        self.assertNotIn("Rust", text); self.assertNotIn("React", text); self.assertNotIn("keyword", text.lower())

    def test_site_runtime_uses_canonical_renderer_modules(self):
        text = (ROOT / "renderer" / "runtime.js").read_text(encoding="utf-8")
        for token in ["createKnowledgeSimulation", "drawKnowledgeStar", "computeOverviewVisibilityPlan", "nodeSemanticVisibility", "drawIdentityCore", "drawIdentityPresence", "drawProjectAnchor", "buildNodeDetailModel", "drawBackgroundField"]:
            self.assertIn(token, text)
        self.assertNotIn("secondaryLayerVisibility(", text)

    def test_scene_contract_is_versioned(self):
        schema = json.loads((ROOT / "contracts" / "scene.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("kc.scene.v1", schema["properties"]["version"]["const"])
        self.assertIn("anchors", schema["required"]); self.assertIn("nodes", schema["required"]); self.assertIn("relations", schema["required"])

    def test_product_surface_template_has_no_audit_chrome(self):
        html = (ROOT / "renderer" / "index.template.html").read_text(encoding="utf-8")
        for forbidden in ["可靠度", "已观察", "仍然模糊", "下一步"]:
            self.assertNotIn(forbidden, html)
        self.assertIn("查看依据", html); self.assertIn("detail-project", html)


if __name__ == "__main__":
    unittest.main()

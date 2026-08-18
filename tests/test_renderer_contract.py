import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RendererContractTests(unittest.TestCase):
    def test_generated_runtime_keeps_page_level_visual_baseline(self):
        runtime = (ROOT / "renderer" / "runtime.js").read_text(encoding="utf-8")
        required = [
            "RUNTIME_BASELINE",
            "function sceneScale()",
            "function cameraForWorld",
            "function tickCamera",
            "createAmbientMeteor",
            "drawAmbientMeteor",
            "drawProjectProvenanceLinks",
            "primaryLabelRevealScale",
            "faintGalaxyLabelsAtOverview",
            "galaxyFocusScale",
        ]
        for token in required:
            self.assertIn(token, runtime)

    def test_site_template_uses_canonical_shell_and_runtime(self):
        template = (ROOT / "renderer" / "index.template.html").read_text(encoding="utf-8")
        self.assertIn('./renderer/shell.css', template)
        self.assertIn('./renderer/runtime.js', template)
        self.assertNotIn('<svg', template.lower())
        self.assertNotIn('drawKnowledgeStar(', template)

    def test_repository_preview_uses_same_runtime(self):
        preview = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-kc-scene="./preview/scene.json"', preview)
        self.assertIn('./renderer/shell.css', preview)
        self.assertIn('./renderer/runtime.js', preview)
        self.assertNotIn('function drawLinks', preview)
        self.assertNotIn('drawKnowledgeStar(', preview)

    def test_no_handcrafted_svg_exporter_is_part_of_runtime(self):
        for path in (ROOT / "harness").glob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertNotIn('<svg', text, path.name)


if __name__ == "__main__":
    unittest.main()

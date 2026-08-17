import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "renderer"


class RendererContractTests(unittest.TestCase):
    def test_renderer_baseline_is_versioned(self):
        for name in ["README.md", "physics.js", "star-renderer.js", "semantic-zoom.js", "index.js"]:
            self.assertTrue((RENDERER / name).is_file(), name)

    def test_d3_force_baseline_cannot_silently_disappear(self):
        text = (RENDERER / "physics.js").read_text(encoding="utf-8")
        for token in [
            "d3.forceSimulation",
            "d3.forceLink",
            "d3.forceManyBody",
            "d3.forceCollide",
            "d3.forceX",
            "d3.forceY",
            "alphaDecay: 0.024",
            "velocityDecay: 0.24",
            "dragAlphaTarget: 0.20",
        ]:
            self.assertIn(token, text)

    def test_point_light_star_baseline_cannot_be_replaced_by_generic_dot(self):
        text = (RENDERER / "star-renderer.js").read_text(encoding="utf-8")
        for token in [
            "drawKnowledgeStar",
            "elliptical halo",
            "point source first",
            "Tiny overexposed pinprick",
            "incomplete whisper arc",
        ]:
            self.assertIn(token, text)

    def test_semantic_zoom_preserves_camera_invariants(self):
        text = (RENDERER / "semantic-zoom.js").read_text(encoding="utf-8")
        for token in [
            "inspectNodeRecenters: false",
            "zoomOutRecenters: false",
            "identityCoreOwnsReset: true",
            "secondaryRevealStart: 1.22",
            "detailExitScale: 1.43",
            "galaxyExitScale: 1.12",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()

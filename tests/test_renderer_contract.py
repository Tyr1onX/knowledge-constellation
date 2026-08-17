import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "renderer"


class RendererContractTests(unittest.TestCase):
    def test_renderer_baseline_is_versioned(self):
        for name in [
            "README.md",
            "physics.js",
            "star-renderer.js",
            "stellar-color.js",
            "identity-core-physics.js",
            "identity-core-renderer.js",
            "background-field.js",
            "semantic-zoom.js",
            "index.js",
        ]:
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

    def test_point_light_star_baseline_and_polish_cannot_silently_disappear(self):
        text = (RENDERER / "star-renderer.js").read_text(encoding="utf-8")
        for token in [
            "drawKnowledgeStar",
            "elliptical halo",
            "point source first",
            "Tiny overexposed pinprick",
            "incomplete whisper arc",
            "partial corona filament",
            "arcOffset",
        ]:
            self.assertIn(token, text)

    def test_stellar_temperature_is_visual_only(self):
        text = (RENDERER / "stellar-color.js").read_text(encoding="utf-8")
        for token in [
            "visual-only deterministic parameter",
            "stellarTemperatureForId",
            "kelvinToRgb",
            "stellarPaletteForNode",
        ]:
            self.assertIn(token, text)

    def test_identity_core_physics_is_bounded_and_coupled_to_layout(self):
        text = (RENDERER / "identity-core-physics.js").read_text(encoding="utf-8")
        for token in [
            "maxRadius: 82",
            "homeSpring: 0.032",
            "homeDamping: 0.79",
            "1 - Math.exp",
            "createIdentityCoreInfluenceForce",
            "velocityWake: 0.018",
            "alphaTarget(CORE_PHYSICS.reheatDuringDrag)",
        ]:
            self.assertIn(token, text)

    def test_all_quality_gated_identity_core_families_are_rendered(self):
        text = (RENDERER / "identity-core-renderer.js").read_text(encoding="utf-8")
        for token in [
            "monogram",
            "eclipse",
            "quiet_star",
            "minimal_ring",
            "black_hole",
            "pulsar",
            "binary_star",
            "protostar_nebula",
            "pulsePeriod = 1120",
            "for (const dir of [1, -1])",
            "Math.PI * 2 / 7200",
        ]:
            self.assertIn(token, text)

    def test_background_field_stays_inside_quality_gated_vocabulary(self):
        text = (RENDERER / "background-field.js").read_text(encoding="utf-8")
        for token in [
            "almost_empty",
            "cold_filament",
            "broken_cloud",
            "createAmbientMeteor",
            "drawAmbientMeteor",
        ]:
            self.assertIn(token, text)
        self.assertNotIn("warm_dust", text)
        self.assertNotIn("soft_band", text)

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

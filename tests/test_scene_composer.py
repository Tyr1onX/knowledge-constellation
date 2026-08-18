import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("compose_scene", ROOT / "harness" / "compose_scene.py")
compose_scene = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compose_scene)


def sample():
    input_data = {"subject": {"id": "u1", "label": "Example", "language": "zh-CN", "scope": "GitHub"}, "sources": [{"id": "s1", "kind": "readme", "title": "Project A", "content": "x"}]}
    evidence = {"evidence": [{"id": "e1", "source_ids": ["s1"], "kind": "artifact", "observation": "Implemented and documented a parser.", "confidence": "high", "attribution": "direct", "supports": ["implementation"], "does_not_support": ["broad mastery"]}]}
    model = {"claims": [], "nodes": [{"id": "parser", "label": "Parser implementation", "english_label": "Parser implementation", "state": "established", "confidence": "high", "resolution": "high", "representativeness": "high", "claims": ["c1"], "evidence": ["e1"], "summary": "A concrete parser implementation.", "known": ["implemented"], "unknown": ["transfer"], "reason": "source", "boundary": ["one project"], "next_step": {"title": "More evidence", "text": "Look for another context."}}], "unresolved": []}
    structure = {"anchors": [{"id": "a1", "kind": "project", "label": "Project A", "nodes": ["parser"]}], "relations": [], "motifs": [], "galaxies": [{"id": "g1", "label": "Project A · parsing", "anchor": "a1", "primary_nodes": ["parser"], "secondary_nodes": []}], "distillation": {"primary_nodes": ["parser"], "secondary_nodes": []}}
    visual = {"seed": "kc:test:u1", "identity": {"family": "monogram", "label": "Example", "monogram": "EX", "avatar": None, "presence": {"mode": "brief_intro", "subtitle": "A living knowledge map"}}, "composition": {"archetype": "sparse_archipelago", "asymmetry": .4, "openness": .8, "dominant_axis": "none"}, "field": {"density": "very_sparse", "dust_family": "almost_empty", "temperature_bias": "neutral"}, "stars": {"family": "subtle_point", "temperature_variation": "low"}, "motion": {"temperament": "quiet"}, "anchors": [{"id": "a1", "role": "provenance", "prominence": "low", "galaxies": ["g1"]}], "galaxies": [{"id": "g1", "mass": .4, "morphology": "compact", "dominance": .7}]}
    return input_data, evidence, model, structure, visual


def layout_fixture(archetype="asymmetric_chain", openness=.65):
    structure = {
        "galaxies": [
            {"id": f"g{i}", "label": f"G{i}", "anchor": f"a{i}", "primary_nodes": [], "secondary_nodes": []}
            for i in range(4)
        ]
    }
    visual = {
        "seed": "kc:layout:test",
        "composition": {"archetype": archetype, "asymmetry": .72, "openness": openness, "dominant_axis": "diagonal"},
        "galaxies": [
            {"id": f"g{i}", "mass": .65, "morphology": "compact", "dominance": .7}
            for i in range(4)
        ],
    }
    return visual, structure


class SceneComposerTests(unittest.TestCase):
    def test_sparse_scene_stays_sparse_and_exact(self):
        args = sample(); scene = compose_scene.compose_scene(*args)
        self.assertEqual("kc.scene.v1", scene["version"])
        self.assertEqual(1, len(scene["nodes"])); self.assertEqual(1, len(scene["anchors"])); self.assertEqual(1, len(scene["galaxies"])); self.assertEqual([], scene["relations"])
        self.assertEqual("Example", scene["identity"]["label"]); self.assertEqual("Project A", scene["nodes"][0]["project"]); self.assertEqual("core", scene["nodes"][0]["kind"])
        self.assertEqual([171, 201, 235], scene["galaxies"][0]["color"])
        self.assertEqual([], compose_scene.validate_scene_semantics(scene, args[0], args[2], args[3]))

    def test_composition_is_deterministic(self):
        args = sample(); self.assertEqual(compose_scene.compose_scene(*args), compose_scene.compose_scene(*args))

    def test_scene_cannot_drop_accepted_node(self):
        args = sample(); scene = compose_scene.compose_scene(*args); scene["nodes"] = []
        self.assertIn("scene nodes must exactly match accepted model nodes", compose_scene.validate_scene_semantics(scene, args[0], args[2], args[3]))

    def test_scene_does_not_surface_audit_chrome_by_default(self):
        node = compose_scene.compose_scene(*sample())["nodes"][0]
        self.assertNotIn("confidence", node); self.assertNotIn("unknown", node); self.assertNotIn("next_step", node)

    def test_all_quality_gated_archetypes_keep_identity_core_clear(self):
        cx, cy = compose_scene.WORLD_WIDTH / 2, compose_scene.WORLD_HEIGHT / 2
        for archetype in compose_scene.ARCHETYPE_POINTS:
            visual, structure = layout_fixture(archetype)
            centers = compose_scene.galaxy_centers(visual, structure)
            for point in centers.values():
                self.assertGreaterEqual(math.hypot(point["x"] - cx, point["y"] - cy), compose_scene.CORE_CLEARANCE - 1, archetype)

    def test_asymmetric_chain_is_bent_not_center_diagonal(self):
        visual, structure = layout_fixture("asymmetric_chain")
        centers = list(compose_scene.galaxy_centers(visual, structure).values())
        self.assertGreater(max(p["x"] for p in centers) - min(p["x"] for p in centers), 430)
        self.assertGreater(max(p["y"] for p in centers) - min(p["y"] for p in centers), 150)
        # The middle pair must not both sit close to the Identity Core.
        cx, cy = compose_scene.WORLD_WIDTH / 2, compose_scene.WORLD_HEIGHT / 2
        near = [p for p in centers if math.hypot(p["x"] - cx, p["y"] - cy) < compose_scene.CORE_CLEARANCE + 35]
        self.assertLessEqual(len(near), 1)

    def test_openness_changes_spacing_without_changing_semantics(self):
        compact_visual, structure = layout_fixture("three_islands", openness=0)
        open_visual, _ = layout_fixture("three_islands", openness=1)
        compact = compose_scene.galaxy_centers(compact_visual, structure)
        opened = compose_scene.galaxy_centers(open_visual, structure)
        self.assertNotEqual(compact, opened)
        self.assertEqual(set(compact), set(opened))


if __name__ == "__main__":
    unittest.main()

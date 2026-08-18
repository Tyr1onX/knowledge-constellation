import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "harness" / "verify_eval_case.py"


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class EvalIntegrityTests(unittest.TestCase):
    def minimal_case(self, root):
        case = Path(root) / "case"
        dump(case / "metadata.json", {
            "protocol_version": "kc.cleanroom.v2",
            "validation_mode": "harness",
        })
        dump(case / "source-manifest.json", {
            "subject": {"id": "case-x", "label": "Case X"},
            "sources": [{"id": "S1", "kind": "project", "observation": "Two related practices are documented."}],
        })
        dump(case / "runner" / "pass-a.json", {
            "evidence": [{
                "id": "E1", "source_ids": ["S1"], "kind": "artifact",
                "observation": "Two related practices are documented.",
                "confidence": "high", "attribution": "uncertain",
                "supports": ["project practice"],
                "does_not_support": ["independent mastery"],
            }]
        })
        dump(case / "runner" / "pass-b.json", {
            "claims": [
                {"id": "C1", "subject": "N1", "dimension": "exposure", "value": "supported", "confidence": "high", "evidence": ["E1"], "boundary": "Does not prove independence."},
                {"id": "C2", "subject": "N2", "dimension": "exposure", "value": "supported", "confidence": "high", "evidence": ["E1"], "boundary": "Does not prove independence."},
            ],
            "nodes": [
                {"id": "N1", "label": "Practice One", "state": "observed", "confidence": "high", "resolution": "medium", "representativeness": "high", "activity": "unknown", "claims": ["C1"], "evidence": ["E1"], "summary": "Observed practice one.", "known": ["It appears in the project."], "unknown": ["Independent depth."], "reason": "Representative project context.", "boundary": ["Artifact is not mastery."], "next_step": {"title": "More evidence", "text": "Observe independent behavior."}},
                {"id": "N2", "label": "Practice Two", "state": "observed", "confidence": "high", "resolution": "medium", "representativeness": "high", "activity": "unknown", "claims": ["C2"], "evidence": ["E1"], "summary": "Observed practice two.", "known": ["It appears in the project."], "unknown": ["Independent depth."], "reason": "Representative project context.", "boundary": ["Artifact is not mastery."], "next_step": {"title": "More evidence", "text": "Observe independent behavior."}},
            ],
            "unresolved": [],
        })
        dump(case / "runner" / "pass-c.json", {
            "anchors": [{"id": "A1", "kind": "project", "label": "Project X", "nodes": ["N1", "N2"]}],
            "relations": [{"source": "N1", "target": "N2", "kind": "co_occurrence", "evidence": ["E1"]}],
            "motifs": [],
            "galaxies": [{"id": "G1", "label": "Project X practice", "anchor": "A1", "primary_nodes": ["N1", "N2"], "secondary_nodes": []}],
            "distillation": {"primary_nodes": ["N1", "N2"], "secondary_nodes": []},
        })
        dump(case / "runner" / "pass-d.json", {
            "seed": "kc:test:case-x",
            "identity": {"family": "quiet_star", "label": "Case X", "monogram": None, "avatar": None, "presence": {"mode": "brief_intro", "subtitle": "A personal knowledge universe"}},
            "composition": {"archetype": "compact_cluster", "asymmetry": 0.2, "openness": 0.4, "dominant_axis": "none"},
            "field": {"density": "very_sparse", "dust_family": "almost_empty", "temperature_bias": "neutral"},
            "stars": {"family": "subtle_point", "temperature_variation": "low"},
            "motion": {"temperament": "quiet"},
            "anchors": [{"id": "A1", "role": "provenance", "prominence": "medium", "galaxies": ["G1"]}],
            "galaxies": [{"id": "G1", "mass": 0.7, "morphology": "compact", "dominance": 0.8}],
        })
        dump(case / "runner" / "validation-proof.json", {"validator": "harness/verify_eval_case.py", "pass": True})
        return case

    def run_verify(self, case):
        return subprocess.run([sys.executable, str(VERIFY), str(case)], capture_output=True, text=True)

    def test_valid_v2_case_passes(self):
        with tempfile.TemporaryDirectory() as td:
            case = self.minimal_case(td)
            proc = self.run_verify(case)
            self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
            self.assertTrue(json.loads(proc.stdout)["pass"])

    def test_noncanonical_runner_fails(self):
        with tempfile.TemporaryDirectory() as td:
            case = self.minimal_case(td)
            dump(case / "runner" / "pass-b.json", {"nodes": []})
            proc = self.run_verify(case)
            self.assertNotEqual(0, proc.returncode)
            result = json.loads(proc.stdout)
            self.assertFalse(result["pass"])
            self.assertTrue(any("model:" in error for error in result["errors"]))

    def test_repository_v2_cases_remain_valid(self):
        cases_root = ROOT / "evals" / "clean-room" / "cases"
        if not cases_root.exists():
            return
        for case in sorted(p for p in cases_root.iterdir() if p.is_dir()):
            metadata = case / "metadata.json"
            if not metadata.exists():
                continue
            try:
                meta = json.loads(metadata.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.fail(f"invalid metadata JSON: {metadata}")
            if meta.get("protocol_version") != "kc.cleanroom.v2":
                continue
            proc = self.run_verify(case)
            self.assertEqual(0, proc.returncode, f"{case.name}\n{proc.stdout}\n{proc.stderr}")


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "evals" / "clean-room" / "milestone-10-user.json"
CASES = ROOT / "evals" / "clean-room" / "cases"


class RecognitionMilestoneTests(unittest.TestCase):
    def test_ten_distinct_accepted_users(self):
        data = json.loads(MILESTONE.read_text(encoding="utf-8"))
        accepted = data["accepted_cases"]
        self.assertGreaterEqual(len(accepted), 10)
        targets = [item["target"] for item in accepted]
        self.assertEqual(len(targets), len(set(targets)))
        self.assertTrue(any(item.get("over_conservatism_test") for item in accepted))

        for item in accepted:
            case = CASES / item["case"]
            verdict_path = case / "audit" / "verdict.json"
            self.assertTrue(verdict_path.exists(), f"missing verdict: {item['case']}")
            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
            self.assertEqual("PASS", verdict.get("verdict"), item["case"])
            self.assertEqual(0, verdict.get("critical_inflation"), item["case"])
            self.assertEqual([], verdict.get("material_warnings"), item["case"])
            self.assertTrue(verdict.get("counts_toward_ten_user_gate"), item["case"])
            self.assertEqual("PASS", verdict.get("anchor_identity_handoff"), item["case"])

    def test_gate_contract_is_explicit(self):
        data = json.loads(MILESTONE.read_text(encoding="utf-8"))
        gate = data["gate"]
        self.assertEqual(10, gate["distinct_users"])
        self.assertEqual("PASS", gate["required_verdict"])
        self.assertEqual(0, gate["critical_inflation"])
        self.assertEqual(0, gate["material_warnings"])
        self.assertEqual("PASS", gate["anchor_identity_handoff"])
        self.assertTrue(gate["requires_over_conservatism_counterexample"])
        self.assertTrue(gate["requires_ci_green"])


if __name__ == "__main__":
    unittest.main()

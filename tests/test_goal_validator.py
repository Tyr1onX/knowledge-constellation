import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_goal", ROOT / "harness" / "validate_goal.py")
validate_goal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_goal)


class GoalValidatorTests(unittest.TestCase):
    def goal_input(self):
        return {
            "version": "kc.goal-input.v1",
            "subject_id": "u1",
            "goal": {"id": "G1", "label": "Target role", "statement": "Reach target role", "constraints": []},
            "target_sources": [{"id": "T1", "kind": "job", "title": "Role", "content": "Needs C++."}],
        }

    def target(self):
        return {
            "version": "kc.target.v1",
            "goal_id": "G1",
            "requirements": [
                {"id": "R1", "label": "C++ implementation", "kind": "practice", "dimension": "implementation", "expectation": "required", "source_ids": ["T1"], "rationale": "Role asks for implementation.", "ambiguity": "Depth is not quantified."},
                {"id": "R2", "label": "Work authorization", "kind": "eligibility", "dimension": None, "expectation": "required", "source_ids": ["T1"], "rationale": "Role constraint.", "ambiguity": "Depends on location."},
            ],
        }

    def current_model(self):
        return {"claims": [{"id": "C1"}], "nodes": [{"id": "N1"}]}

    def current_evidence(self):
        return {"evidence": [{"id": "E1"}]}

    def test_target_rejects_unknown_source(self):
        target = self.target()
        target["requirements"][0]["source_ids"] = ["missing"]
        errors = validate_goal.semantic_errors("target", target, {"goal_input": self.goal_input()})
        self.assertTrue(any("unknown target source" in error for error in errors))

    def test_gap_not_observed_cannot_cite_direct_support(self):
        gap = {
            "version": "kc.gap.v1", "goal_id": "G1",
            "items": [
                {"requirement_id": "R1", "status": "not_observed", "current_node_ids": [], "current_claim_ids": [], "current_evidence_ids": ["E1"], "bridge_from_node_ids": ["N1"], "rationale": "No direct evidence.", "boundary": "Absence is not inability.", "verification_needed": []},
                {"requirement_id": "R2", "status": "unresolved", "current_node_ids": [], "current_claim_ids": [], "current_evidence_ids": [], "bridge_from_node_ids": [], "rationale": "Unknown.", "boundary": "Needs user data.", "verification_needed": ["Confirm authorization status."]},
            ],
        }
        errors = validate_goal.semantic_errors("gap", gap, {
            "goal_input": self.goal_input(), "target": self.target(),
            "current_model": self.current_model(), "current_evidence": self.current_evidence(),
        })
        self.assertTrue(any("not_observed must not cite" in error for error in errors))

    def test_plan_keeps_eligibility_out_of_learning_priorities(self):
        gap = {
            "version": "kc.gap.v1", "goal_id": "G1",
            "items": [
                {"requirement_id": "R1", "status": "partial"},
                {"requirement_id": "R2", "status": "unresolved"},
            ],
        }
        plan = {
            "version": "kc.plan.v1", "goal_id": "G1",
            "priorities": [{"id": "P1", "rank": 1, "requirement_ids": ["R2"], "current_foothold_node_ids": [], "title": "Study eligibility", "why_now": "x", "action": "x", "success_evidence": ["x"]}],
            "deferred_requirement_ids": ["R1"],
            "non_learning_constraints": [],
        }
        errors = validate_goal.semantic_errors("plan", plan, {
            "goal_input": self.goal_input(), "target": self.target(), "gap": gap, "current_model": self.current_model(),
        })
        self.assertTrue(any("eligibility constraints cannot be learning priorities" in error for error in errors))
        self.assertTrue(any("unresolved eligibility requirements" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

import json
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2E = ROOT / "harness" / "goal_e2e.py"


class GoalE2ESmokeTests(unittest.TestCase):
    def test_goal_to_gap_to_three_or_fewer_steps(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            current = temp / "current"
            (current / "accepted").mkdir(parents=True)
            (current / "state.json").write_text(json.dumps({"status": "complete"}), encoding="utf-8")
            (current / "accepted" / "input.json").write_text(json.dumps({
                "subject": {"id": "u1", "label": "User"},
                "sources": [{"id": "S1", "kind": "project", "title": "Project", "content": "User implemented a bounded C++ exercise."}],
            }), encoding="utf-8")
            (current / "accepted" / "evidence.json").write_text(json.dumps({
                "evidence": [{"id": "E1", "source_ids": ["S1"], "kind": "behavior", "observation": "A bounded C++ exercise was implemented.", "confidence": "high", "attribution": "direct", "supports": ["bounded C++ implementation"], "does_not_support": ["production independence"]}],
            }), encoding="utf-8")
            (current / "accepted" / "model.json").write_text(json.dumps({
                "claims": [{"id": "C1", "subject": "N1", "dimension": "implementation", "value": "bounded", "confidence": "medium", "evidence": ["E1"], "attribution_evidence": ["E1"], "boundary": "Not production independence."}],
                "nodes": [{"id": "N1", "label": "C++ basics"}],
                "unresolved": [],
            }), encoding="utf-8")

            goal_input = temp / "goal-input.json"
            goal_input.write_text(json.dumps({
                "version": "kc.goal-input.v1", "subject_id": "u1",
                "goal": {"id": "G1", "label": "C++ backend internship", "statement": "Reach a C++ backend internship", "horizon": None, "constraints": []},
                "target_sources": [{"id": "T1", "kind": "job", "title": "Role", "uri": None, "content": "Requires practical C++ implementation.", "observed_at": None}],
            }), encoding="utf-8")

            fake_runner = temp / "fake_goal_runner.py"
            fake_runner.write_text(textwrap.dedent(r'''
                import json
                import os
                from pathlib import Path

                stage = os.environ["KC_STAGE"]
                payloads = {
                    "target": {
                        "version": "kc.target.v1", "goal_id": "G1",
                        "requirements": [{
                            "id": "R1", "label": "Practical C++ implementation", "kind": "practice",
                            "dimension": "implementation", "expectation": "required", "source_ids": ["T1"],
                            "rationale": "The target source explicitly asks for practical implementation.",
                            "ambiguity": "The source does not quantify production depth."
                        }]
                    },
                    "gap": {
                        "version": "kc.gap.v1", "goal_id": "G1",
                        "items": [{
                            "requirement_id": "R1", "status": "partial", "current_node_ids": ["N1"],
                            "current_claim_ids": ["C1"], "current_evidence_ids": ["E1"], "bridge_from_node_ids": ["N1"],
                            "rationale": "There is bounded implementation evidence, but not enough for the broader target context.",
                            "boundary": "Partial does not imply production-level independence.",
                            "verification_needed": ["A larger implementation artifact with tests and debugging evidence."]
                        }]
                    },
                    "plan": {
                        "version": "kc.plan.v1", "goal_id": "G1",
                        "priorities": [{
                            "id": "P1", "rank": 1, "title": "Build one larger C++ service path",
                            "requirement_ids": ["R1"], "current_foothold_node_ids": ["N1"],
                            "why_now": "It extends an existing bounded C++ foothold toward the target's practical requirement.",
                            "action": "Implement a small service feature end-to-end and add tests.",
                            "success_evidence": ["A reviewable repository change showing implementation, tests, and debugging notes."]
                        }],
                        "deferred_requirement_ids": [], "non_learning_constraints": []
                    }
                }
                Path(os.environ["KC_OUTPUT"]).write_text(json.dumps(payloads[stage]), encoding="utf-8")
            '''), encoding="utf-8")

            run = temp / "goal-run"
            runner = f"{shlex.quote(sys.executable)} {shlex.quote(str(fake_runner))}"
            proc = subprocess.run([
                sys.executable, str(E2E),
                "--current-run", str(current), "--goal-input", str(goal_input),
                "--run", str(run), "--runner-command", runner,
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
            self.assertEqual("complete", json.loads((run / "state.json").read_text(encoding="utf-8"))["status"])
            plan = json.loads((run / "accepted" / "plan.json").read_text(encoding="utf-8"))
            self.assertLessEqual(len(plan["priorities"]), 3)
            self.assertEqual("R1", plan["priorities"][0]["requirement_ids"][0])


if __name__ == "__main__":
    unittest.main()

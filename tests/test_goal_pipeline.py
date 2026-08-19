import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "harness" / "goal_pipeline.py"


class GoalPipelineIsolationTests(unittest.TestCase):
    def test_target_workspace_cannot_read_current_person_model(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            current = temp / "current"
            (current / "accepted").mkdir(parents=True)
            (current / "state.json").write_text(json.dumps({"status": "complete"}), encoding="utf-8")
            (current / "accepted" / "input.json").write_text(json.dumps({
                "subject": {"id": "u1", "label": "User"},
                "sources": [{"id": "S1", "kind": "project", "title": "Project", "content": "Project exists."}],
            }), encoding="utf-8")
            (current / "accepted" / "evidence.json").write_text(json.dumps({"evidence": []}), encoding="utf-8")
            (current / "accepted" / "model.json").write_text(json.dumps({"claims": [], "nodes": [], "unresolved": []}), encoding="utf-8")

            goal_input = temp / "goal-input.json"
            goal_input.write_text(json.dumps({
                "version": "kc.goal-input.v1",
                "subject_id": "u1",
                "goal": {"id": "G1", "label": "Backend internship", "statement": "Get a backend internship", "horizon": None, "constraints": []},
                "target_sources": [{"id": "T1", "kind": "job", "title": "Role", "uri": None, "content": "Requires backend fundamentals.", "observed_at": None}],
            }), encoding="utf-8")
            run = temp / "goal-run"

            init = subprocess.run([
                sys.executable, str(PIPELINE), "init",
                "--current-run", str(current), "--goal-input", str(goal_input), "--run", str(run),
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, init.returncode, init.stdout + init.stderr)

            nxt = subprocess.run([sys.executable, str(PIPELINE), "next", "--run", str(run)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, nxt.returncode, nxt.stdout + nxt.stderr)
            packet = json.loads(nxt.stdout)
            self.assertEqual("target", packet["stage"])
            self.assertIn("goal_input", packet["files"])
            self.assertNotIn("current_model", packet["files"])
            workspace_names = {path.name for path in Path(packet["workspace"]).iterdir()}
            self.assertNotIn("current_model.json", workspace_names)
            self.assertNotIn("current_evidence.json", workspace_names)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("recalibrate", ROOT / "harness" / "recalibrate.py")
recalibrate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recalibrate)


class CalibrationLoopTests(unittest.TestCase):
    def base_input(self):
        return {
            "subject": {"id": "u1", "label": "Example", "language": "zh-CN", "scope": "test"},
            "sources": [{"id": "S1", "kind": "project", "title": "Project", "content": "A project exists."}],
        }

    def test_feedback_becomes_first_party_source_without_mutating_original(self):
        original = self.base_input()
        calibrated, source = recalibrate.build_calibrated_input(original, "这部分主要由 AI 完成，我负责 review 和验证。")
        self.assertEqual("user_calibration", source["kind"])
        self.assertEqual("这部分主要由 AI 完成，我负责 review 和验证。", source["content"])
        self.assertEqual(1, len(original["sources"]))
        self.assertEqual(2, len(calibrated["sources"]))
        self.assertEqual(source["id"], calibrated["sources"][-1]["id"])

    def test_identical_feedback_is_idempotent(self):
        first, source = recalibrate.build_calibrated_input(self.base_input(), "这个方向对我更重要。")
        second, same = recalibrate.build_calibrated_input(first, "这个方向对我更重要。")
        self.assertEqual(source["id"], same["id"])
        self.assertEqual(2, len(second["sources"]))

    def test_feedback_id_is_deterministic(self):
        a = recalibrate.calibration_source("我目前只是学习 JavaScript。")
        b = recalibrate.calibration_source("  我目前只是学习 JavaScript。\n")
        self.assertEqual(a["id"], b["id"])
        self.assertTrue(a["id"].startswith("CAL-"))

    def test_completed_run_is_required(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            (run / "accepted").mkdir()
            (run / "accepted" / "input.json").write_text(json.dumps(self.base_input()), encoding="utf-8")
            (run / "state.json").write_text(json.dumps({"status": "running"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                recalibrate.load_completed_input(run)
            (run / "state.json").write_text(json.dumps({"status": "complete"}), encoding="utf-8")
            loaded = recalibrate.load_completed_input(run)
            self.assertEqual("u1", loaded["subject"]["id"])

    def test_recalibration_starts_a_new_full_e2e_run(self):
        cmd = recalibrate.recalibration_command(
            Path("input.json"), Path("run-r2"), Path("dist-r2"), "codex-runner", True
        )
        joined = " ".join(str(part) for part in cmd)
        self.assertIn("harness/e2e.py", joined.replace("\\", "/"))
        self.assertIn("--runner-command", cmd)
        self.assertIn("--fresh", cmd)
        source = (ROOT / "harness" / "recalibrate.py").read_text(encoding="utf-8")
        self.assertNotIn("compose_scene", source)
        self.assertNotIn("accepted/model.json", source)
        self.assertNotIn("accepted/visual.json", source)


if __name__ == "__main__":
    unittest.main()

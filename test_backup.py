
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from game import QuizGame
from quiz import Quiz


class BackupTests(unittest.TestCase):
    def test_backup_created_and_corrupt_original_recovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"

            with contextlib.redirect_stdout(io.StringIO()):
                game = QuizGame(path)

            game.quizzes.append(
                Quiz("백업 복구 테스트", ["A", "B", "C", "D"], 2)
            )
            game.best_score = {
                "points": 100, "correct": 1, "total": 1
            }
            self.assertTrue(game.save_state())

            backup = Path(str(path) + ".bak")
            self.assertTrue(backup.exists())

            path.write_text("{broken", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                recovered = QuizGame(path)

            self.assertEqual(
                recovered.quizzes[-1].question, "백업 복구 테스트"
            )
            self.assertEqual(recovered.best_score["points"], 100)
            self.assertTrue(recovered.save_state())

            # 손상된 원본으로 정상 백업을 덮어쓰지 않았는지 확인합니다.
            with contextlib.redirect_stdout(io.StringIO()):
                check = QuizGame(backup)
            self.assertEqual(check.best_score["points"], 100)

    def test_previous_valid_version_is_backed_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            with contextlib.redirect_stdout(io.StringIO()):
                game = QuizGame(path)

            self.assertTrue(game.save_state())
            first_count = len(game.quizzes)
            game.quizzes.append(
                Quiz("추가 문제", ["A", "B", "C", "D"], 1)
            )
            self.assertTrue(game.save_state())

            with contextlib.redirect_stdout(io.StringIO()):
                previous = QuizGame(Path(str(path) + ".bak"))
            self.assertEqual(len(previous.quizzes), first_count)

    def test_deleted_original_restores_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            with contextlib.redirect_stdout(io.StringIO()):
                game = QuizGame(path)
            game.best_score = {"points": 75, "correct": 3, "total": 4}
            self.assertTrue(game.save_state())
            path.unlink()
            with contextlib.redirect_stdout(io.StringIO()):
                recovered = QuizGame(path)
            self.assertEqual(recovered.best_score["points"], 75)

    def test_both_files_corrupt_falls_back_to_defaults(self):
        from game import DEFAULT_QUIZZES
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text("{broken", encoding="utf-8")
            Path(str(path) + ".bak").write_text("{broken", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                game = QuizGame(path)
            self.assertEqual(len(game.quizzes), len(DEFAULT_QUIZZES))
            self.assertIsNone(game.best_score)

    def test_saved_utf8_characters_are_not_mangled(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            with contextlib.redirect_stdout(io.StringIO()):
                game = QuizGame(path)
            game.quizzes.append(Quiz("한글 질문인가요?", ["예", "아니요", "가끔", "모름"], 1))
            self.assertTrue(game.save_state())
            raw = path.read_text(encoding="utf-8")
            self.assertIn("한글 질문인가요?", raw)
            self.assertEqual(json.loads(raw)["quizzes"][-1]["answer"], 1)


if __name__ == "__main__":
    unittest.main()

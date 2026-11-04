
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
                Quiz("?? ????", ["A", "B", "C", "D"], 2)
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
                recovered.quizzes[-1].question, "?? ????"
            )
            self.assertEqual(recovered.best_score["points"], 100)
            self.assertTrue(recovered.save_state())

            # ??? ??? ???? ??? ???? ??.
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
                Quiz("? ???", ["A", "B", "C", "D"], 1)
            )
            self.assertTrue(game.save_state())

            with contextlib.redirect_stdout(io.StringIO()):
                previous = QuizGame(Path(str(path) + ".bak"))
            self.assertEqual(len(previous.quizzes), first_count)


if __name__ == "__main__":
    unittest.main()

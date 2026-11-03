"""외부 라이브러리 없이 실행하는 기본 단위 테스트."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game import DEFAULT_QUIZZES, QuizGame
from quiz import Quiz


class QuizTests(unittest.TestCase):
    def test_correct_answer(self):
        quiz = Quiz("Q", ["a", "b", "c", "d"], 2)
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_invalid_answer_rejected(self):
        with self.assertRaises(ValueError):
            Quiz("Q", ["a", "b", "c", "d"], 0)

    def test_invalid_quiz_dict_rejected(self):
        with self.assertRaises(ValueError):
            Quiz.from_dict({"question": "Q", "choices": ["a"], "answer": 1})


class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "state.json"
        with contextlib.redirect_stdout(io.StringIO()):
            self.game = QuizGame(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_default_questions(self):
        self.assertGreaterEqual(len(DEFAULT_QUIZZES), 5)

    def test_save_and_reload(self):
        self.game.quizzes.append(Quiz("추가?", ["1", "2", "3", "4"], 1))
        self.game.best_score = {"points": 100, "correct": 1, "total": 1}
        self.assertTrue(self.game.save_state())
        with contextlib.redirect_stdout(io.StringIO()):
            reloaded = QuizGame(self.path)
        self.assertEqual(reloaded.quizzes[-1].question, "추가?")
        self.assertEqual(reloaded.best_score["points"], 100)
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8"))["quizzes"][-1]["answer"], 1)

    def test_corrupt_file_recovers(self):
        self.path.write_text("{broken", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            recovered = QuizGame(self.path)
        self.assertEqual(len(recovered.quizzes), len(DEFAULT_QUIZZES))
        self.assertTrue(recovered.save_state())
        json.loads(self.path.read_text(encoding="utf-8"))

    def test_invalid_input_retries(self):
        with patch("builtins.input", side_effect=["", "abc", "9", " 2 "]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.game.ask_number("입력: ", 1, 5), 2)

    def test_eof_exits_safely(self):
        with patch("builtins.input", side_effect=EOFError):
            with contextlib.redirect_stdout(io.StringIO()):
                self.game.run()
        self.assertTrue(self.path.exists())


if __name__ == "__main__":
    unittest.main()

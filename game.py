"""게임 진행, 사용자 입력, JSON 영속성을 담당하는 QuizGame 클래스."""

import json
from pathlib import Path

from quiz import Quiz


class InputStopped(Exception):
    """Ctrl+C 또는 입력 종료 시 안전하게 종료하기 위한 신호."""


DEFAULT_QUIZZES = [
    Quiz("문어의 심장은 몇 개일까요?", ["1개", "2개", "3개", "4개"], 3),
    Quiz("바나나는 식물학적으로 어떤 열매에 해당할까요?", ["견과", "장과(베리)", "핵과", "삭과"], 2),
    Quiz("금성에서 더 긴 것은 무엇일까요? (자전 주기와 공전 주기 비교)", ["하루(자전 주기)", "1년(공전 주기)", "똑같다", "계절마다 다르다"], 1),
    Quiz("상어의 골격을 주로 이루는 것은?", ["뼈", "나무", "연골", "껍데기"], 3),
    Quiz("일반적으로 벌은 다리가 몇 개일까요?", ["4개", "6개", "8개", "10개"], 2),
    Quiz("성체 개구리는 보통 물을 무엇을 통해 흡수할까요?", ["피부", "귀", "꼬리", "이빨"], 1),
    Quiz("빛은 소리보다 진공에서 어떻게 이동할까요?", ["느리게", "같은 속도로", "더 빠르게", "이동하지 못한다"], 3),
]


class QuizGame:
    def __init__(self, state_path: Path | str | None = None):
        self.state_path = Path(state_path) if state_path is not None else Path(__file__).resolve().parent / "state.json"
        self.quizzes = [Quiz.from_dict(q.to_dict()) for q in DEFAULT_QUIZZES]
        self.best_score: dict | None = None
        self.load_state()

    def load_state(self) -> None:
        if not self.state_path.exists():
            print("기본 퀴즈를 불러왔습니다. (첫 실행)")
            return
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                state = json.load(file)
            if not isinstance(state, dict) or not isinstance(state.get("quizzes"), list):
                raise ValueError("quizzes 배열이 없습니다.")
            quizzes = [Quiz.from_dict(item) for item in state["quizzes"]]
            raw_score = state.get("best_score")
            if raw_score is not None:
                if (not isinstance(raw_score, dict) or
                        type(raw_score.get("points")) is not int or not 0 <= raw_score["points"] <= 100 or
                        type(raw_score.get("correct")) is not int or
                        type(raw_score.get("total")) is not int or
                        not 0 <= raw_score["correct"] <= raw_score["total"] or raw_score["total"] < 1):
                    raise ValueError("best_score 형식이 잘못되었습니다.")
            self.quizzes = quizzes
            self.best_score = raw_score
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as error:
            print(f"⚠️ 저장 파일을 읽지 못했습니다: {error}")
            print("기본 퀴즈로 시작합니다. 다음 저장 때 파일이 복구됩니다.")

    def save_state(self) -> bool:
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            return True
        except (OSError, UnicodeError, TypeError, ValueError) as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")
            return False

    @staticmethod
    def prompt(message: str) -> str:
        try:
            return input(message).strip()
        except (KeyboardInterrupt, EOFError) as error:
            raise InputStopped() from error

    def ask_number(self, message: str, minimum: int, maximum: int) -> int:
        while True:
            raw = self.prompt(message)
            if not raw:
                print(f"⚠️ 빈 입력입니다. {minimum}~{maximum}의 숫자를 입력하세요.")
                continue
            try:
                number = int(raw)
            except ValueError:
                print(f"⚠️ 숫자를 입력하세요. ({minimum}~{maximum})")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"⚠️ 범위를 벗어났습니다. {minimum}~{maximum}의 숫자를 입력하세요.")

    def ask_text(self, message: str) -> str:
        while True:
            value = self.prompt(message)
            if value:
                return value
            print("⚠️ 빈 입력은 사용할 수 없습니다. 다시 입력하세요.")

    def play(self) -> None:
        if not self.quizzes:
            print("아직 등록된 퀴즈가 없습니다.")
            return
        correct = 0
        total = len(self.quizzes)
        print(f"\n📝 퀴즈 시작! 총 {total}문제")
        for number, quiz in enumerate(self.quizzes, 1):
            quiz.show(number)
            selected = self.ask_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(selected):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        points = round(correct / total * 100)
        print(f"\n🏆 결과: {total}문제 중 {correct}문제 정답! ({points}점)")
        if self.best_score is None or points > self.best_score["points"]:
            self.best_score = {"points": points, "correct": correct, "total": total}
            print("🎉 새로운 최고 점수입니다!")
        self.save_state()

    def add_quiz(self) -> None:
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.ask_text("문제: ")
        choices = [self.ask_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.ask_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("✅ 퀴즈가 추가되어 저장되었습니다!")
        else:
            print("⚠️ 퀴즈는 현재 실행 중에만 추가되었습니다. 저장 오류를 확인하세요.")

    def show_list(self) -> None:
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"[{number}] {quiz.question}")

    def show_score(self) -> None:
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return
        score = self.best_score
        print(f"🏆 최고 점수: {score['points']}점 ({score['total']}문제 중 {score['correct']}문제 정답)")

    def run(self) -> None:
        try:
            while True:
                print("\n=== 반전 상식 퀴즈 ===")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 최고 점수")
                print("5. 종료")
                choice = self.ask_number("번호를 선택하세요 (1~5): ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
                else:
                    self.save_state()
                    print("안전하게 종료합니다. 다음에 만나요!")
                    break
        except InputStopped:
            print("\n입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
            self.save_state()

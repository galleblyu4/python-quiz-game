"""한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("모든 선택지에 내용이 있어야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4의 숫자여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def show(self, number: int) -> None:
        print(f"\n[문제 {number}] {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def is_correct(self, selected: int) -> bool:
        return selected == self.answer

    def to_dict(self) -> dict:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")
        return cls(data.get("question"), data.get("choices"), data.get("answer"))

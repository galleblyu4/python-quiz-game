"""1,000문제 성능 검증: 실제 QuizGame JSON 저장/로드 및 목록 검색.

실제 사용자 state.json은 변경하지 않는다. 테스트 데이터는 임시 폴더에 저장된다.
수치는 실행 환경에 따라 달라지는 참고값이다.
"""
import gc
import tempfile
import time
import tracemalloc
from pathlib import Path

from game import QuizGame
from quiz import Quiz


def measure_1000() -> str:
    count = 1000
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "state.json"
        game = QuizGame(path)
        game.quizzes = [
            Quiz(f"성능 테스트 문항 {i:04d}", ["A", "B", "C", "D"], (i % 4) + 1)
            for i in range(count)
        ]

        gc.collect()
        tracemalloc.start()
        start = time.perf_counter()
        assert game.save_state(), "1,000문항 JSON 저장 실패"
        save_seconds = time.perf_counter() - start

        start = time.perf_counter()
        loaded = QuizGame(path)
        load_seconds = time.perf_counter() - start
        assert len(loaded.quizzes) == count, "로드한 문제 수가 다릅니다"

        start = time.perf_counter()
        found = [quiz for quiz in loaded.quizzes if "0999" in quiz.question]
        search_seconds = time.perf_counter() - start
        assert len(found) == 1, "검색 결과가 예상과 다릅니다"

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        state_bytes = path.stat().st_size

    result = f"""# 1,000문제 성능 분석 (실제 QuizGame 기준)

- 테스트 문항 수: {count:,}개
- JSON 저장: {save_seconds:.6f}초
- JSON 로드 및 Quiz 객체 생성: {load_seconds:.6f}초
- 목록 검색: {search_seconds:.6f}초 (검색 결과 {len(found)}개)
- 최대 추적 메모리: {peak / (1024 * 1024):.3f} MiB
- JSON 파일 크기: {state_bytes / 1024:.1f} KiB
- 테스트 범위: 임시 파일에서 저장/로드/검색을 수행해 사용자의 state.json 보존

## 성능과 확장 전략

- 현재 문항 목록 검색은 선형 탐색이므로 시간복잡도 O(n)이다.
- 전체 문제를 메모리에 보관하므로 데이터 규모에 따른 메모리는 대체로 O(n)이다.
- 목록 표시를 20개 단위로 페이지 구분하면 터미널 출력 부담을 낮출 수 있다.
- 반복 검색은 정규화한 질문별 색인을 만들면 빠르지만, 색인 메모리 비용이 추가된다.
- 수만 문항으로 확장되면 SQLite와 LIMIT/OFFSET 또는 키셋 페이징을 고려한다.
- tracemalloc은 파이썬 추적 할당을 측정하며, 프로세스 전체 RSS를 의미하지 않는다.
- 측정 시간과 메모리는 컴퓨터·Python 버전·운영체제에 따라 달라진다.
"""
    report = Path(__file__).resolve().parent / "docs" / "logs" / "performance-1000.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(result, encoding="utf-8")
    return result


if __name__ == "__main__":
    print(measure_1000())

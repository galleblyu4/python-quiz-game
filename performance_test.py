import json
import time
import tracemalloc
from pathlib import Path

questions = [
    {
        "question": f"테스트 문제 {i}",
        "choices": ["1번", "2번", "3번", "4번"],
        "answer": 1
    }
    for i in range(1000)
]

tracemalloc.start()
start = time.perf_counter()

data = json.dumps(questions, ensure_ascii=False)
loaded = json.loads(data)
found = [q for q in loaded if "999" in q["question"]]

elapsed = time.perf_counter() - start
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

Path("docs/logs").mkdir(parents=True, exist_ok=True)

report = f"""# 1000문제 성능 분석

- 테스트 문항 수: {len(questions)}
- JSON 처리 및 검색 시간: {elapsed:.6f}초
- 최대 추적 메모리: {peak / 1024 / 1024:.3f} MiB
- 검색 결과 수: {len(found)}
- 검색 시간복잡도: O(n)
- 메모리 사용량: 문항 수에 비례하여 O(n) 증가
- 개선 방안: 문제 목록 20개씩 페이지 분할, 반복 검색 시 색인 활용, 데이터 증가 시 SQLite 도입
- 참고: 측정값은 현재 컴퓨터의 실행 환경에 따라 달라질 수 있음
"""

Path("docs/logs/performance-1000.md").write_text(report, encoding="utf-8")
print(report)

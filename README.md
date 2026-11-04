# 🎯 반전 상식 퀴즈 (Python 콘솔 게임)

## 1. 프로젝트 개요와 주제 선정 이유

Python의 입력·출력, 조건문, 반복문, 함수, 클래스, 예외 처리, JSON 파일 저장을 익히기 위해 터미널에서 동작하는 4지선다 퀴즈 게임을 만들었다. 일상에서 사실과 다르게 생각하기 쉬운 **반전 상식**을 주제로 선택했다. 별도 라이브러리 없이 Python 3.10 이상에서 실행할 수 있다.

## 2. 실행 방법

```bash
python --version
python main.py
```

Windows에서 `python` 명령이 동작하지 않으면 `py main.py`, macOS/Linux에서는 `python3 main.py`를 사용할 수 있다.

## 3. 기능

| 메뉴 | 기능 | 검증 방법 |
|---|---|---|
| 1 | 퀴즈 풀기와 정답/오답 안내 | 현재 저장된 모든 문제를 풀고 결과 확인 |
| 2 | 퀴즈 추가 | 문제·선택지 4개·정답 입력 후 저장 |
| 3 | 퀴즈 목록 | 기본 및 추가 문제 표시 |
| 4 | 최고 점수 | 최고 점수 표시 및 기록 유지 |
| 5 | 종료 | 저장 후 정상 종료 |

빈 입력, 공백 입력, 숫자가 아닌 문자, 허용 범위 밖 숫자를 다시 입력하도록 처리한다. Ctrl+C/EOF에서도 저장하고 안전하게 종료한다.

## 4. 파일 구조

```text
python-quiz-game/
├── main.py             # 프로그램 시작점
├── quiz.py             # Quiz 클래스: 한 문제, 출력, 정답 확인
├── game.py             # QuizGame 클래스: 메뉴, 입력, 게임, 저장/불러오기
├── state.json          # 실행 시 생성되는 퀴즈 및 최고 점수 데이터
├── tests.py            # 기본 단위 테스트
├── test_backup.py      # 백업·복구 단위 테스트
├── performance_test.py # 1,000문제 성능 분석
├── .gitignore          # 불필요한 파일 제외
└── docs/
    ├── logs/           # Git 증빙 및 성능 분석
    └── screenshots/    # 실제 실행 화면 증거
```

## 5. JSON 데이터 파일

프로젝트 루트의 `state.json`을 UTF-8로 저장한다. 첫 실행에서 파일이 없으면 기본 퀴즈 7개로 시작하며, 종료하거나 퀴즈를 추가하거나 게임을 마치면 파일이 만들어진다. 손상된 JSON은 유효한 백업이 있으면 백업에서 복원하고, 두 파일 모두 손상되었다면 기본 퀴즈로 시작한다. **기존 저장 데이터를 유지하려면 `state.json`을 삭제하지 않는다.**

```json
{
  "quizzes": [
    {"question": "문어의 심장은 몇 개일까요?", "choices": ["1개", "2개", "3개", "4개"], "answer": 3}
  ],
  "best_score": {"points": 100, "correct": 7, "total": 7}
}
```

`quizzes`는 문제 객체 배열, `best_score`는 최고 점수(100점 만점)와 정답 수·전체 문항 수를 저장한다. 실제 실행 시 기본 퀴즈는 7개다. 아직 플레이하지 않았다면 `best_score`는 `null`이다.

## 6. 클래스 설계

- `Quiz`: `question`, `choices`, `answer` 속성, `show()` 문제 출력, `is_correct()` 정답 확인, `to_dict()`/`from_dict()` JSON 변환
- `QuizGame`: 퀴즈 목록·최고 점수, `run()` 메뉴, `play()` 진행, `add_quiz()` 등록, `show_list()` 목록, `show_score()` 점수, `save_state()`/`load_state()` JSON 저장

## 7. 실행 검증

```bash
python -m unittest -v tests test_backup
python performance_test.py
```

- [ ] Python 3.10 이상 버전 확인
- [ ] 메뉴 및 잘못된 입력 시험
- [ ] 퀴즈 추가 후 재시작하여 유지 확인
- [ ] 점수 갱신 후 재시작하여 유지 확인
- [ ] `state.json` 삭제/손상 시 복구 확인 (반드시 데이터 백업 후 테스트)
- [ ] Ctrl+C 및 EOF 시 안전 종료 확인
- [ ] 캡처 파일 추가: [screenshots](docs/screenshots/README.md)

**주의:** 체크리스트는 개발자가 직접 실행하고 결과를 확인한 뒤 `[x]`로 표시한다.

## 8. Git 요구사항과 수행 기록

- 10개 이상의 **의미 있는 실제 커밋**이 필요하다. 기능을 단계별로 구현·수정할 때마다 기록한다. 빈 커밋이나 같은 파일의 의미 없는 반복 수정으로 개수만 채우지 않는다.
- `main` 외의 브랜치를 생성해 퀴즈 기능을 작업하고, 변경사항을 커밋한 후 `main`으로 병합한다.
- 완성 후 별도 디렉터리에 `git clone`하고, 그 복제본에서 README 한 줄을 고쳐 commit/push한다. 원래 폴더에서 `git pull`로 반영을 확인한다.
- Git 실행 기록과 결과는 실제 수행 후 스크린샷이나 문서에 첨부한다.

```bash
git log --oneline --graph --all
git branch -a
git remote -v
```

**상세 진행 안내:** [Git 실습 단계](docs/GIT-STEPS.md)

### Git 명령어 의미

| 명령 | 설명 |
|---|---|
| `init` | 새 로컬 저장소 시작 |
| `add` | 커밋할 변경 파일 선택 |
| `commit` | 변경 이력 저장 |
| `push` | GitHub에 올리기 |
| `pull` | GitHub의 변경 내역 가져오기 |
| `checkout` | 다른 브랜치로 이동하기 |
| `clone` | 저장소를 새 폴더에 복제하기 |

## 9. 기본 문법 학습 메모

- 변수: 값을 이름에 저장하여 다시 쓸 수 있게 하는 것
- `int` 정수, `str` 문자열, `bool` 참·거짓, `list` 순서 있는 목록, `dict` 키와 값의 짝
- `if/elif/else`: 입력에 따라 기능 선택
- `while`: 사용자가 종료할 때까지 메뉴 반복, `for`: 각 퀴즈/선택지 순회
- 함수: 여러 동작을 이름으로 묶음. 매개변수는 함수에 전달하는 값, 반환값은 함수가 돌려주는 값
- 클래스: 관련 데이터(속성)와 행동(메서드)을 묶는 설계도. `__init__`는 객체를 만들 때 호출되고 `self`는 현재 객체를 가리킴
- JSON: 데이터를 텍스트로 구조화해 저장하는 형식. `try/except`는 파일 오류나 입력 오류가 있어도 프로그램이 중단되지 않도록 도움

## 10. 제출용 실제 스크린샷

- [메뉴](docs/screenshots/menu.png)
- [퀴즈 풀기](docs/screenshots/play.png)
- [퀴즈 추가](docs/screenshots/add_quiz.png)
- [퀴즈 목록](docs/screenshots/list.png)
- [최고 점수](docs/screenshots/score.png)
- [Git 로그](docs/screenshots/git-log.png)

> 위 링크는 저장소에 실제 포함된 실행 화면이다. 개발 환경(Python/Git 버전) 캡처는 필요하면 별도로 추가한다.

## 퀴즈 게임 사용 안내
메뉴에서 1번은 퀴즈 풀기, 2번은 퀴즈 추가, 3번은 목록 확인, 4번은 최고 점수 확인, 5번은 종료입니다.

## 잘못된 입력 처리
메뉴에서 숫자가 아닌 문자, 빈 입력, 범위 밖 숫자를 입력하면 오류 안내 후 다시 입력받습니다.

## Python 자료형
int는 정수, str은 문자열, bool은 참과 거짓, list는 목록, dict는 키와 값으로 데이터를 관리합니다.

## 조건문과 반복문
if, elif, else는 조건에 따라 동작을 선택합니다. for는 정해진 목록을 반복하고 while은 조건이 참인 동안 반복합니다.

## 클래스 구조
Quiz 클래스는 문제와 정답을 관리하고 QuizGame 클래스는 메뉴와 전체 게임 진행을 관리합니다.

## JSON 데이터 저장
state.json은 퀴즈 목록과 최고 점수를 저장합니다. UTF-8 인코딩을 사용하며 프로그램을 다시 실행해도 데이터가 유지됩니다.

## Git과 GitHub
Git은 컴퓨터에서 코드 변경 이력을 관리하고 GitHub는 그 기록을 인터넷에 보관하고 공유하는 서비스입니다.

## 예외 처리
try와 except를 사용하면 잘못된 입력이나 파일 오류가 발생해도 프로그램을 안전하게 처리할 수 있습니다.

## Git 복제 실습
복제한 저장소에서 README를 수정하고 GitHub에 공유했습니다.

## 11. AI 사전평가 피드백 보완 사항

### 기본 퀴즈와 실행 흐름 (#1, #4, #10)

기본 퀴즈는 `game.py`의 `DEFAULT_QUIZZES` **7개**이다. 사용자 추가 퀴즈가 저장되어 있다면 실제 플레이 문제 수는 더 늘어난다. 프로젝트의 `state.json`에는 현재 **9개 문제**와 최고 점수 기록이 들어 있다.

실행 예시:

```text
=== 반전 상식 퀴즈 ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 최고 점수
5. 종료
번호를 선택하세요 (1~5): 3
```

프로그램 시작 → `state.json` 로드 → 파일 오류 시 백업 확인 → 메뉴 → 풀이/추가 → 저장 → 정상 종료 순서로 동작한다. 잘못된 입력은 `ask_number()`와 `ask_text()`에서 처리하므로 게임 로직과 분리된다.

### 실제 Git 증빙 (#5, #6, #7, #12)

- [`git-history.txt`](docs/logs/git-history.txt): 당시 수집된 커밋 그래프
- [`git-remote.txt`](docs/logs/git-remote.txt): 원격 저장소 주소
- [`git-branches.txt`](docs/logs/git-branches.txt): 당시 브랜치 정보
- [`git-reflog.txt`](docs/logs/git-reflog.txt): 해당 PC의 로컬 reflog
- [`clone-pull-verification.txt`](docs/logs/clone-pull-verification.txt): 별도 임시 디렉터리 clone 및 pull 확인
- [`git-evidence-check.md`](docs/logs/git-evidence-check.md): 증빙의 범위와 현재 부족한 사항

**중요:** Git 로그·브랜치는 수집 당시의 PC 환경과 시점을 보여준다. 소스 ZIP에는 `.git` 이력이 들어 있지 않으므로, ZIP에서 과거 병합 이력을 검증하거나 새로운 이력을 꾸며낼 수 없다. **커밋 10개 이상**과 **기능별 의미 있는 변경 10개 이상**은 다른 조건이다. 두 번째 조건은 실제 `git show`/`git log --stat`으로 판단해야 한다.

현재 컴퓨터에서 최신 증빙을 갱신하려면 다음 명령을 실행한다.

```powershell
py tools/collect_git_evidence.py
```

별도 브랜치 작업·병합 자체는 이 스크립트가 대신하지 않으며, 실제 수행했을 때에만 `git log --graph --all`에 나타난다.

### 클래스 설계와 역할 분리 (#8, #9, #13)

| 클래스·메서드 | 책임 |
|---|---|
| `Quiz.__init__()` | 문제/선택지/정답 검증 및 생성 |
| `Quiz.is_correct()` | 답안 정오 판정 |
| `Quiz.to_dict()` / `Quiz.from_dict()` | JSON 자료구조 변환 |
| `QuizGame.run()` | 메뉴와 선택 흐름 제어 |
| `QuizGame.play()` | 전체 문제 풀이 및 점수 계산 |
| `QuizGame.add_quiz()` | 사용자 문제 입력 및 저장 |
| `QuizGame.ask_number()` | 빈 값·문자·범위 오류 입력 재시도 |
| `QuizGame._read_state()` | 저장 파일 형식 검증 |
| `QuizGame.load_state()` | 원본 우선 로드, 손상 시 백업 복원 |
| `QuizGame.save_state()` | 임시 파일 저장, 백업, 교체 |

`Quiz`는 문제와 정답을 독립적으로 나타내므로, 콘솔이 아닌 웹 학습 앱의 문제 모델이나 단위 테스트에서도 재사용할 수 있다. 메뉴 입력과 JSON 처리를 `Quiz`에 넣지 않아 각 클래스를 독립적으로 변경·테스트할 수 있다.

### 1,000개 이상 성능 검증 (#16)

```powershell
py performance_test.py
```

실제 `QuizGame` 객체에 **1,000문제**를 넣어 임시 JSON에 저장하고, 다시 읽은 뒤 검색한다. 실행 결과는 [`performance-1000.md`](docs/logs/performance-1000.md)에 기록된다. 프로그램의 실제 `state.json`은 변경하지 않는다.

현재 구조는 전체 목록을 메모리에 적재하므로 메모리 O(n), 검색 O(n)이다. 목록을 20개 단위로 표시하고 반복 검색에 색인을 활용하거나, 문항 수가 크게 증가하면 SQLite 및 페이징을 적용하는 것이 바람직하다. 실측값은 컴퓨터 환경에 따라 달라진다.

### 자동 백업·복구 및 예외 처리 (#11, #15, #17)

저장 정책:

1. `state.json`에 기존 **정상 데이터**가 있다면 이를 `state.json.bak`에 복사한다.
2. 변경 데이터를 UTF-8 JSON 임시 파일로 기록한 뒤 `os.replace()`로 원본을 교체해 부분 쓰기 위험을 줄인다.
3. 최초 저장에는 백업이 없으므로 새 원본으로 `state.json.bak`도 생성한다.
4. 원본이 손상되거나 없어지면 유효한 `.bak` 파일을 읽는다. 백업까지 손상되었으면 기본 7문제로 시작한다.
5. 손상된 원본은 정상 백업을 덮어쓰지 않는다. 파일 쓰기 권한이나 디스크 공간이 부족하면 저장 실패 메시지를 표시한다.

수동 복구: 프로그램을 종료하고 두 JSON 파일을 별도 위치에 복사해 보존한 다음, 프로그램을 재실행하면 백업 로드를 시도한다. 정상 종료하면 복원된 내용을 원본에 다시 기록한다. 백업은 직전의 정상 저장 버전이므로 **가장 최근 추가한 문제가 복원되지 않을 수 있다.**

`Ctrl+C`, EOF는 `InputStopped`로 전환해 안전한 종료 흐름에서 저장한다. 외부에서 강제로 종료하는 `SIGTERM`은 환경에 따라 별도 처리나 OS 수준 복구가 필요하므로 여기서 완전한 보장을 주장하지 않는다.

검증 명령:

```powershell
py -m unittest -v tests test_backup
```

### 유지보수·요구사항 변경 가이드 (#18)

| 변경 요구 | 수정 대상 | 검증 포인트 |
|---|---|---|
| 점수 계산법 변경 | `game.py` → `QuizGame.play()` | 반올림·최고 점수 갱신 |
| 퀴즈 선택지 개수 변경 | `quiz.py` → `Quiz.__init__()`·`show()` | 입력 번호 범위·JSON 호환성 |
| 정답 판정 변경 | `quiz.py` → `Quiz.is_correct()` | 정답과 오답 판정 |
| 기본 퀴즈 변경 | `game.py` → `DEFAULT_QUIZZES` | 저장 파일이 없는 최초 실행 |
| 추가 입력 과정 변경 | `game.py` → `add_quiz()` | 입력 검증 및 저장 |
| 메뉴 변경 | `game.py` → `run()` | 메뉴 번호·종료 경로 |
| 파일 구조 변경 | `game.py` → `_read_state()`, `save_state()` | 이전 JSON 호환성·백업 복원 |
| 저장 오류 처리 변경 | `game.py` → `save_state()`, `load_state()` | 권한 오류·손상된 파일 |
| 대규모 문항 성능 개선 | `performance_test.py`, `show_list()` | 시간/메모리·페이지 출력 |

수정 후 **`py -m unittest -v tests test_backup`**로 회귀 테스트를 수행하고, 자료 저장 방식이나 큰 데이터 처리 변경이 있다면 **`py performance_test.py`**를 추가 실행한다.

## Verified Git Commit History
- [Public GitHub commit history](https://github.com/galleblyu4/python-quiz-game/commits/main)
- Full Git history bundle: docs/git-history.bundle
- Verify with: git bundle verify docs/git-history.bundle
- The bundle includes original Git history and branch references.

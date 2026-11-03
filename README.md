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
| 1 | 퀴즈 풀기와 정답/오답 안내 | 문제 7개를 풀고 결과 확인 |
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
├── tests.py            # 표준 라이브러리 unittest 검증
├── .gitignore          # 불필요한 파일 제외
└── docs/
    └── screenshots/    # 실제 실행 화면 증거를 저장하는 곳
```

## 5. JSON 데이터 파일

프로젝트 루트의 `state.json`을 UTF-8로 저장한다. 첫 실행에서 파일이 없으면 기본 퀴즈 7개로 시작하며, 종료하거나 퀴즈를 추가하거나 게임을 마치면 파일이 만들어진다. 손상된 JSON은 기본 퀴즈로 복구한다. **기존 저장 데이터를 유지하려면 `state.json`을 삭제하지 않는다.**

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
python -m unittest -v tests
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

## 10. 제출용 실제 스크린샷 (촬영 후 삽입)

- [메뉴](docs/screenshots/menu.png)
- [퀴즈 풀기](docs/screenshots/play.png)
- [퀴즈 추가](docs/screenshots/add_quiz.png)
- [퀴즈 목록](docs/screenshots/list.png)
- [최고 점수](docs/screenshots/score.png)
- [Git 로그](docs/screenshots/git-log.png)
- [개발 환경](docs/screenshots/environment.png)

> 아직 스크린샷 파일을 촬영하지 않았다면 위 링크는 열리지 않는다. 반드시 본인의 실제 실행 화면을 캡처하여 추가해야 한다.

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

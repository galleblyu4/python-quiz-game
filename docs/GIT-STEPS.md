# Git 작업 실습 안내 (직접 수행해야 하는 단계)

이 프로젝트 코드는 실행 가능한 완성 예시다. 하지만 **10개 의미 있는 커밋, 브랜치 병합, clone, pull 이력은 자동으로 생기지 않는다.** 본인의 작업 과정에서 실제로 변경하고 커밋해야 한다.

## 새 저장소 연결

1. GitHub에 **새 빈 저장소**를 생성한다(기존 1차 미션 저장소와 분리).
2. VS Code에서 프로젝트 폴더를 연다.
3. 터미널에서 `git init`, `git branch -M main`, `git add .`, `git commit -m "Chore: create Python quiz project"`를 실행한다.
4. `git remote add origin <본인 저장소 HTTPS URL>`과 `git push -u origin main`을 실행한다.

## 의미 있는 커밋 10개를 남기는 방법

현재 완성본을 한 번에 커밋한다고 해서 10개의 기능별 개발 커밋이 자동으로 만들어지지 않는다. 실제로 기능을 단계별로 변경하면서 아래 작업을 수행하면 된다. 이미 존재하는 기능은 이해·검증·개선 등의 **실제 변경사항**을 만든 뒤 커밋한다.

1. 저장소 생성 및 `.gitignore` 설정
2. 메뉴 입력과 안전한 종료 개선
3. `Quiz` 클래스 및 정답 검증 개선
4. 기본 퀴즈 데이터 검토·확장
5. 별도 브랜치에서 퀴즈 풀이 기능 작업
6. 풀이 브랜치를 `main`에 병합
7. 퀴즈 추가 기능 검증·개선
8. 퀴즈 목록 기능 개선
9. 최고 점수 유지 및 출력 개선
10. JSON 저장/복구와 오류 처리 개선
11. 테스트 추가 또는 개선
12. README 문서와 실제 화면 캡처 정리

각 단계마다 `git add ...`, `git commit -m "Feat: ..."`로 진짜 변경 내역을 남긴다. 커밋 10개 이상인지 `git log --oneline --graph --all`로 확인한다.

## 브랜치 실습 예시

```bash
git checkout -b feature/quiz-play
# 실제로 해당 기능을 수정하고 테스트한다.
git add game.py
git commit -m "Feat: improve quiz play feedback"
git checkout main
git merge feature/quiz-play
git push origin main
```

## 복제 및 pull 실습

두 번째 폴더에서 실행한다. 현재 프로젝트 폴더의 **상위 디렉터리**로 이동해 명령을 실행한다.

```bash
cd ..
git clone <본인 저장소 URL> quiz-game-copy
cd quiz-game-copy
# README에 실제 학습 내용을 한 줄 추가한다.
git add README.md
git commit -m "Docs: document cloned repository test"
git push origin main
cd ../python-quiz-game
git pull origin main
git log --oneline --graph --all
```

이미 같은 경로에 `quiz-game-copy`가 있다면 다른 이름을 선택한다. 여러 작업 공간에서 동시에 변경했다면 pull 전에 현재 변경 사항을 먼저 확인한다. 실행 화면을 스크린샷으로 저장한다.

"""실제 로컬 Git 이력과 원격 설정을 docs/logs에 기록합니다.

Git 저장소 메타데이터가 있는 로컬 작업 폴더에서만 실행합니다.
이 스크립트는 Git 브랜치/커밋을 생성하거나 수정하지 않습니다.
"""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
logs = root / "docs" / "logs"
logs.mkdir(parents=True, exist_ok=True)

commands = {
    "git-history.txt": ["git", "log", "--oneline", "--graph", "--decorate", "--all", "-40"],
    "git-branches.txt": ["git", "branch", "-avv"],
    "git-remote.txt": ["git", "remote", "-v"],
    "git-reflog.txt": ["git", "reflog", "-30"],
    "git-commit-details.txt": ["git", "log", "--format=%h %s", "--stat", "-40"],
}

if not (root / ".git").exists():
    raise SystemExit("오류: .git 폴더가 있는 로컬 Git 저장소에서 실행해야 합니다.")

for name, command in commands.items():
    result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode("utf-8", errors="replace")
    if result.returncode:
        raise SystemExit(f"실패: {' '.join(command)}\n{output}")
    (logs / name).write_text("$ " + " ".join(command) + "\n" + output, encoding="utf-8")
    print(name, "저장 완료")
print("실제 Git 증빙 수집 완료")

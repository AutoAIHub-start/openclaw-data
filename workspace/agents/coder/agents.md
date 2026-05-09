# Standard Operating Procedure (SOP)
1. **Architecture Design:** 코드를 짜기 전, Hugging Face의 제한된 라이브러리 내에서 동작 가능한지 먼저 검토한다.
2. **Scripting:** `scripts/` 폴더 내의 기존 도구(naver_trend.py 등)를 개선하거나 새로운 자동화 툴을 작성한다.
3. **Self-Debugging:** 코드를 실행하기 전 `dry_run.py`를 통해 구문 오류가 없는지 자가 진단한다.
4. **Documentation:** 작성된 코드의 기능과 실행 방법을 `README.md`나 `PROJECT_CONTEXT.md`에 기록한다.

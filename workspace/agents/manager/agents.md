# Standard Operating Procedure (SOP)
1. **Request Triage:** Jack의 요청이 오면 '정보 검색(Researcher)'인지 '기술 구현(Coder)'인지 즉시 판단한다.
2. **Delegation:** `srv.agents` 명령을 사용하여 적합한 전문가에게 업무를 할당한다.
3. **Context Check:** 모든 결과물이 `PROJECT_CONTEXT.md`의 목표와 일치하는지 검수한다.
4. **Cleanup:** 작업 완료 후 생성된 임시 파일(data/*.tmp, *.json)을 삭제하는 명령을 최우선으로 실행한다.

### 박진형 · secretj

2021년 여름에 `Chapter01_JavaStart` 라는 저장소를 만들었다. Java 교재를 한 장씩 따라 치면서 챕터마다 저장소를 팠고, 그때 기록이 지금 아카이브 57개로 남아 있다.

지금은 사람이 쓰는 서버를 맡는다. 회사에서는 이미 돌아가는 서비스를 고치고 옮기고, 퇴근하면 가까운 사람이 쓸 앱을 만들어 직접 굴린다. 둘 다 만드는 시간보다 멈추지 않게 하는 시간이 길다.

그 사이에 관심이 옮겨 갔다. 새로 짓는 것보다, 오래 버티게 만드는 쪽을 잘하고 싶다.

<br>

## 하는 일

<img src="assets/backend.svg" width="880" alt="웹·앱·외부 시스템의 요청이 API 서버로 들어오고, 서버가 데이터베이스·캐시·검색·배치로 뻗었다가 응답으로 돌아나가는 구조">

- 서버 API를 만들고 고친다. 새 기능보다 운영 중인 코드를 바꾸는 일이 많다
- 데이터베이스 스키마와 쿼리를 다룬다. 느린 쿼리와 N+1을 찾아 고친다
- 배치와 스케줄러를 짠다. 중간에 끊겨도 다시 돌릴 수 있게 만든다
- 대량 데이터를 옮긴다. 옮긴 뒤에는 원본과 대조해 검증한다
- 여러 시간대에서 접속하는 서비스를 다룬다. 날짜와 시간은 요청 시간대 기준으로 처리한다
- 장애가 나면 로그와 쿼리부터 본다
- 사이드 프로젝트에서는 서버, 안드로이드·웹 클라이언트, 배포까지 직접 한다

<br>

## 작업 방식

<img src="assets/ai-flow.svg" width="880" alt="티켓에서 출발해 코드 탐색, 도메인 지식, 이슈 문서를 나눠 조사하고 계획·구현, 테스트·리뷰, 커밋·PR로 모이는 순서">

- 이슈 하나를 조사 → 계획 → 구현 → 검증 → PR 순서로 처리한다. 반복되는 절차는 Claude Code 커맨드로 묶어 둔다
- 코드를 고치기 전에 호출 관계와 영향 범위를 먼저 확인한다. 탐색은 codegraph 인덱스를 쓴다
- 조사와 리뷰는 관점을 나눠 병렬로 돌리고, 나온 결과는 직접 확인한 뒤 반영한다
- 작업하며 알아낸 도메인 지식은 문서로 남기고 저장소 `CLAUDE.md`에 붙인다
- 커밋 전 점검은 훅으로 건다
- 작업 환경 설정은 [secretj-claude-config](https://github.com/secretj/secretj-claude-config)에 올려 둔다

<br>

## 쓰는 것


<table>
<tr><td><b>서버</b></td><td>
<img src="https://img.shields.io/badge/Java-24292f?style=flat-square&logo=openjdk&logoColor=white" alt="Java">
<img src="https://img.shields.io/badge/Spring%20Boot-24292f?style=flat-square&logo=springboot&logoColor=white" alt="Spring Boot">
<img src="https://img.shields.io/badge/PHP-24292f?style=flat-square&logo=php&logoColor=white" alt="PHP">
<img src="https://img.shields.io/badge/MariaDB-24292f?style=flat-square&logo=mariadb&logoColor=white" alt="MariaDB">
<img src="https://img.shields.io/badge/MySQL-24292f?style=flat-square&logo=mysql&logoColor=white" alt="MySQL">
<img src="https://img.shields.io/badge/PostgreSQL-24292f?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Redis-24292f?style=flat-square&logo=redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/Elasticsearch-24292f?style=flat-square&logo=elasticsearch&logoColor=white" alt="Elasticsearch">
</td></tr>
<tr><td><b>앱 · 프론트</b></td><td>
<img src="https://img.shields.io/badge/Kotlin-24292f?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin">
<img src="https://img.shields.io/badge/Jetpack%20Compose-24292f?style=flat-square&logo=jetpackcompose&logoColor=white" alt="Jetpack Compose">
<img src="https://img.shields.io/badge/React-24292f?style=flat-square&logo=react&logoColor=white" alt="React">
<img src="https://img.shields.io/badge/TypeScript-24292f?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/Vite-24292f?style=flat-square&logo=vite&logoColor=white" alt="Vite">
<img src="https://img.shields.io/badge/Astro-24292f?style=flat-square&logo=astro&logoColor=white" alt="Astro">
</td></tr>
<tr><td><b>운영</b></td><td>
<img src="https://img.shields.io/badge/Docker-24292f?style=flat-square&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/GitHub%20Actions-24292f?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
<img src="https://img.shields.io/badge/nginx-24292f?style=flat-square&logo=nginx&logoColor=white" alt="nginx">
<img src="https://img.shields.io/badge/Cloudflare-24292f?style=flat-square&logo=cloudflare&logoColor=white" alt="Cloudflare">
<img src="https://img.shields.io/badge/Vercel-24292f?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">
<img src="https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white" alt="Python">
</td></tr>
<tr><td><b>작업 환경</b></td><td>
<img src="https://img.shields.io/badge/Claude%20Code-24292f?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code">
<img src="https://img.shields.io/badge/MCP-24292f?style=flat-square&logo=modelcontextprotocol&logoColor=white" alt="MCP">
<img src="https://img.shields.io/badge/Obsidian-24292f?style=flat-square&logo=obsidian&logoColor=white" alt="Obsidian">
<img src="https://img.shields.io/badge/Jira-24292f?style=flat-square&logo=jira&logoColor=white" alt="Jira">
<img src="https://img.shields.io/badge/IntelliJ%20IDEA-24292f?style=flat-square&logo=intellijidea&logoColor=white" alt="IntelliJ IDEA">
</td></tr>
</table>

<br>

## 기록

<img src="assets/stats.svg" width="880" alt="지난 1년 컨트리뷰션 1,678건, 유지 중인 저장소 12개, 아카이브 57개, 언어 비중 Java 46% TypeScript 27% Kotlin 14%">

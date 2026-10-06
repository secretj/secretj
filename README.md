### 박진형 · secretj

**백엔드 개발자.** 메일과 그룹웨어 서버를 만든다. 새로 짓는 일보다, 이미 돌고 있는 걸 멈추지 않게 고치고 옮기는 일이 많다.

<br>

## 하는 일

<img src="assets/pipeline.svg" width="880" alt="메일 한 통이 수신·발송에서 검사·필터, 파싱·인덱싱, 보관·이관을 거쳐 검색·조회에 닿는 경로">

- 메일 수신·발송, 검색 인덱싱, 보관함 이관처럼 사용자 눈에는 잘 안 보이는 구간을 맡는다
- `Java` · `Spring Boot`가 주력이고, 오래 돌아가는 `PHP` 레거시도 같이 본다
- 여러 나라에서 접속하는 서비스라, 날짜·시간은 KST 고정이 아니라 요청 타임존 기준으로 다룬다
- 대량 데이터 이관은 중단·재개·검증이 되게 설계한다. 한 번에 끝나는 마이그레이션은 믿지 않는다
- 사이드 프로젝트에서는 기획부터 Android·웹 클라이언트, 배포·운영까지 혼자 한다

<br>

## AI를 쓰는 방식

<img src="assets/ai-flow.svg" width="880" alt="티켓에서 출발해 코드 탐색·도메인 지식·이슈 문서를 서브에이전트로 병렬 조사하고, 계획·구현, 테스트·리뷰, 커밋·PR 로 모이는 작업 루프">

- Claude Code가 기본 작업 환경이다. 조사 → 계획 → 구현 → 검증 → PR을 커맨드와 스킬로 고정해 두고 매번 같은 순서로 돌린다
- 코드 탐색은 grep 반복 대신 **codegraph** 인덱스로 호출 관계와 변경 영향을 먼저 본다
- 조사·리뷰는 역할별 서브에이전트(기획 · 개발 · QA · 보안 · 인프라)를 병렬로 띄우고, 엇갈리는 의견은 내가 정리한다
- 세션에서 알게 된 도메인 지식은 Obsidian에 쌓고 저장소 `CLAUDE.md`로 내려, 다음 사람이 같은 걸 다시 캐지 않게 한다
- 훅으로 커밋 전 점검을 걸어 둔다. 테스트를 건너뛴 채로 넘어가지 않게
- 설정은 [secretj-claude-config](https://github.com/secretj/secretj-claude-config)에 공개해 둔다

> 초안은 AI가 만들고, 도메인 판단과 책임은 내가 진다.

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

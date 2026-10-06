### 박진형 · secretj

구조적으로 단단하면서도 나중에 확장하기 좋은, 유연한 코드를 만드는 데 힘을 쏟고 있습니다.

기능 하나 붙일 때마다 여기저기 손대야 한다면 구조가 잘못 잡힌 거라고 생각해요.

<br>

## 하는 일

<img src="assets/backend.svg" width="880" alt="웹과 앱에서 들어온 요청이 API 서버를 거쳐 데이터베이스, 캐시, 검색, 정해진 시간에 도는 작업으로 퍼졌다가 다시 돌아나가는 구조">

- 이미 돌아가고 있는 서비스를 고치고, 멈추지 않게 지킵니다
- 데이터가 어디에 어떻게 쌓일지 정하고, 느려지면 원인을 찾습니다
- 사람이 보지 않는 시간에도 돌아야 하는 작업을 만듭니다
- 쌓인 데이터를 다른 곳으로 옮기고, 옮긴 뒤에 맞는지 하나씩 맞춰 봅니다
- 문제가 생기면 원인을 찾을 때까지 들여다봅니다
- 혼자 하는 프로젝트에서는 서버부터 화면, 배포까지 전부 직접 합니다

<br>

## 작업 방식

<img src="assets/ai-flow.svg" width="880" alt="할 일 하나를 받으면 코드 찾아보기, 적어 둔 메모, 이슈와 문서를 나눠 살펴본 뒤 계획과 구현, 테스트와 리뷰, 커밋과 PR로 이어지는 순서">

- 할 일 하나를 받으면 찾아보고 → 계획하고 → 고치고 → 확인하고 → 올립니다. 매번 같은 순서로 합니다
- 코드를 고치기 전에 어디까지 영향이 가는지 먼저 봅니다
- 찾아보는 일은 여러 갈래로 나눠 동시에 돌리고, 나온 결과는 직접 확인한 뒤에 씁니다
- 작업하다 알게 된 건 메모로 남겨 둡니다. 다음에 같은 걸 또 찾지 않으려고요
- 자주 하는 일은 Claude Code 커맨드로 묶어 두고, 커밋 전 점검도 자동으로 걸어 둡니다
- 쓰는 설정은 [secretj-claude-config](https://github.com/secretj/secretj-claude-config)에 올려 뒀습니다

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

## 지금까지

<img src="assets/stats.svg" width="880" alt="지난 1년 활동 1,678건, 지금 쓰는 저장소 12개, 예전에 만든 저장소 57개, 주로 쓰는 언어 Java 46% TypeScript 27% Kotlin 14%">

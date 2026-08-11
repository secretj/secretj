### 박진형 · secretj

백엔드를 주로 다루지만, 서비스 하나를 서버부터 화면·배포·운영까지 혼자 굴리는 쪽을 좋아한다.
평일에는 그룹웨어 메일 서비스 백엔드를, 그 밖의 시간에는 아래 두 개를 만들고 있다.

<br>

## 지금 만드는 것

<table>
<tr>
<td width="76" valign="top" align="center"><img src="assets/checky-icon.png" width="56" alt=""></td>
<td valign="top">

**체키 (Checky)** · [hichecky.com](https://hichecky.com)

가까운 사람끼리 **소식 · 체크리스트 · 살림 · 기념일**을 한곳에서 나누는 비공개 그룹 PWA.
2인 그룹이 기본이고, 카드 결제 알림을 읽어 가계부에 그대로 꽂아준다. 기념일은 1주 전에 알려준다.

`Java 21` `Spring Boot 3.4` `MariaDB` `Flyway` `React 18` `TypeScript` `Vite` `Docker Compose` `Cloudflare Tunnel`

</td>
</tr>
</table>

<p align="center">
  <img src="assets/checky-memory.png" width="30%" alt="소식">
  <img src="assets/checky-checklist.png" width="30%" alt="체크리스트">
  <img src="assets/checky-household.png" width="30%" alt="살림 가계부">
</p>

<table>
<tr>
<td width="76" valign="top" align="center"><img src="assets/poomasi-icon.png" width="56" alt=""></td>
<td valign="top">

**품앗이** · Google Play 비공개 테스트 중

축의금·부의금 같은 **경조사비를 기록하는 로컬 우선(local-first) 안드로이드 앱**.
데이터는 기기 밖으로 나가지 않는다 — DB를 통째로 암호화하고, 서버 동기화 대신 자동 로컬 백업과 CSV 복구를 쓴다.
연락처 가져오기, 결제 알림 매칭, 기프티콘 촬영 인식까지 기록 부담을 줄이는 쪽에 붙였다.

`Kotlin` `Jetpack Compose` `Room` `SQLCipher` `Android Keystore` `Play Billing`

</td>
</tr>
</table>

<br>

## 그 외

| | |
|---|---|
| **[promptfit](https://github.com/secretj/promptfit)** | 프롬프트·업무 규칙을 claude.ai / ChatGPT / Claude Code 각 환경에 맞는 파일로 만들어 주는 카탈로그 · `Astro` `Cloudflare Pages` `D1` |
| **[ot-job](https://github.com/secretj/ot-job)** | 서울 지역 작업치료 채용 공고를 수집해 카카오톡으로 알려주는 멀티유저 웹앱 · `Python` `Flask` `APScheduler` |
| **[Lien](https://github.com/secretj/Lien)** | Spring Boot 기반 JWT 인증 시스템 · `Spring Security` `Redis` `MySQL` |
| **[Discord-pubg-bot](https://github.com/secretj/Discord-pubg-bot)** | 배틀그라운드 랭크에 따라 디스코드 역할을 자동 부여하는 봇 · `Kotlin` |
| **[secretj-claude-config](https://github.com/secretj/secretj-claude-config)** | Claude Code 개인 설정 — skills / hooks |

<br>

## 주로 쓰는 것

**서버** Java · Spring Boot · JPA · MariaDB / MySQL · Redis · Flyway
**앱·프론트** Kotlin · Jetpack Compose · React · TypeScript · Vite · PWA
**운영** Docker Compose · GitHub Actions · nginx · Cloudflare · Python

<br>

<sub>2021~2022년 학습·실습 저장소는 아카이브로 옮겨 뒀다.</sub>

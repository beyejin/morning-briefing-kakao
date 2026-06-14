# Morning Briefing Kakao Bot

매일 아침 날씨, 대기질, Google Calendar 일정, 오늘의 뉴스, 옷 추천, 랜덤 아침 확언을 모아서 카카오톡 나에게 보내기로 전송하는 Python 프로젝트입니다.

## 기능

- OpenWeather 날씨: 현재 온도, 체감온도, 최저/최고 온도, 강수 가능성, 바람
- OpenWeather 대기질: AQI, PM10, PM2.5
- Google Calendar: 비공개 ICS URL로 오늘 일정 조회
- RSS 뉴스: 기본값은 Google News 한국 RSS
- 옷 추천: 체감/최저기온, 비, 바람, 대기질 기반 규칙
- 카카오톡: Kakao Message API `send me` endpoint 사용

## 로컬 테스트

```bash
python3 -m unittest discover -s tests
DRY_RUN=true python3 -m morning_briefing.main
```

## 환경 변수

`.env.example`을 참고해서 GitHub Secrets에 아래 값을 넣습니다.

- `LATITUDE`: 위도
- `LONGITUDE`: 경도
- `BRIEFING_LATITUDE`: iPhone 단축어가 보낸 현재 위도. GitHub Secret으로 넣지 않아도 됩니다.
- `BRIEFING_LONGITUDE`: iPhone 단축어가 보낸 현재 경도. GitHub Secret으로 넣지 않아도 됩니다.
- `OPENWEATHER_API_KEY`: OpenWeather API 키
- `GOOGLE_CALENDAR_ICS_URL`: Google Calendar 비공개 iCal 주소
- `KAKAO_ACCESS_TOKEN`: 카카오 로그인으로 발급받은 액세스 토큰
- `RSS_FEEDS`: 쉼표로 구분한 RSS URL 목록. 비워두면 Google News 한국 RSS 사용

## Google Calendar ICS URL

Google Calendar 설정에서 원하는 캘린더의 "비공개 주소 iCal 형식" URL을 복사해 `GOOGLE_CALENDAR_ICS_URL`로 넣으면 됩니다. 이 URL은 비밀값이라 공개 저장소에 직접 커밋하면 안 됩니다.

## Kakao 설정

Kakao Developers에서 앱을 만들고 카카오 로그인을 활성화한 뒤, 동의항목에서 `talk_message` 권한을 설정해야 합니다. 이 프로젝트는 공식 `https://kapi.kakao.com/v2/api/talk/memo/default/send` endpoint로 나에게 보내기를 호출합니다.

액세스 토큰은 만료되므로 운영 단계에서는 refresh token으로 갱신하는 작업을 추가하는 것이 좋습니다. 첫 버전은 `KAKAO_ACCESS_TOKEN`을 Secrets에 넣어 바로 전송할 수 있게 구성되어 있습니다.

## GitHub Actions

`.github/workflows/morning-briefing.yml`은 매일 UTC 21:30, 한국 시간 06:30에 실행됩니다. GitHub UI에서 `workflow_dispatch`로 수동 실행도 가능합니다.

iPhone 단축어에서 현재 위치를 보내 실행하려면 [iPhone Shortcut Setup](docs/iphone-shortcut.md)을 참고합니다. 단축어가 보낸 위치가 있으면 그 좌표를 사용하고, 없으면 GitHub Secrets의 `LATITUDE`와 `LONGITUDE`를 사용합니다.

# Morning Briefing Design

## Goal

Build a scheduled morning briefing that gathers weather, air quality, calendar events, news headlines, a random affirmation, and an outfit recommendation, then sends the summary to the user's KakaoTalk "My Chatroom".

## Architecture

The project uses a small Python command-line app because Python is the simplest fit for scheduled API orchestration and Kakao messaging. The app is split into focused modules: weather, calendar, news, outfit rules, formatting, and Kakao delivery.

GitHub Actions runs the app every morning. Secrets hold API keys and private URLs. The first calendar implementation supports a private Google Calendar ICS URL because it is easier and safer to automate than a full OAuth refresh-token flow.

## Data Flow

1. Load settings from environment variables.
2. Fetch OpenWeather current/daily weather and air pollution.
3. Fetch today's events from a Google Calendar private ICS URL.
4. Fetch headlines from RSS feeds.
5. Select one affirmation from a local list.
6. Choose an outfit recommendation from temperature, rain, wind, and air quality.
7. Format a concise Korean briefing.
8. Send the text to KakaoTalk using the official "send me" message API.

## Error Handling

External data fetches are best-effort. Missing weather, calendar, or news data should not stop the entire briefing unless Kakao delivery is explicitly requested and fails. The message includes available sections and omits unavailable details.

## Testing

Unit tests cover the deterministic core: outfit recommendation, ICS event parsing, and message formatting. Network calls are kept behind small functions so they can be tested later with fixtures without touching live APIs.

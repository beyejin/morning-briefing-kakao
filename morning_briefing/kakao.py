from __future__ import annotations

import json

from morning_briefing.http import post_form

KAKAO_SEND_ME_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def send_to_me(access_token: str, text: str) -> None:
    for chunk in _chunks(text, 190):
        template = {
            "object_type": "text",
            "text": chunk,
            "link": {
                "web_url": "https://calendar.google.com/calendar",
                "mobile_web_url": "https://calendar.google.com/calendar",
            },
            "button_title": "캘린더 보기",
        }
        response = post_form(KAKAO_SEND_ME_URL, access_token, {"template_object": json.dumps(template, ensure_ascii=False)})
        if response.get("result_code", 0) != 0:
            raise RuntimeError(f"Kakao send failed: {response}")


def _chunks(text: str, max_size: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for line in text.splitlines():
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) <= max_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        current = line
    if current:
        chunks.append(current)
    return chunks


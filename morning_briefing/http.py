from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class HttpError(RuntimeError):
    pass


def get_json(url: str, params: dict[str, object] | None = None) -> dict:
    full_url = _with_params(url, params)
    text = get_text(full_url)
    return json.loads(text)


def get_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "morning-briefing/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise HttpError(f"GET failed: {url}") from exc


def post_form(url: str, token: str, data: dict[str, str]) -> dict:
    body = urlencode(data).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "User-Agent": "morning-briefing/1.0",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except (HTTPError, URLError, TimeoutError) as exc:
        raise HttpError(f"POST failed: {url}") from exc


def _with_params(url: str, params: dict[str, object] | None) -> str:
    if not params:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urlencode(params)}"


from __future__ import annotations

import xml.etree.ElementTree as ET

from morning_briefing.http import HttpError, get_text
from morning_briefing.models import NewsItem


def fetch_news(feed_urls: list[str], limit: int = 5) -> list[NewsItem]:
    items: list[NewsItem] = []
    for url in feed_urls:
        if len(items) >= limit:
            break
        try:
            text = get_text(url)
        except HttpError:
            continue
        items.extend(_parse_rss(text, limit - len(items)))
    return items[:limit]


def _parse_rss(text: str, limit: int) -> list[NewsItem]:
    root = ET.fromstring(text)
    result: list[NewsItem] = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title:
            result.append(NewsItem(title=title, link=link))
        if len(result) >= limit:
            break
    return result


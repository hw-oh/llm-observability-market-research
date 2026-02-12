from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup, Tag

from intel_bot.models import FeedEntry

_BEAMER_API_URL = "https://app.getbeamer.com/loadMoreNews"
_DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(\d{1,2}),\s+(\d{4})"
)
_MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}

MAX_PAGES = 3
MAX_ENTRIES = 20


def _parse_date(text: str) -> str | None:
    m = _DATE_RE.search(text)
    if not m:
        return None
    month = _MONTH_MAP[m.group(1)]
    day = int(m.group(2))
    year = int(m.group(3))
    return f"{year:04d}-{month:02d}-{day:02d}"


def _parse_entries(html: str, category_filter: str = "weave") -> list[FeedEntry]:
    soup = BeautifulSoup(html, "html.parser")
    entries: list[FeedEntry] = []

    css_class = f"category_{category_filter}"
    for div in soup.find_all("div", class_="feature"):
        if not isinstance(div, Tag):
            continue
        classes = div.get("class", [])
        if css_class not in classes:
            continue

        title_tag = div.find("h3", class_="featureTitle")
        title = title_tag.get_text(strip=True) if title_tag else ""

        date_tag = div.find("div", class_="featureDate")
        published = _parse_date(date_tag.get_text() if date_tag else "")

        content_tag = div.find("div", class_="featureContent")
        summary = content_tag.get_text(strip=True)[:2000] if content_tag else ""

        link = ""
        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag and isinstance(a_tag, Tag):
                link = a_tag.get("href", "") or ""
                if isinstance(link, list):
                    link = link[0] if link else ""

        if title:
            entries.append(
                FeedEntry(
                    source="beamer",
                    title=title,
                    link=link,
                    published=published,
                    summary=summary,
                )
            )

    return entries


async def fetch_beamer_changelog(
    app_id: str,
    category_filter: str = "weave",
) -> list[FeedEntry]:
    all_entries: list[FeedEntry] = []

    async with httpx.AsyncClient(follow_redirects=True) as client:
        for page in range(MAX_PAGES):
            try:
                resp = await client.get(
                    _BEAMER_API_URL,
                    params={"app_id": app_id, "page": page},
                    timeout=30,
                )
                resp.raise_for_status()
            except Exception as e:
                print(f"  [warn] Beamer fetch failed (page {page}): {e}")
                break

            entries = _parse_entries(resp.text, category_filter)
            all_entries.extend(entries)

            if len(resp.text.strip()) < 100:
                break

    return all_entries[:MAX_ENTRIES]

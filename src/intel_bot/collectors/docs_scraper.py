from __future__ import annotations

from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from intel_bot.config import CompetitorConfig
from intel_bot.models import DocsPage

MAX_CONTENT_LENGTH = 50_000


async def scrape_docs(url: str) -> DocsPage:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, timeout=30)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup.find_all(["nav", "footer", "header", "script", "style"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else url
    content = soup.get_text(separator="\n", strip=True)

    if len(content) > MAX_CONTENT_LENGTH:
        content = content[:MAX_CONTENT_LENGTH]

    return DocsPage(
        url=url,
        title=title,
        content=content,
        fetched_at=datetime.now(),
    )


async def scrape_competitor_docs(
    competitor: CompetitorConfig,
) -> list[DocsPage]:
    urls = [competitor.docs_url]
    if competitor.changelog_url and not competitor.changelog_url.endswith(
        (".rss", ".xml", ".atom")
    ):
        urls.append(competitor.changelog_url)

    pages: list[DocsPage] = []
    for url in urls:
        try:
            page = await scrape_docs(url)
            pages.append(page)
        except Exception as e:
            print(f"  [warn] Scraping failed for {url}: {e}")
            pages.append(
                DocsPage(
                    url=url,
                    title="(fetch failed)",
                    content="",
                    fetched_at=datetime.now(),
                )
            )
    return pages

from __future__ import annotations

from time import struct_time

import feedparser

from intel_bot.config import CompetitorConfig
from intel_bot.models import FeedEntry

MAX_ENTRIES = 10


def _format_date(t: struct_time | None) -> str | None:
    if t is None:
        return None
    return f"{t.tm_year:04d}-{t.tm_mon:02d}-{t.tm_mday:02d}"


def fetch_github_releases(repo: str) -> list[FeedEntry]:
    url = f"https://github.com/{repo}/releases.atom"
    feed = feedparser.parse(url)

    entries: list[FeedEntry] = []
    for item in feed.entries[:MAX_ENTRIES]:
        entries.append(
            FeedEntry(
                source="github",
                title=item.get("title", ""),
                link=item.get("link", ""),
                published=_format_date(item.get("published_parsed")),
                summary=item.get("summary", "")[:500],
            )
        )
    return entries


def fetch_pypi_releases(package: str) -> list[FeedEntry]:
    url = f"https://pypi.org/rss/project/{package}/releases.xml"
    feed = feedparser.parse(url)

    entries: list[FeedEntry] = []
    for item in feed.entries[:MAX_ENTRIES]:
        entries.append(
            FeedEntry(
                source="pypi",
                title=item.get("title", ""),
                link=item.get("link", ""),
                published=_format_date(item.get("published_parsed")),
                summary=item.get("summary", "")[:500],
            )
        )
    return entries


def _is_rss_url(url: str) -> bool:
    return url.endswith((".rss", ".xml", ".atom"))


def fetch_changelog_rss(url: str) -> list[FeedEntry]:
    feed = feedparser.parse(url)

    entries: list[FeedEntry] = []
    for item in feed.entries[:MAX_ENTRIES]:
        entries.append(
            FeedEntry(
                source="changelog",
                title=item.get("title", ""),
                link=item.get("link", ""),
                published=_format_date(item.get("published_parsed")),
                summary=item.get("summary", "")[:500],
            )
        )
    return entries


def fetch_competitor_feeds(competitor: CompetitorConfig) -> list[FeedEntry]:
    all_entries: list[FeedEntry] = []

    if competitor.github_repo:
        try:
            all_entries.extend(fetch_github_releases(competitor.github_repo))
        except Exception as e:
            print(f"  [warn] GitHub feed failed for {competitor.github_repo}: {e}")

    if competitor.pypi_package:
        try:
            all_entries.extend(fetch_pypi_releases(competitor.pypi_package))
        except Exception as e:
            print(f"  [warn] PyPI feed failed for {competitor.pypi_package}: {e}")

    if competitor.changelog_url and _is_rss_url(competitor.changelog_url):
        try:
            all_entries.extend(fetch_changelog_rss(competitor.changelog_url))
        except Exception as e:
            print(f"  [warn] Changelog RSS failed for {competitor.changelog_url}: {e}")

    return all_entries

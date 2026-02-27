"""Markdown translation module (Gemini Flash via OpenRouter)."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from pathlib import Path

import weave
from openai import OpenAI

from intel_bot.config import LANGUAGE_NAMES, SUPPORTED_LANGS, Settings

logger = logging.getLogger(__name__)

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5

_TRANSLATION_PROMPT = """\
Translate the following Markdown document from English to {target_language_name}.

Rules:
- Preserve ALL Markdown formatting (headers, tables, lists, bold, links, blockquotes, frontmatter)
- Preserve ALL relative URLs in links — translate link text only, never URL paths
- Preserve YAML frontmatter (---) but translate the 'title' value
- Preserve rating symbols (●●●, ●●○, ●○○, ○○○) without change
- Preserve product names: Weave, LangSmith, Arize Phoenix, Braintrust, Langfuse, MLflow
- Preserve table structure (|, ---, alignment)
- Keep English terms where Korean translations sound unnatural:
  Tracing, Observability, SDK, API, Dashboard, Eval, Fine-tuning, Streaming, Scoring
- Do NOT translate into obscure Sino-Korean (한자어); prefer the English original
  when it is more commonly used in the Korean AI/ML community
- Use standard {target_language_name} translations for technical terms
- Output ONLY the translated markdown

Document:
{content}
"""


@weave.op()
def translate_content(
    client: OpenAI,
    model: str,
    content: str,
    target_lang: str,
) -> str:
    """Translate a single markdown document. Includes retry logic."""
    target_language_name = LANGUAGE_NAMES[target_lang]

    prompt = _TRANSLATION_PROMPT.format(
        target_language_name=target_language_name,
        content=content,
    )

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a professional translator. "
                            f"Translate Markdown documents from English to {target_language_name}. "
                            f"Preserve all formatting exactly."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=16384,
            )
            result = response.choices[0].message.content or ""
            # Strip markdown fences if the model wraps the output
            text = result.strip()
            if text.startswith("```"):
                first_newline = text.index("\n")
                text = text[first_newline + 1:]
            if text.endswith("```"):
                text = text[:text.rfind("```")]
            return text.strip()

        except Exception as e:
            last_error = e
            logger.warning(
                "Translation attempt %d/%d for %s failed: %s",
                attempt,
                _MAX_ATTEMPTS,
                target_lang,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to translate to {target_lang} after {_MAX_ATTEMPTS} attempts: {last_error}"
    )


def translate_all_reports(
    settings: Settings,
    english_paths: dict[str, Path],
    on_progress: Callable[[str, str], None] | None = None,
) -> dict[str, list[Path]]:
    """Translate English reports to ko/ja. Returns {lang: [paths]}."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key.get_secret_value(),
    )
    model = settings.translation_model

    result: dict[str, list[Path]] = {}

    for lang in SUPPORTED_LANGS:
        lang_paths: list[Path] = []

        for key, en_path in english_paths.items():
            if on_progress:
                on_progress(lang, key)

            content = en_path.read_text(encoding="utf-8")
            translated = translate_content(client, model, content, lang)

            # Determine output path: lang/relative_path
            out_path = Path(lang) / en_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(translated, encoding="utf-8")
            lang_paths.append(out_path)

        result[lang] = lang_paths

    return result

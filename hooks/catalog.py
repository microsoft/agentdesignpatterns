from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

import yaml
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils import get_relative_url

ARTICLE_TYPES = {
    "pattern": {
        "directory": "patterns",
        "sections": ["Description", "Applicability", "Implementation", "References"],
        "title": "Patterns",
    },
    "anti-pattern": {
        "directory": "anti-patterns",
        "sections": ["Description", "Issue", "Implementation", "References"],
        "title": "Anti-Patterns",
    },
}
INDEX_MARKER = re.compile(r"<!-- catalog-index:(all|pattern|anti-pattern) -->")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECOND_LEVEL_HEADING = re.compile(r"^## (.+)$", re.MULTILINE)

_articles: dict[str, dict[str, Any]] = {}


def on_config(config: Any) -> Any:
    global _articles
    _articles = {}
    docs_dir = Path(config.docs_dir)

    for article_type, rules in ARTICLE_TYPES.items():
        article_dir = docs_dir / rules["directory"]
        for path in sorted(article_dir.glob("*.md")):
            if path.name == "index.md":
                continue

            metadata, body = _read_article(path)
            _validate_article(path, metadata, body, article_type, rules["sections"])
            article_id = metadata["id"]
            if article_id in _articles:
                other = _articles[article_id]["src_uri"]
                raise PluginError(
                    f"{path}: duplicate article id '{article_id}' (also used by {other})"
                )

            _articles[article_id] = {
                **metadata,
                "src_uri": path.relative_to(docs_dir).as_posix(),
            }

    for article in _articles.values():
        for related_id in article["related"]:
            if related_id not in _articles:
                raise PluginError(
                    f"{article['src_uri']}: related article '{related_id}' does not exist"
                )
            if related_id == article["id"]:
                raise PluginError(
                    f"{article['src_uri']}: an article cannot relate to itself"
                )

    return config


def on_page_markdown(
    markdown: str, page: Page, config: Any, files: Files
) -> str:
    markdown = INDEX_MARKER.sub(
        lambda match: _render_index(match.group(1), page, files), markdown
    )

    article_id = page.meta.get("id")
    article = _articles.get(article_id)
    if article is None:
        return markdown

    caption = f'<p class="article-caption">{html.escape(article["description"])}</p>'
    markdown = re.sub(
        r"^(# .+)$",
        rf"\1\n\n{caption}",
        markdown,
        count=1,
        flags=re.MULTILINE,
    )

    if article["related"]:
        markdown = f"{markdown.rstrip()}\n\n{_render_related(article, page, files)}\n"

    return markdown


def _read_article(path: Path) -> tuple[dict[str, Any], str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise PluginError(f"{path}: article must start with YAML frontmatter")

    parts = content.split("---\n", 2)
    if len(parts) != 3:
        raise PluginError(f"{path}: YAML frontmatter is not closed")

    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as error:
        raise PluginError(f"{path}: invalid YAML frontmatter: {error}") from error

    if not isinstance(metadata, dict):
        raise PluginError(f"{path}: YAML frontmatter must be a mapping")

    return metadata, parts[2]


def _validate_article(
    path: Path,
    metadata: dict[str, Any],
    body: str,
    article_type: str,
    expected_sections: list[str],
) -> None:
    required = {"id", "title", "description", "type", "category", "tags", "related"}
    missing = sorted(required - metadata.keys())
    if missing:
        raise PluginError(f"{path}: missing frontmatter keys: {', '.join(missing)}")

    article_id = metadata["id"]
    if not isinstance(article_id, str) or not ID_PATTERN.fullmatch(article_id):
        raise PluginError(f"{path}: id must use lowercase kebab-case")

    for key in ("title", "description", "category"):
        if not isinstance(metadata[key], str) or not metadata[key].strip():
            raise PluginError(f"{path}: {key} must be a non-empty string")

    if metadata["type"] != article_type:
        raise PluginError(f"{path}: type must be '{article_type}'")

    for key in ("tags", "related"):
        value = metadata[key]
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            raise PluginError(f"{path}: {key} must be an array of non-empty strings")

    headings = SECOND_LEVEL_HEADING.findall(body)
    if headings != expected_sections:
        expected = ", ".join(expected_sections)
        actual = ", ".join(headings) or "none"
        raise PluginError(
            f"{path}: level-two sections must be exactly [{expected}]; found [{actual}]"
        )


def _render_index(index_type: str, page: Page, files: Files) -> str:
    article_types = (
        ARTICLE_TYPES.keys() if index_type == "all" else (index_type,)
    )
    sections: list[str] = []

    for article_type in article_types:
        matching = [
            article
            for article in _articles.values()
            if article["type"] == article_type
        ]
        if not matching:
            continue

        if index_type == "all":
            sections.append(f"## {ARTICLE_TYPES[article_type]['title']}")

        categories = sorted({article["category"] for article in matching})
        for category in categories:
            heading = "###" if index_type == "all" else "##"
            sections.append(f"{heading} {category}")
            for article in sorted(
                (item for item in matching if item["category"] == category),
                key=lambda item: item["title"],
            ):
                target = files.get_file_from_path(article["src_uri"])
                url = get_relative_url(target.src_uri, page.file.src_uri)
                sections.append(
                    f"- [{article['title']}]({url}) — {article['description']}"
                )

    return "\n\n".join(sections)


def _render_related(article: dict[str, Any], page: Page, files: Files) -> str:
    lines = ["## Related"]
    for related_id in article["related"]:
        related = _articles[related_id]
        target = files.get_file_from_path(related["src_uri"])
        url = get_relative_url(target.src_uri, page.file.src_uri)
        lines.append(f"- [{related['title']}]({url}) — {related['description']}")
    return "\n".join(lines)

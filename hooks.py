"""Build hooks for the site.

Reads topics.yml once, then:

- puts a "Human reviewed" mark under the title of every page whose front
  matter has `human_reviewed: <date>`: a person has read the page in full.
  It says nothing about whether an idea is settled; every idea is still
  open;
- replaces the line `<!-- board -->` with the table of every talking point;
- fails the build when a page names a topic that topics.yml does not list,
  or a topic carries a level or destination that is not defined.
"""

from __future__ import annotations

import os

import yaml
from mkdocs.exceptions import PluginError

_DATA: dict = {}


def _load(config) -> dict:
    path = os.path.join(os.path.dirname(config.config_file_path), "topics.yml")
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    levels = data["levels"]
    destinations = data["destinations"]
    packages = data["packages"]
    seen = set()
    for topic in data["topics"]:
        slug = topic["slug"]
        if slug in seen:
            raise PluginError(f"topics.yml lists {slug} twice.")
        seen.add(slug)
        for field in ("maturity", "proposed"):
            value = topic.get(field)
            if value is not None and value not in levels:
                raise PluginError(f"topics.yml: {slug} has {field} {value!r}, which is not a level.")
        if topic["destination"] not in destinations:
            raise PluginError(f"topics.yml: {slug} has destination {topic['destination']!r}, which is not defined.")
        if topic["package"] not in packages:
            raise PluginError(f"topics.yml: {slug} has package {topic['package']!r}, which is not defined.")
    data["by_slug"] = {topic["slug"]: topic for topic in data["topics"]}
    return data


def on_config(config):
    _DATA.clear()
    _DATA.update(_load(config))
    return config


def _badge(level: str | None, proposed: str | None) -> str:
    levels = _DATA["levels"]
    if level:
        return f'<span class="level level-{level}">{levels[level]["label"]}</span>'
    if proposed:
        return (
            '<span class="level level-unrated">Not yet rated</span> '
            f'<span class="level-proposed">proposed: {levels[proposed]["label"]}</span>'
        )
    return '<span class="level level-unrated">Not yet rated</span>'


def _link(page_file: str, target: str) -> str:
    """Writes a link from one docs file to another, relative to the first."""
    if target.startswith(("http://", "https://")):
        return target
    path, _, anchor = target.partition("#")
    rel = os.path.relpath(path, os.path.dirname(page_file) or ".")
    return rel + (f"#{anchor}" if anchor else "")


def _board(page_file: str) -> str:
    lines = []
    for key, package in _DATA["packages"].items():
        topics = [t for t in _DATA["topics"] if t["package"] == key]
        if not topics:
            continue
        lines.append(f"### {package['label']}\n")
        if package.get("summary"):
            lines.append(package["summary"] + "\n")
        lines.append("| Talking point | Maturity | Destination | Owner |")
        lines.append("|---|---|---|---|")
        for topic in topics:
            title = topic["title"]
            if topic.get("page"):
                title = f"[{title}]({_link(page_file, topic['page'])})"
            owner = topic.get("owner") or "open"
            destination = _DATA["destinations"][topic["destination"]]["label"]
            badge = _badge(topic.get("maturity"), topic.get("proposed"))
            lines.append(f"| {title} | {badge} | {destination} | {owner} |")
        lines.append("")
    return "\n".join(lines)


def _human_reviewed(date) -> str:
    return (
        '<div class="human-reviewed"><span class="human-reviewed-box" aria-hidden="true">&#x2611;</span> '
        f"<strong>Human reviewed</strong> {date}</div>\n"
    )


def _under_title(markdown: str, block: str) -> str:
    lines = markdown.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(index + 1, "\n" + block)
            break
    else:
        lines.insert(0, block)
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files):
    if "<!-- board -->" in markdown:
        markdown = markdown.replace("<!-- board -->", _board(page.file.src_uri))
    reviewed = page.meta.get("human_reviewed")
    slug = page.meta.get("topic")
    if slug:
        topic = _DATA["by_slug"].get(slug)
        if topic is None:
            raise PluginError(f"{page.file.src_uri} names topic {slug!r}, which topics.yml does not list.")
    if reviewed:
        markdown = _under_title(markdown, _human_reviewed(reviewed))
    return markdown

#!/usr/bin/env python3
"""Build script: reads markdown content files and generates index.html."""

import hashlib
import re
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"

INLINE_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown text. Returns (metadata dict, body string)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta = {}
    for line in match.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'")
        meta[key.strip()] = value
    return meta, match.group(2).strip()


def inline_md(text):
    """Escape HTML, then convert inline markdown: [text](url) links and **bold**."""
    text = escape(text)
    text = INLINE_LINK_RE.sub(
        r'<a href="\2" target="_blank" rel="noopener">\1</a>', text
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(text):
    """Minimal markdown to HTML: ## headings, paragraphs, line breaks, and inline links."""
    paragraphs = re.split(r"\n{2,}", text.strip())
    parts = []
    for p in paragraphs:
        if p.startswith("## "):
            parts.append(f"<h2>{inline_md(p[3:].strip())}</h2>")
            continue
        p = inline_md(p)
        # Convert single newlines to <br>
        p = p.replace("\n", "<br>\n")
        parts.append(f"<p>{p}</p>")
    return "\n".join(parts)


def load_hero():
    """Load hero section content."""
    hero_file = CONTENT_DIR / "hero.md"
    meta, body = parse_frontmatter(hero_file.read_text())
    return meta.get("title", ""), md_to_html(body)


def load_portfolio():
    """Load portfolio cards from content/portfolio/, sorted by filename."""
    portfolio_dir = CONTENT_DIR / "portfolio"
    cards = []
    for md_file in sorted(portfolio_dir.glob("*.md")):
        meta, body = parse_frontmatter(md_file.read_text())
        cards.append({
            "title": meta.get("title", "Untitled"),
            "tag": meta.get("tag", ""),
            "image": meta.get("image", ""),
            "link": meta.get("link", "#"),
            "link_text": meta.get("link_text", "View Project"),
            "description": body,
        })
    return cards


def render_card(card, number):
    """Render a single portfolio card as HTML. `number` is the race-plate number."""
    title = escape(card["title"])
    tag = escape(card["tag"])
    description = inline_md(card["description"])
    link = escape(card["link"])
    link_text = escape(card["link_text"])
    plate = f"{number:02d}"

    if card["image"]:
        media_html = (
            f'<img src="{escape(card["image"])}" class="ride-card__img" '
            f'alt="Screenshot of {title}" loading="lazy">'
        )
    else:
        media_html = (
            '<div class="ride-card__img ride-card__img--empty" aria-hidden="true">'
            '<i class="bi bi-bicycle"></i>'
            "</div>"
        )

    tag_html = f'\n                            <p class="ride-card__tag">{tag}</p>' if tag else ""

    return f"""                <div class="col-md-6 col-lg-4 reveal">
                    <article class="ride-card">
                        <div class="ride-card__media">
                            {media_html}
                            <span class="ride-card__plate" aria-hidden="true">{plate}</span>
                        </div>
                        <div class="ride-card__body">{tag_html}
                            <h3 class="ride-card__title">{title}</h3>
                            <p class="ride-card__desc">{description}</p>
                        </div>
                        <div class="ride-card__footer">
                            <a href="{link}" class="ride-link">{link_text}<span class="ride-link__arrow" aria-hidden="true">&rarr;</span></a>
                        </div>
                    </article>
                </div>"""


def asset_version(rel_path):
    """Short content hash of a static asset, used to bust browser caches."""
    return hashlib.md5((ROOT / rel_path).read_bytes()).hexdigest()[:8]


def apply_globals(html, project_count):
    """Fill placeholders shared by every template."""
    html = html.replace("{{year}}", str(date.today().year))
    html = html.replace("{{project_count}}", f"{project_count:02d}")
    html = html.replace("{{css_v}}", asset_version("css/styles.css"))
    html = html.replace("{{js_v}}", asset_version("js/main.js"))
    return html


def build():
    """Build all HTML pages from templates and content files."""
    cards = load_portfolio()

    # Build index.html
    template = (TEMPLATES_DIR / "index.html").read_text()

    hero_title, hero_body = load_hero()
    portfolio_html = "\n".join(
        render_card(card, i) for i, card in enumerate(cards, start=1)
    )

    output = template.replace("{{hero_title}}", hero_title)
    output = output.replace("{{hero_body}}", hero_body)
    output = output.replace("{{portfolio_cards}}", portfolio_html)
    output = apply_globals(output, len(cards))

    (ROOT / "index.html").write_text(output)
    print(f"Built index.html ({len(cards)} portfolio cards)")

    # Build privacy.html and terms.html from the shared legal template
    legal_template = (TEMPLATES_DIR / "legal.html").read_text()
    for slug in ("privacy", "terms"):
        meta, body = parse_frontmatter((CONTENT_DIR / f"{slug}.md").read_text())
        page = legal_template
        page = page.replace("{{legal_title}}", meta.get("title", ""))
        page = page.replace("{{legal_updated}}", meta.get("updated", ""))
        page = page.replace("{{legal_description}}", meta.get("description", ""))
        page = page.replace("{{legal_slug}}", slug)
        notice = meta.get("notice", "")
        notice_html = (
            '<p class="legal-notice"><i class="bi bi-cone-striped" aria-hidden="true"></i> '
            f"{inline_md(notice)}</p>"
        ) if notice else ""
        page = page.replace("{{legal_notice}}", notice_html)
        page = page.replace("{{legal_body}}", md_to_html(body))
        page = apply_globals(page, len(cards))
        (ROOT / f"{slug}.html").write_text(page)
        print(f"Built {slug}.html")

    # Build contact.html
    contact_template = (TEMPLATES_DIR / "contact.html").read_text()
    contact_file = CONTENT_DIR / "contact.md"
    contact_meta, _ = parse_frontmatter(contact_file.read_text())

    contact_output = contact_template
    contact_output = contact_output.replace("{{contact_title}}", contact_meta.get("title", "Get In Touch"))
    contact_output = contact_output.replace("{{contact_subtitle}}", contact_meta.get("subtitle", ""))
    contact_output = contact_output.replace("{{contact_github}}", contact_meta.get("github", "#"))
    contact_output = contact_output.replace("{{contact_discord}}", contact_meta.get("discord", "#"))
    contact_output = contact_output.replace("{{contact_location}}", contact_meta.get("location", ""))
    contact_output = apply_globals(contact_output, len(cards))

    (ROOT / "contact.html").write_text(contact_output)
    print("Built contact.html")


if __name__ == "__main__":
    build()

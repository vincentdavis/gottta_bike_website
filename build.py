#!/usr/bin/env python3
"""Build script: reads markdown content files and generates index.html."""

import os
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"


def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown text. Returns (metadata dict, body string)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta = {}
    for line in match.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'")
        meta[key.strip()] = value
    return meta, match.group(2).strip()


def md_to_html(text):
    """Minimal markdown to HTML: paragraphs and line breaks."""
    paragraphs = re.split(r"\n{2,}", text.strip())
    parts = []
    for p in paragraphs:
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
            "image": meta.get("image", ""),
            "link": meta.get("link", "#"),
            "link_text": meta.get("link_text", "View Project"),
            "description": body,
        })
    return cards


def render_card(card):
    """Render a single portfolio card as HTML."""
    title = escape(card["title"])
    description = escape(card["description"])
    link = escape(card["link"])
    link_text = escape(card["link_text"])

    if card["image"]:
        image_html = (
            f'<img src="{escape(card["image"])}" class="card-img-top" '
            f'alt="{title}" style="height: 200px; object-fit: cover;">'
        )
    else:
        image_html = (
            '<div class="card-img-top bg-secondary d-flex align-items-center '
            'justify-content-center" style="height: 200px;">'
            '<i class="bi bi-image text-white" style="font-size: 3rem;"></i>'
            "</div>"
        )

    return f"""                <div class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm portfolio-card">
                        {image_html}
                        <div class="card-body">
                            <h5 class="card-title">{title}</h5>
                            <p class="card-text text-muted">{description}</p>
                        </div>
                        <div class="card-footer bg-transparent border-0">
                            <a href="{link}" class="btn btn-outline-primary btn-sm">{link_text}</a>
                        </div>
                    </div>
                </div>"""


def load_about():
    """Load about page content."""
    about_file = CONTENT_DIR / "about.md"
    meta, body = parse_frontmatter(about_file.read_text())
    return meta.get("title", "About"), md_to_html(body)


def build():
    """Build all HTML pages from templates and content files."""
    # Build index.html
    template = (TEMPLATES_DIR / "index.html").read_text()

    hero_title, hero_body = load_hero()
    cards = load_portfolio()

    portfolio_html = "\n".join(render_card(card) for card in cards)

    output = template.replace("{{hero_title}}", hero_title)
    output = output.replace("{{hero_body}}", hero_body)
    output = output.replace("{{portfolio_cards}}", portfolio_html)

    (ROOT / "index.html").write_text(output)
    print(f"Built index.html ({len(cards)} portfolio cards)")

    # Build about.html
    about_template = (TEMPLATES_DIR / "about.html").read_text()
    about_title, about_body = load_about()

    about_output = about_template.replace("{{about_title}}", about_title)
    about_output = about_output.replace("{{about_body}}", about_body)

    (ROOT / "about.html").write_text(about_output)
    print("Built about.html")

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

    (ROOT / "contact.html").write_text(contact_output)
    print("Built contact.html")


if __name__ == "__main__":
    build()

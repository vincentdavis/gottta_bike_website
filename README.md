# GOTTA.BIKE

Portfolio website for cycling projects by Vincent Davis.

## Project Structure

```
content/
  hero.md                   # Hero section (title + body text)
  contact.md                # Contact page (github, discord, location)
  privacy.md                # Privacy policy page content
  terms.md                  # Terms of service page content
  portfolio/
    01_world_of_cycling.md   # One file per portfolio card
    05_gotta_bike_fast.md    # Number prefix controls display order
    ...
templates/
  index.html                # Home page template
  contact.html              # Contact page template
  legal.html                # Shared template for privacy + terms pages
build.py                    # Generates index, contact, privacy, terms pages
```

## Editing Content

### Hero Section

Edit `content/hero.md`:

```markdown
---
title: GOTTA.BIKE
---

A PASSION FOR CYCLING
by: Vincent Davis
```

### Portfolio Cards

Add or edit files in `content/portfolio/`. Files are sorted by name, so use a number prefix to control order (e.g. `01_`, `02_`). Cards get a race-plate number (01, 02, ...) from their sort position.

```markdown
---
title: Project Name
tag: Web app
image: images/screenshot.png
link: https://example.com
link_text: View Project
---

Description of the project goes here. Inline [links](https://example.com) and **bold** are supported.
```

- `tag` — short category label shown above the title (e.g. `Web app`, `Chrome extension`, `Research`); optional
- `image` — path to an image in `images/`, or leave empty for a styled bike-icon placeholder
- `link` — URL to the live project, or `"#"` if not yet available

### Privacy & Terms Pages

Edit `content/privacy.md` and `content/terms.md`. Both use `templates/legal.html`.

```markdown
---
title: Privacy Policy
updated: July 13, 2026
notice: Draft — this policy is a working draft and may change.
description: Meta description for the page.
---

Intro paragraph.

## Section Heading

Section text. Separate paragraphs with blank lines; `## ` starts a new section.
```

### Contact Page

Edit `content/contact.md`:

```markdown
---
title: Get In Touch
subtitle: Have a project in mind? Let's talk!
email: hello@example.com
phone: "+1 (555) 123-4567"
location: City, Country
---
```

## Building

Requires Python 3. No external dependencies.

```sh
uv run build.py
```

This generates `index.html`, `contact.html`, `privacy.html`, and `terms.html` from the templates and content files. The build also fills two global placeholders in every template: `{{year}}` (current year, used in the footer copyright) and `{{project_count}}` (number of portfolio cards).

## Previewing

Serve the folder and open http://localhost:8137:

```sh
python3 -m http.server 8137
```

# GOTTA.BIKE

Portfolio website for cycling projects by Vincent Davis.

## Project Structure

```
content/
  hero.md                   # Hero section (title + body text)
  about.md                  # About page content
  contact.md                # Contact page (email, phone, location)
  portfolio/
    01_3d_printed_rides.md   # One file per portfolio card
    02_world_of_cycling.md   # Number prefix controls display order
    ...
templates/
  index.html                # Home page template
  about.html                # About page template
  contact.html              # Contact page template
build.py                    # Generates index.html, about.html, contact.html
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

Add or edit files in `content/portfolio/`. Files are sorted by name, so use a number prefix to control order (e.g. `01_`, `02_`).

```markdown
---
title: Project Name
image: images/screenshot.png
link: https://example.com
link_text: View Project
---

Description of the project goes here.
```

- `image` — path to an image in `images/`, or leave empty for a placeholder icon
- `link` — URL to the live project, or `"#"` if not yet available

### About Page

Edit `content/about.md`:

```markdown
---
title: About Me
---

Your about text here. Separate paragraphs with blank lines.
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

This generates `index.html`, `about.html`, and `contact.html` from the templates and content files.

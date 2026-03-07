#!/usr/bin/env python3
"""
convert_md_to_html.py
Converts the Floral Theory markdown (florary-headers.md) to index.html.
Usage:  python convert_md_to_html.py [input.md] [output.html]
"""

import re
import sys
from pathlib import Path
from html import escape

# ── CONFIG ────────────────────────────────────────────────────────────────────

SITE_TITLE = "Floral Theory"
ARCHIVE_URL = "https://github.com/DarshanKalita/floral-theory/blob/main/florary-headers.md"
CONTACT_EMAIL = "darshank.ug2025@cmi.ac.in"
CSS_FILE = "style.css"

DESCRIPTION = (
    "An archive of plants spotted in CMI "
    "that I deem archive-worthy of."
)

PS_TEXT = (
    "I made this in a hurry as part of a Group Theory coursework assignment, "
    "and hence most photos are really bad. "
    "I do, however, request future submissions to have a higher standard of aesthetics."
)

PENDING_PLANTS = [
    "Red Banana", "Chilli", "Custard Apple", "Marigold",
    "Water Lily", "Jamun", "Guava",
]

# ── PARSING ───────────────────────────────────────────────────────────────────

def parse_md(text: str):
    """
    Returns a list of dicts:
        { "number": int, "name": str, "images": [url, ...] }
    """
    plants = []
    # Match headings like:  ### 12. Coconut Palm
    heading_re = re.compile(r'^###\s+(\d+)\.\s+(.+)', re.MULTILINE)
    # Match markdown images: ![alt](url)
    image_re   = re.compile(r'!\[.*?\]\((https?://[^)]+)\)')

    # Split into blocks by heading
    positions = [(m.start(), m) for m in heading_re.finditer(text)]
    for i, (pos, match) in enumerate(positions):
        number = int(match.group(1))
        name   = match.group(2).strip().rstrip('?')
        # Text until next heading (or end)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        block = text[pos:end]
        images = image_re.findall(block)
        plants.append({"number": number, "name": name, "images": images})
    return plants

# ── HTML GENERATION ───────────────────────────────────────────────────────────

LEAF_SVG = """
<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 6 C12 6 6 18 6 30 C6 38 12 44 24 44 C36 44 42 34 42 22 C42 12 34 6 24 6Z"
        fill="#4a5e3a" opacity="0.35"/>
  <path d="M24 44 C24 44 22 28 14 18" stroke="#4a5e3a" stroke-width="1.5"
        stroke-linecap="round" opacity="0.5"/>
</svg>"""


def image_block(images: list, name: str) -> str:
    if not images:
        return f'<div class="card-img-wrap"><div class="card-img-placeholder">{LEAF_SVG}</div></div>'

    n = len(images)
    wrap_class = "card-img-wrap"
    if n == 2:
        wrap_class += " multi"
    elif n >= 3:
        wrap_class += " triple"

    if n == 1:
        # single image — whole card is clickable (handled by card-level listener)
        imgs_html = f'      <img class="card-img" src="{escape(images[0])}" alt="" loading="lazy">'
    else:
        # each image gets its own clickable wrapper
        imgs_html = "\n".join(
            f'      <span class="img-click" data-img="{escape(url)}" data-name="{escape(name)}">'
            f'<img class="card-img" src="{escape(url)}" alt="" loading="lazy"></span>'
            for url in images[:3]
        )

    return f'<div class="{wrap_class}">\n{imgs_html}\n    </div>'


def card_html(plant: dict, idx: int) -> str:
    num   = plant["number"]
    name  = escape(plant["name"])
    is_unknown = name.lower().startswith("unidentified")
    name_class = "card-name unidentified" if is_unknown else "card-name"
    display_name = "Unidentified" if is_unknown else name

    imgs = plant["images"]
    img_blk = image_block(imgs, name)

    # For single-image cards, keep card-level click; multi handled per-image
    if len(imgs) == 1:
        first_img = escape(imgs[0])
        data_attrs = f'data-img="{first_img}" data-name="{name}"'
        card_class = 'plant-card single-img'
    else:
        data_attrs = f'data-name="{name}"'
        card_class = 'plant-card'

    return f"""  <article class="{card_class}" {data_attrs}>
    {img_blk}
    <div class="card-overlay"></div>
    <div class="card-footer">
      <span class="card-number">#{num:02d}</span>
      <span class="{name_class}">{display_name}</span>
    </div>
  </article>"""


def pending_html() -> str:
    items = "\n".join(f"    <li>{escape(p)}</li>" for p in PENDING_PLANTS)
    return f"""<section class="coming-soon-section">
  <h2>— coming soon —</h2>
  <ul class="pending-list">
{items}
  </ul>
</section>"""


def build_html(plants: list) -> str:
    cards = "\n".join(card_html(p, i) for i, p in enumerate(plants))
    count = len(plants)

    leaf_ornament_l = """<svg width="28" height="28" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M38 10 C26 8 10 18 8 36 C16 36 28 32 38 22 C44 16 44 10 38 10Z" fill="#4a5e3a"/>
      <path d="M8 36 C8 36 20 24 36 12" stroke="#f5f0e8" stroke-width="1.5" stroke-linecap="round"/>
    </svg>"""

    leaf_ornament_r = """<svg width="28" height="28" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="transform:scaleX(-1)">
      <path d="M38 10 C26 8 10 18 8 36 C16 36 28 32 38 22 C44 16 44 10 38 10Z" fill="#4a5e3a"/>
      <path d="M8 36 C8 36 20 24 36 12" stroke="#f5f0e8" stroke-width="1.5" stroke-linecap="round"/>
    </svg>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_TITLE}</title>
  <link rel="stylesheet" href="{CSS_FILE}">
  <meta name="description" content="{DESCRIPTION}">
</head>
<body>

  <!-- ── HEADER ── -->
  <header class="site-header">
    <div class="title-ornament">
      {leaf_ornament_l}
      <h1 class="site-title">
        <span class="site-title-text">
          <span class="word-floral">Floral</span> Theory
        </span>
        <div class="title-tagline">A campus flora archive</div>
      </h1>
      {leaf_ornament_r}
    </div>
    <div class="header-rule"></div>
    <p class="site-description">{DESCRIPTION}</p>
    <a class="archive-link" href="{ARCHIVE_URL}" target="_blank" rel="noopener">
      View Raw Archive ↗
    </a>

    <!-- ── SUBMISSION CALL ── -->
    <div class="submission-banner">
      <p>
        <strong>Open for submissions.</strong> A lot more trees are available on campus than
        the cardinality of this archive. You are encouraged to
        <a href="mailto:{CONTACT_EMAIL}">mail me</a> with pictures
        of the specific plant if you want it updated.
      </p>
    </div>

    <p class="header-ps">
      <strong>PS.</strong> {PS_TEXT}
    </p>
  </header>

  <div class="divider">✦ &nbsp; ✦ &nbsp; ✦</div>

  <!-- ── PLANT COUNT ── -->
  <div class="count-bar">
    <span class="count-badge"><span>{count}</span> &ensp; specimens archived</span>
  </div>

  <!-- ── PLANT GRID ── -->
  <main>
    <div class="plant-grid">
{cards}
    </div>

    {pending_html()}
  </main>

  <!-- ── FOOTER ── -->
  <footer class="site-footer">
    <div class="footer-rule"></div>
    <p class="footer-made-by">
      Made with <span class="heart">♥</span> and lots of effort by
      <span class="footer-author">Darshan Kalita</span>
    </p>
    <p class="footer-text">
      Please send any corrections and errors to
      <a class="footer-mail" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
    </p>
  </footer>

  <!-- ── LIGHTBOX ── -->
  <div class="lightbox" id="lightbox">
    <button class="lb-nav lb-prev" id="lb-prev" aria-label="Previous">&#8592;</button>
    <div class="lightbox-inner">
      <button class="lightbox-close" id="lb-close">✕ close</button>
      <img class="lightbox-img" id="lb-img" src="" alt="">
      <p class="lightbox-caption" id="lb-caption"></p>
      <p class="lb-counter" id="lb-counter"></p>
    </div>
    <button class="lb-nav lb-next" id="lb-next" aria-label="Next">&#8594;</button>
  </div>

  <script>
    const lb        = document.getElementById('lightbox');
    const lbImg     = document.getElementById('lb-img');
    const lbCap     = document.getElementById('lb-caption');
    const lbCounter = document.getElementById('lb-counter');
    const lbClose   = document.getElementById('lb-close');
    const lbPrev    = document.getElementById('lb-prev');
    const lbNext    = document.getElementById('lb-next');

    // Build a flat ordered gallery from all clickable images
    // Each entry: {{ src, name }}
    const gallery = [];

    document.querySelectorAll('.plant-card').forEach(card => {{
      const clicks = card.querySelectorAll('.img-click');
      if (clicks.length > 0) {{
        clicks.forEach(el => gallery.push({{ src: el.dataset.img, name: el.dataset.name }}));
      }} else if (card.dataset.img) {{
        gallery.push({{ src: card.dataset.img, name: card.dataset.name }});
      }}
    }});

    let current = 0;

    function showSlide(idx, animate) {{
      current = (idx + gallery.length) % gallery.length;
      const entry = gallery[current];
      if (animate) {{
        lbImg.style.opacity = '0';
        lbImg.style.transform = animate === 'left' ? 'translateX(-18px)' : 'translateX(18px)';
        setTimeout(() => {{
          lbImg.src = entry.src;
          lbCap.textContent = entry.name;
          lbImg.style.transition = 'opacity 0.22s ease, transform 0.22s ease';
          lbImg.style.opacity = '1';
          lbImg.style.transform = 'translateX(0)';
        }}, 180);
      }} else {{
        lbImg.style.transition = 'none';
        lbImg.style.opacity = '1';
        lbImg.style.transform = 'translateX(0)';
        lbImg.src = entry.src;
        lbCap.textContent = entry.name;
      }}
      lbCounter.textContent = (current + 1) + ' / ' + gallery.length;
    }}

    function openLightbox(src, name) {{
      const idx = gallery.findIndex(e => e.src === src && e.name === name);
      lb.classList.add('active');
      showSlide(idx >= 0 ? idx : 0, null);
    }}

    // Single-image cards
    document.querySelectorAll('.plant-card.single-img').forEach(card => {{
      card.addEventListener('click', () => openLightbox(card.dataset.img, card.dataset.name));
    }});

    // Multi-image cards
    document.querySelectorAll('.img-click').forEach(el => {{
      el.addEventListener('click', e => {{
        e.stopPropagation();
        openLightbox(el.dataset.img, el.dataset.name);
      }});
    }});

    lbPrev.addEventListener('click', e => {{ e.stopPropagation(); showSlide(current - 1, 'right'); }});
    lbNext.addEventListener('click', e => {{ e.stopPropagation(); showSlide(current + 1, 'left'); }});
    lbClose.addEventListener('click', () => lb.classList.remove('active'));
    lb.addEventListener('click', e => {{ if (e.target === lb) lb.classList.remove('active'); }});

    document.addEventListener('keydown', e => {{
      if (!lb.classList.contains('active')) return;
      if (e.key === 'Escape')      lb.classList.remove('active');
      if (e.key === 'ArrowLeft')   showSlide(current - 1, 'right');
      if (e.key === 'ArrowRight')  showSlide(current + 1, 'left');
    }});

    // Touch swipe
    let touchStartX = 0;
    lb.addEventListener('touchstart', e => {{ touchStartX = e.touches[0].clientX; }}, {{passive: true}});
    lb.addEventListener('touchend',   e => {{
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) showSlide(dx < 0 ? current + 1 : current - 1, dx < 0 ? 'left' : 'right');
    }});
  </script>
</body>
</html>
"""

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    input_path  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("florary-headers.md")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("index.html")

    if not input_path.exists():
        print(f"Error: '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    text   = input_path.read_text(encoding="utf-8")
    plants = parse_md(text)
    print(f"Parsed {len(plants)} plant entries.")

    html = build_html(plants)
    output_path.write_text(html, encoding="utf-8")
    print(f"Written → {output_path}")


if __name__ == "__main__":
    main()

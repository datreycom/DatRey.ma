import os
import json
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from autopilot.config import BLOG_DIR, BLOG_DATA_JSON, BASE_DIR

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | DatRey Blog</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://datrey.ma/blog/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://datrey.ma/blog/{slug}.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://datrey.ma/assets/blog/{slug}-1.webp">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  
  <style>
    :root {{
      --bg-main: #ffffff;
      --text-main: #0f172a;
      --text-muted: #475569;
      --card-bg: #f8fafc;
      --accent: #2563eb;
      --border-color: #e2e8f0;
    }}
    body {{
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: 'Inter', sans-serif;
      line-height: 1.8;
    }}
    .article-container {{
      max-width: 820px;
      margin: 0 auto;
      padding: 40px 20px;
    }}
    .hero-title {{
      font-family: 'DM Serif Display', serif;
      font-size: 2.75rem;
      line-height: 1.25;
      color: #0f172a;
      margin-bottom: 16px;
    }}
    .hero-meta {{
      font-size: 0.9rem;
      color: #64748b;
      margin-bottom: 28px;
    }}
    .article-hero-img-wrap {{
      margin-bottom: 36px;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
    }}
    .article-hero-img-wrap img {{
      width: 100%;
      height: auto;
      max-height: 480px;
      object-fit: cover;
      display: block;
    }}
    .blog-content h2 {{
      font-family: 'DM Serif Display', serif;
      font-size: 1.85rem;
      color: #0f172a;
      margin-top: 40px;
      margin-bottom: 16px;
    }}
    .blog-content h3 {{
      font-size: 1.35rem;
      color: #1e293b;
      margin-top: 28px;
      margin-bottom: 12px;
    }}
    .blog-content p {{
      font-size: 1.1rem;
      color: #334155;
      margin-bottom: 20px;
    }}
    .blog-content ul, .blog-content ol {{
      margin-bottom: 24px;
      padding-left: 24px;
      color: #334155;
    }}
    .blog-content li {{
      margin-bottom: 8px;
      font-size: 1.05rem;
    }}
    .article-body-img-wrap {{
      margin: 40px 0;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
      background-color: #f1f5f9;
    }}
    .article-body-img-wrap img {{
      width: 100%;
      height: auto;
      max-height: 440px;
      object-fit: cover;
      display: block;
    }}
    .geo-definition-box {{
      background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
      border-left: 4px solid #2563eb;
      padding: 24px;
      border-radius: 8px;
      margin: 28px 0;
      font-size: 1.1rem;
      line-height: 1.7;
      color: #1e293b;
    }}
    .cta-article-box {{
      background: #0f172a;
      color: #ffffff;
      padding: 36px;
      border-radius: 16px;
      margin-top: 48px;
      text-align: center;
    }}
    .cta-article-box h3 {{
      color: #ffffff;
      font-family: 'DM Serif Display', serif;
      font-size: 1.8rem;
      margin-bottom: 12px;
    }}
    .cta-article-box p {{
      color: #94a3b8;
      font-size: 1.05rem;
      margin-bottom: 24px;
    }}
    .cta-btn {{
      display: inline-block;
      background: #2563eb;
      color: #ffffff;
      font-weight: 600;
      padding: 14px 32px;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.2s ease;
    }}
    .cta-btn:hover {{
      background: #1d4ed8;
    }}
  </style>

  <!-- Schema.org BlogPosting -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{description}",
    "image": "https://datrey.ma/assets/blog/{slug}-1.webp",
    "publisher": {{
      "@type": "Organization",
      "name": "DatRey SARL",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://datrey.ma/assets/logo.png"
      }}
    }},
    "url": "https://datrey.ma/blog/{slug}.html",
    "inLanguage": "fr-MA"
  }}
  </script>
</head>
<body>
  <header style="border-bottom: 1px solid #e2e8f0; padding: 16px 0;">
    <div class="article-container" style="padding-top:0; padding-bottom:0; display:flex; justify-size:space-between; align-items:center;">
      <a href="../index.html" style="font-weight:700; font-size:1.25rem; color:#0f172a; text-decoration:none;">DatRey</a>
      <a href="../blog.html" style="color:#2563eb; font-weight:500; text-decoration:none;">&larr; Retour au Blog</a>
    </div>
  </header>

  <main>
    <div class="article-container">
      <div style="margin-bottom: 16px;">
        <span style="background:#eff6ff; color:#2563eb; font-weight:600; font-size:0.85rem; padding:6px 14px; border-radius:20px;">{category}</span>
      </div>
      <h1 class="hero-title">{title}</h1>
      <p class="hero-meta">Publié par l'équipe DatRey | Temps de lecture : ~6 min</p>

      <div class="article-hero-img-wrap">
        <img src="../assets/blog/{slug}-1.webp" alt="{title}" />
      </div>

      <article class="blog-content">
        {content}
      </article>

      <div class="cta-article-box">
        <h3>Besoin d'accélérer votre croissance digitale ?</h3>
        <p>Obtenez un Audit Digital & SEO complet de votre entreprise par les experts DatRey au Maroc.</p>
        <a href="../contact.html?subject=AuditGratuit" class="cta-btn">Demander mon Audit Gratuit</a>
      </div>
    </div>
  </main>

  <footer style="border-top:1px solid #e2e8f0; margin-top:60px; padding:30px 0; text-align:center; color:#64748b; font-size:0.9rem;">
    <p>&copy; 2026 DatRey SARL. Tous droits réservés. Agence Marketing Digital Maroc.</p>
  </footer>
</body>
</html>
"""

def inject_inbody_images(content_html, slug, title):
    """
    Injects 4 in-body images ([slug]-2.webp to [slug]-5.webp) evenly into the HTML content,
    guaranteeing AT LEAST 250 words / 1500 characters of text spacing between consecutive images!
    """
    elements = re.split(r'(</p>|</h2>|</h3>)', content_html, flags=re.IGNORECASE)
    if len(elements) <= 1:
        return content_html

    result = []
    current_word_count = 0
    img_idx = 2
    MIN_WORD_SPACING = 250  # At least 250 words between photos

    for element in elements:
        result.append(element)
        words_in_element = len(re.findall(r'\w+', element))
        current_word_count += words_in_element

        if img_idx <= 5 and current_word_count >= MIN_WORD_SPACING and (element.lower() == '</p>' or element.lower() == '</h2>'):
            img_tag = (
                f'\n<div class="article-body-img-wrap">'
                f'<img src="../assets/blog/{slug}-{img_idx}.webp" alt="{title} - Illustration {img_idx-1}" class="blog-img" loading="lazy" />'
                f'</div>\n'
            )
            result.append(img_tag)
            img_idx += 1
            current_word_count = 0  # Reset counter for next image spacing

    return "".join(result)

def build_article_page(article_data):
    """
    Compiles article HTML, injects body images with >=250 word spacing, and writes file to blog/{slug}.html.
    """
    slug = article_data["slug"]
    title = article_data["title"]
    desc = article_data["description"]
    cat = article_data["category"]
    content_raw = article_data["content"]

    content_with_images = inject_inbody_images(content_raw, slug, title)

    full_html = ARTICLE_TEMPLATE.format(
        title=title,
        description=desc,
        slug=slug,
        category=cat,
        content=content_with_images
    )

    os.makedirs(BLOG_DIR, exist_ok=True)
    out_path = os.path.join(BLOG_DIR, f"{slug}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[Site Builder] Article HTML created -> blog/{slug}.html")
    update_blog_data_json(article_data)
    rebuild_blog_index_and_sitemaps()

    return out_path

def update_blog_data_json(article_data):
    """Update blog_data.json with the new article metadata."""
    entries = []
    if os.path.exists(BLOG_DATA_JSON):
        try:
            with open(BLOG_DATA_JSON, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []

    # Remove existing entry if slug matches
    entries = [e for e in entries if e.get("slug") != article_data["slug"]]

    new_entry = {
        "title": article_data["title"],
        "slug": article_data["slug"],
        "description": article_data["description"],
        "category": article_data["category"],
        "date": "2026-07-28",
        "author": "DatRey Experts",
        "image": f"assets/blog/{article_data['slug']}-1.webp",
        "lang": "fr"
    }
    entries.insert(0, new_entry)

    with open(BLOG_DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def rebuild_blog_index_and_sitemaps():
    """Rebuild blog.html and generate multi-language sitemaps."""
    try:
        from build_blog_index import build_blog_index
        build_blog_index()
    except Exception as e:
        print(f"[Site Builder] Error building blog index: {e}")

    try:
        from generate_sitemap_index import generate_sitemaps
        generate_sitemaps()
    except Exception as e:
        print(f"[Site Builder] Error building sitemaps: {e}")

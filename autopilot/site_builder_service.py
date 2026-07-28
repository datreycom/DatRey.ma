import os
import sys
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from autopilot.config import BLOG_DIR, BLOG_DATA_JSON
from build_blog_index import build_blog_index
from generate_sitemap_index import generate_sitemap_index

HTML_ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Blog DatRey</title>
  <meta name="description" content="{description}" />
  <meta property="og:title" content="{title} | Blog DatRey" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="https://datrey.ma/assets/blog/{slug}-1.webp" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://datrey.ma/blog/{slug}.html" />
  <link rel="canonical" href="https://datrey.ma/blog/{slug}.html" />
  <link rel="stylesheet" href="../style.css" />
  <link rel="icon" href="../assets/logo.webp" type="image/webp" />
  <meta name="theme-color" content="#ffffff" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap" />
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
  <script defer src="../shared.js"></script>
  <script defer src="../animations.js"></script>
  
  <script type="application/ld+json">
  {schema_json}
  </script>
</head>
<body>
  <script>document.documentElement.setAttribute('data-theme',localStorage.getItem('datrey-theme')||'light');</script>
  
  <header class="header" id="header">
    <div class="container">
      <a href="../index.html" class="logo" aria-label="DatRey — Accueil">
        <img src="../assets/logo.webp" alt="DatRey Logo" width="40" height="40" />
        <span><span class="logo-blue">D</span>at<span class="logo-blue">R</span>ey</span>
      </a>
      <nav class="nav-links" aria-label="Navigation principale">
        <a href="../index.html">Accueil</a>
        <a href="../services.html">Nos Services</a>
        <a href="../blog.html" class="nav-active">Blog</a>
        <a href="../contact.html">Contact</a>
        <a href="../contact.html" class="btn btn-primary nav-cta">Audit Gratuit</a>
      </nav>
      <div style="display: flex; align-items: center; gap: 16px;">
        <button id="themeToggle" class="theme-toggle" aria-label="Basculer le thème">
          <svg class="sun-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
          <svg class="moon-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
      </div>
    </div>
  </header>

  <section class="page-hero antigrav-hero">
    <div class="container">
      <div class="page-hero-content">
        <nav class="breadcrumb" aria-label="Fil d'Ariane">
          <a href="../index.html">Accueil</a> <span class="breadcrumb-sep">/</span>
          <a href="../blog.html">Blog</a> <span class="breadcrumb-sep">/</span>
          <span class="breadcrumb-current">{category}</span>
        </nav>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{description}</p>
      </div>
    </div>
  </section>

  <main id="main-content" class="section-padding">
    <div class="container" style="max-width: 850px; margin: 0 auto;">
      <div class="article-hero-img-wrap" style="margin-bottom:32px; border-radius:12px; overflow:hidden;">
        <img src="../assets/blog/{slug}-1.webp" alt="{title}" style="width:100%; max-height:450px; object-fit:cover;" />
      </div>
      <article class="blog-content">
        {content}
      </article>
    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <p style="text-align:center; color:var(--text-muted);">&copy; 2026 DatRey SARL. Tous droits réservés.</p>
    </div>
  </footer>

  <!-- Exit Intent Popup -->
  <div id="exitIntentPopup" class="exit-popup-overlay">
    <div class="exit-popup-modal">
      <button class="exit-popup-close" aria-label="Fermer">×</button>
      <div class="exit-popup-content">
        <h3 style="color: var(--text-main); font-size: 1.5rem; margin-bottom: 12px; font-family: 'DM Serif Display', serif;">Ne partez pas les mains vides !</h3>
        <p style="color: var(--text-muted); margin-bottom: 24px; font-size: 0.95rem;">Obtenez un <strong>Audit UX/UI & SEO gratuit</strong> de votre site web. Découvrez comment augmenter vos conversions dès aujourd'hui.</p>
        <a href="../contact.html?subject=AuditGratuit" class="btn btn-primary magnetic-btn" style="width: 100%; justify-content: center;">Je veux mon audit gratuit</a>
        <p style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted);">Sans engagement. Analyse livrée en 48h.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""

def inject_inbody_images(content_html, slug, title):
    """
    Injects 4 body images ([slug]-2.webp to [slug]-5.webp) evenly after H2 sections.
    """
    h2_parts = re.split(r'(<h2.*?>.*?</h2>)', content_html, flags=re.IGNORECASE)
    if len(h2_parts) <= 1:
        return content_html

    result = []
    img_idx = 2

    for part in h2_parts:
        result.append(part)
        if part.lower().startswith('<h2') and img_idx <= 5:
            img_tag = (
                f'\n<div class="article-body-img-wrap" style="margin:24px 0; border-radius:8px; overflow:hidden;">'
                f'<img src="../assets/blog/{slug}-{img_idx}.webp" alt="{title} - Illustration {img_idx-1}" class="blog-img" loading="lazy" style="width:100%; height:auto; display:block;" />'
                f'</div>\n'
            )
            result.append(img_tag)
            img_idx += 1

    return "".join(result)

def build_article_page(article_data):
    """
    Compiles article data into HTML file, updates blog_data.json, rebuilds index, updates sitemap.
    """
    title = article_data["title"]
    slug = article_data["slug"]
    desc = article_data["description"]
    category = article_data["category"]
    raw_content = article_data["content"]

    # Inject inbody images
    content_with_imgs = inject_inbody_images(raw_content, slug, title)

    # JSON-LD Schema
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": desc,
        "image": f"https://datrey.ma/assets/blog/{slug}-1.webp",
        "datePublished": datetime.now().strftime("%Y-%m-%d"),
        "author": {"@type": "Organization", "name": "DatRey", "url": "https://datrey.ma"},
        "publisher": {
            "@type": "Organization",
            "name": "DatRey",
            "logo": {"@type": "ImageObject", "url": "https://datrey.ma/assets/logo.webp"}
        }
    }

    html_page = HTML_ARTICLE_TEMPLATE.format(
        title=title,
        slug=slug,
        description=desc,
        category=category,
        content=content_with_imgs,
        schema_json=json.dumps(schema, ensure_ascii=False, indent=2)
    )

    os.makedirs(BLOG_DIR, exist_ok=True)
    file_path = os.path.join(BLOG_DIR, f"{slug}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_page)

    print(f"[Site Builder] Article HTML created -> blog/{slug}.html")

    # Update blog_data.json
    blog_index = []
    if os.path.exists(BLOG_DATA_JSON):
        try:
            with open(BLOG_DATA_JSON, "r", encoding="utf-8") as f:
                blog_index = json.load(f)
        except Exception:
            blog_index = []

    # Check if article already exists in json
    existing_idx = next((i for i, item in enumerate(blog_index) if item.get("slug") == slug), None)
    new_entry = {
        "title": title,
        "slug": slug,
        "category": category,
        "desc": desc,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    if existing_idx is not None:
        blog_index[existing_idx] = new_entry
    else:
        blog_index.insert(0, new_entry)

    with open(BLOG_DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(blog_index, f, ensure_ascii=False, indent=2)

    # Rebuild blog.html and sitemap.xml
    print("[Site Builder] Rebuilding blog index (blog.html) and sitemaps...")
    build_blog_index()
    generate_sitemap_index()

    return file_path

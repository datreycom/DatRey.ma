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
      background-color: var(--bg-main) !important;
      color: var(--text-main) !important;
      font-family: 'Inter', sans-serif;
      line-height: 1.8;
      margin: 0;
      padding: 0;
      width: 100%;
    }}
    .site-header {{
      background: #ffffff;
      border-bottom: 1px solid #e2e8f0;
      position: sticky;
      top: 0;
      z-index: 1000;
      padding: 16px 0;
      width: 100%;
    }}
    .site-header-container {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0 4%;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .site-logo {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 1.4rem;
      color: #0f172a;
      text-decoration: none;
    }}
    .site-nav {{
      display: flex;
      align-items: center;
      gap: 28px;
    }}
    .site-nav a {{
      color: #475569;
      font-weight: 500;
      text-decoration: none;
      font-size: 1rem;
      transition: color 0.2s ease;
    }}
    .site-nav a:hover {{
      color: #2563eb;
    }}
    .article-container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 52px 4%;
      width: 92%;
    }}
    .hero-title {{
      font-family: 'DM Serif Display', serif;
      font-size: 3.1rem;
      line-height: 1.2;
      color: #0f172a !important;
      margin-top: 16px;
      margin-bottom: 20px;
    }}
    .hero-meta {{
      font-size: 0.95rem;
      color: #64748b;
      margin-bottom: 32px;
    }}
    .article-hero-img-wrap {{
      margin-bottom: 44px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
      width: 100%;
    }}
    .article-hero-img-wrap img {{
      width: 100%;
      height: auto;
      max-height: 560px;
      object-fit: cover;
      display: block;
    }}
    .blog-content {{
      width: 100%;
      max-width: 100%;
    }}
    .blog-content h2 {{
      font-family: 'DM Serif Display', serif;
      font-size: 2.1rem;
      color: #0f172a !important;
      margin-top: 48px;
      margin-bottom: 18px;
    }}
    .blog-content h3 {{
      font-size: 1.45rem;
      color: #1e293b !important;
      margin-top: 32px;
      margin-bottom: 14px;
    }}
    .blog-content p {{
      font-size: 1.15rem;
      color: #334155 !important;
      margin-bottom: 24px;
      line-height: 1.85;
    }}
    .blog-content ul, .blog-content ol {{
      margin-bottom: 28px;
      padding-left: 28px;
      color: #334155 !important;
    }}
    .blog-content li {{
      margin-bottom: 10px;
      font-size: 1.1rem;
    }}
    .article-body-img-wrap {{
      margin: 48px 0;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 12px 36px rgba(15, 23, 42, 0.06);
      background-color: #f1f5f9;
      width: 100%;
    }}
    .article-body-img-wrap img {{
      width: 100%;
      height: auto;
      max-height: 540px;
      object-fit: cover;
      display: block;
    }}
    .geo-definition, .geo-definition-box {{
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
      border-left: 5px solid #2563eb !important;
      padding: 24px 28px !important;
      border-radius: 12px !important;
      margin: 32px 0 !important;
      font-size: 1.1rem !important;
      line-height: 1.75 !important;
      color: #0f172a !important;
      width: 100%;
      box-sizing: border-box;
    }}
    .geo-definition strong, .geo-definition-box strong {{
      color: #2563eb !important;
    }}
    .cta-article-box {{
      background: #0f172a;
      color: #ffffff;
      padding: 44px 36px;
      border-radius: 20px;
      margin-top: 60px;
      text-align: center;
      width: 100%;
      box-sizing: border-box;
    }}
    .cta-article-box h3 {{
      color: #ffffff !important;
      font-family: 'DM Serif Display', serif;
      font-size: 2.1rem;
      margin-bottom: 14px;
    }}
    .cta-article-box p {{
      color: #94a3b8 !important;
      font-size: 1.1rem;
      margin-bottom: 28px;
    }}
    .cta-btn {{
      display: inline-block;
      background: #2563eb;
      color: #ffffff !important;
      font-weight: 600;
      padding: 14px 32px;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.2s ease;
      font-size: 1rem;
    }}
    .cta-btn:hover {{
      background: #1d4ed8;
    }}
    @media (max-width: 768px) {{
      .hero-title {{ font-size: 2.2rem; }}
      .site-nav {{ display: none; }}
      .article-container {{ width: 95%; padding: 24px 12px; }}
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

  <!-- Meta Facebook Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window,document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '1018889237621151');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=1018889237621151&ev=PageView&noscript=1"/></noscript>
  <!-- End Meta Facebook Pixel Code -->
</head>
<body>
  <header class="site-header">
    <div class="site-header-container">
      <a href="../index.html" class="site-logo">
        <img src="../assets/logo.webp" alt="DatRey Logo" width="40" height="40" style="border-radius:6px;" />
        <span><span style="color:#2563eb;">D</span>at<span style="color:#2563eb;">R</span>ey</span>
      </a>
      <nav class="site-nav">
        <a href="../index.html">Accueil</a>
        <a href="../services.html">Services</a>
        <a href="../blog.html" style="color:#2563eb; font-weight:600;">Blog</a>
        <a href="../contact.html?subject=AuditGratuit" class="cta-btn" style="padding:10px 22px; font-size:0.95rem;">Audit Gratuit</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="article-container">
      <div style="margin-bottom: 14px;">
        <span style="background:#eff6ff; color:#2563eb; font-weight:600; font-size:0.9rem; padding:6px 16px; border-radius:20px;">{category}</span>
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

  <footer style="border-top:1px solid #e2e8f0; margin-top:80px; padding:40px 0; text-align:center; color:#64748b; font-size:0.95rem;">
    <div class="site-header-container" style="justify-content:center;">
      <p>&copy; 2026 DatRey SARL. Tous droits réservés. Agence Marketing Digital Maroc.</p>
    </div>
  </footer>
</body>
</html>
"""

def inject_inbody_images(content_html, slug, title):
    """
    Injects 4 in-body images ([slug]-2.webp to [slug]-5.webp) evenly into the HTML content,
    guaranteeing AT LEAST 250 words / 1500 characters of text spacing between consecutive images!
    """
    clean_title = re.sub(r'\s*\|\s*Blog\s*DatRey.*$', '', title, flags=re.IGNORECASE).strip()
    elements = re.split(r'(</p>|</h2>|3>)', content_html, flags=re.IGNORECASE)
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
                f'<img src="../assets/blog/{slug}-{img_idx}.webp" alt="{clean_title} - Illustration {img_idx-1}" class="blog-img" loading="lazy" />'
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
    raw_title = article_data["title"]
    desc = article_data["description"]
    cat = article_data["category"]
    content_raw = article_data["content"]

    clean_title = re.sub(r'\s*\|\s*Blog\s*DatRey.*$', '', raw_title, flags=re.IGNORECASE).strip()

    content_with_images = inject_inbody_images(content_raw, slug, clean_title)

    full_html = ARTICLE_TEMPLATE.format(
        title=clean_title,
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
    update_blog_data_json({**article_data, "title": clean_title})
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

    entries = [e for e in entries if e.get("slug") != article_data["slug"]]

    clean_title = re.sub(r'\s*\|\s*Blog\s*DatRey.*$', '', article_data["title"], flags=re.IGNORECASE).strip()

    new_entry = {
        "title": clean_title,
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
        from generate_sitemap_index import generate_sitemap_index
        generate_sitemap_index()
    except Exception as e:
        print(f"[Site Builder] Error building sitemaps: {e}")

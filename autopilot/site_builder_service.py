import os
import json
import re
import sys
from datetime import datetime

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
    :root {
      --bg-main: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #475569;
      --accent: #2563eb;
      --border-color: #e2e8f0;
    }
    [data-theme="dark"] {
      --bg-main: #050814;
      --card-bg: #0a0f1f;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #3b82f6;
      --border-color: rgba(255, 255, 255, 0.1);
    }
    body {
      background-color: var(--bg-main) !important;
      color: var(--text-main) !important;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      line-height: 1.85;
      margin: 0;
      padding: 0;
      width: 100%;
    }
    .site-header {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 1000;
      padding: 16px 0;
      width: 100%;
    }
    [data-theme="dark"] .site-header {
      background: rgba(10, 15, 31, 0.95);
    }
    .site-header-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .site-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 1.35rem;
      color: var(--text-main);
      text-decoration: none;
    }
    .site-nav {
      display: flex;
      align-items: center;
      gap: 28px;
    }
    .site-nav a {
      color: var(--text-muted);
      font-weight: 500;
      text-decoration: none;
      font-size: 0.95rem;
      transition: color 0.2s ease;
    }
    .site-nav a:hover {
      color: var(--accent);
    }

    /* Boxed Outer Layout */
    .article-outer-wrapper {
      background-color: var(--bg-main);
      padding: 48px 20px 80px 20px;
      min-height: 85vh;
    }
    .article-card-box {
      max-width: 920px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      box-shadow: 0 12px 48px rgba(15, 23, 42, 0.05);
      padding: 56px 64px;
      box-sizing: border-box;
    }

    /* Centered Header Elements */
    .article-header-centered {
      text-align: center;
      margin-bottom: 36px;
    }
    .category-badge {
      display: inline-block;
      background: rgba(37, 99, 235, 0.08);
      color: var(--accent);
      font-weight: 700;
      font-size: 0.85rem;
      padding: 6px 20px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 20px;
    }
    .hero-title {
      font-family: 'DM Serif Display', serif;
      font-size: 2.6rem;
      line-height: 1.25;
      color: var(--text-main) !important;
      margin: 0 auto 20px auto;
      max-width: 800px;
      text-align: center;
    }
    .hero-meta {
      font-size: 0.95rem;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin: 0;
    }

    /* Boxed Featured Image */
    .article-hero-img-wrap {
      margin: 0 auto 48px auto;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
      border: 1px solid var(--border-color);
      max-width: 100%;
    }
    .article-hero-img-wrap img {
      width: 100%;
      height: auto;
      max-height: 460px;
      object-fit: cover;
      display: block;
    }

    /* Reading Content Area (Centered Optimal Line Width 780px) */
    .blog-content {
      max-width: 780px;
      margin: 0 auto;
      font-size: 1.125rem;
      color: var(--text-main);
    }
    .blog-content h2 {
      font-family: 'DM Serif Display', serif;
      font-size: 2.0rem;
      color: var(--text-main) !important;
      margin-top: 52px;
      margin-bottom: 20px;
      line-height: 1.3;
      padding-bottom: 12px;
      border-bottom: 2px solid var(--border-color);
    }
    .blog-content h3 {
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-main) !important;
      margin-top: 36px;
      margin-bottom: 16px;
    }
    .blog-content p {
      font-size: 1.125rem;
      color: var(--text-muted) !important;
      margin-bottom: 28px;
      line-height: 1.85;
    }
    .blog-content ul, .blog-content ol {
      margin-bottom: 32px;
      padding-left: 28px;
      color: var(--text-muted) !important;
      line-height: 1.8;
    }
    .blog-content li {
      margin-bottom: 12px;
      font-size: 1.08rem;
    }
    
    /* Boxed In-Body Images with Controlled Spacing */
    .article-body-img-wrap {
      margin: 48px auto;
      max-width: 100%;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 12px 32px rgba(15, 23, 42, 0.07);
      border: 1px solid var(--border-color);
      background-color: var(--card-bg);
    }
    .article-body-img-wrap img {
      width: 100%;
      height: auto;
      max-height: 440px;
      object-fit: cover;
      display: block;
    }

    /* GEO / Definition Box */
    .geo-definition, .geo-definition-box, .article-geo-definition {
      background: rgba(37, 99, 235, 0.05) !important;
      border: 1px solid var(--border-color) !important;
      border-left: 4px solid var(--accent) !important;
      padding: 24px 30px !important;
      border-radius: 14px !important;
      margin: 36px 0 !important;
      font-size: 1.1rem !important;
      line-height: 1.8 !important;
      color: var(--text-main) !important;
      box-sizing: border-box;
    }

    /* CTA Box */
    .cta-article-box {
      background: linear-gradient(135deg, #0a0f1f 0%, #1e293b 100%);
      color: #ffffff;
      padding: 48px 36px;
      border-radius: 20px;
      margin-top: 60px;
      text-align: center;
      box-shadow: 0 16px 40px rgba(10, 15, 31, 0.15);
      max-width: 780px;
      margin-left: auto;
      margin-right: auto;
      box-sizing: border-box;
    }
    .cta-article-box h3 {
      color: #ffffff !important;
      font-family: 'DM Serif Display', serif;
      font-size: 2.1rem;
      margin: 0 0 14px 0;
    }
    .cta-article-box p {
      color: #94a3b8 !important;
      font-size: 1.1rem;
      margin: 0 0 28px 0;
    }
    .cta-btn {
      display: inline-block;
      background: #2563eb;
      color: #ffffff !important;
      font-weight: 600;
      padding: 14px 32px;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.2s ease, transform 0.2s ease;
      font-size: 1rem;
    }
    .cta-btn:hover {
      background: #1d4ed8;
      transform: translateY(-2px);
    }

    /* Responsive Mobile Boxed Padding */
    @media (max-width: 768px) {
      .article-outer-wrapper { padding: 16px 12px 40px 12px; }
      .article-card-box { padding: 32px 20px; border-radius: 16px; }
      .hero-title { font-size: 1.95rem; }
      .site-nav { display: none; }
      .blog-content h2 { font-size: 1.65rem; }
      .cta-article-box { padding: 32px 20px; }
    }
  </style>

  <!-- Schema.org BlogPosting -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{description}",
    "image": "https://datrey.ma/assets/blog/{slug}-1.webp",
    "publisher": {
      "@type": "Organization",
      "name": "DatRey SARL",
      "logo": {
        "@type": "ImageObject",
        "url": "https://datrey.ma/assets/logo.webp"
      }
    },
    "url": "https://datrey.ma/blog/{slug}.html",
    "inLanguage": "fr-MA"
  }
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

  <main class="article-outer-wrapper">
    <div class="article-card-box">
      <!-- Centered Header Section -->
      <div class="article-header-centered">
        <span class="category-badge">{category}</span>
        <h1 class="hero-title">{title}</h1>
        <div class="hero-meta">
          <span>📅 Publié le {pub_date} à {pub_time}</span> • <span>Par l'équipe DatRey</span> • <span>Temps de lecture : ~6 min</span>
        </div>
      </div>

      <!-- Featured Hero Image -->
      <div class="article-hero-img-wrap">
        <img src="../assets/blog/{slug}-1.webp" alt="{title}" />
      </div>

      <!-- Article Reading Content -->
      <article class="blog-content">
        {content}
      </article>

      <!-- CTA Box -->
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

    now = datetime.now()
    pub_date = article_data.get("date", now.strftime("%d/%m/%Y"))
    pub_time = article_data.get("publish_time", now.strftime("%H:%M"))

    clean_title = re.sub(r'\s*\|\s*Blog\s*DatRey.*$', '', raw_title, flags=re.IGNORECASE).strip()

    content_with_images = inject_inbody_images(content_raw, slug, clean_title)

    full_html = ARTICLE_TEMPLATE.replace("{title}", clean_title)\
                                .replace("{description}", desc)\
                                .replace("{slug}", slug)\
                                .replace("{category}", cat)\
                                .replace("{pub_date}", pub_date)\
                                .replace("{pub_time}", pub_time)\
                                .replace("{content}", content_with_images)

    os.makedirs(BLOG_DIR, exist_ok=True)
    out_path = os.path.join(BLOG_DIR, f"{slug}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[Site Builder] Article HTML created -> blog/{slug}.html")
    update_blog_data_json({**article_data, "title": clean_title, "date": pub_date, "publish_time": pub_time})
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
    
    now = datetime.now()
    pub_date = article_data.get("date", now.strftime("%d/%m/%Y"))
    pub_time = article_data.get("publish_time", now.strftime("%H:%M"))

    new_entry = {
        "title": clean_title,
        "slug": article_data["slug"],
        "description": article_data["description"],
        "category": article_data["category"],
        "date": pub_date,
        "publish_time": pub_time,
        "formatted_date_time": f"Publié le {pub_date} à {pub_time}",
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

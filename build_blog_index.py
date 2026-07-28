import json

def build_blog_index():
    with open('blog_data.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # HTML header and hero section
    html = """<!DOCTYPE html>
<html lang="fr" dir="ltr" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog DatRey | Actualités et Expertise Digitales</title>
  <meta name="description" content="Découvrez nos articles, guides et études de cas sur l'acquisition digitale, le SEO, les Ads, et la stratégie au Maroc." />
  <meta property="og:title" content="Blog DatRey | Expertise Full-Stack" />
  <meta property="og:description" content="Découvrez nos articles, guides et études de cas sur l'acquisition digitale." />
  <meta property="og:image" content="https://datrey.ma/assets/logo.webp" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://datrey.ma/blog.html" />
  <link rel="canonical" href="https://datrey.ma/blog.html" />
  <link rel="stylesheet" href="style.css" />
  <link rel="icon" href="assets/logo.webp" type="image/webp" />
  <meta name="theme-color" content="#ffffff" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap" />
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
  <script defer src="shared.js"></script>
  <style>
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 30px;
      margin-top: 40px;
    }
    .blog-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      overflow: hidden;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .blog-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }
    .blog-card-img {
      width: 100%;
      height: 200px;
      object-fit: cover;
      background: #f1f5f9;
    }
    .blog-card-content {
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .blog-card-category {
      color: #2563eb;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }
    .blog-card-title {
      font-size: 1.25rem;
      color: #0f172a;
      margin-bottom: 12px;
      line-height: 1.4;
    }
    .blog-card-desc {
      color: #475569;
      font-size: 0.95rem;
      line-height: 1.6;
      margin-bottom: 20px;
      flex: 1;
    }
    .blog-card-link {
      color: #2563eb;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: color 0.3s ease;
    }
    .blog-card-link:hover {
      color: #1d4ed8;
    }
  </style>
</head>
<body>
  <script>document.documentElement.setAttribute('data-theme','light');</script>
  
  <header class="header" id="header">
    <div class="container">
      <a href="index.html" class="logo" aria-label="DatRey — Accueil">
        <img src="assets/logo.webp" alt="DatRey Logo" width="40" height="40" />
        <span><span class="logo-blue">D</span>at<span class="logo-blue">R</span>ey</span>
      </a>
      <nav class="nav-links" aria-label="Navigation principale">
        <a href="index.html">Accueil</a>
        <a href="services.html">Nos Services</a>
        <a href="blog.html" class="nav-active">Blog</a>
        <a href="contact.html">Contact</a>
        <a href="contact.html" class="btn btn-primary nav-cta">Audit Gratuit</a>
      </nav>
      <div style="display: flex; align-items: center; gap: 16px;">
        <button class="mobile-toggle" id="mobileToggle" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <section class="page-hero">
    <div class="container text-center">
      <h1 class="hero-title">Notre Blog &amp; Expertise</h1>
      <p class="hero-subtitle">Guides complets, études de cas et stratégies d'acquisition pour les entreprises exigeantes.</p>
    </div>
  </section>

  <main id="main-content" class="section-padding">
    <div class="container">
      <div class="blog-grid reveal">
"""

    for article in articles:
        desc = article.get("description", article.get("desc", ""))
        html += f"""
        <article class="blog-card">
          <img src="assets/blog/{article['slug']}-1.webp" alt="{article['title']}" class="blog-card-img" loading="lazy" />
          <div class="blog-card-content">
            <span class="blog-card-category">{article['category']}</span>
            <h2 class="blog-card-title">{article['title']}</h2>
            <p class="blog-card-desc">{desc}</p>
            <a href="blog/{article['slug']}.html" class="blog-card-link">Lire l'article &rarr;</a>
          </div>
        </article>
"""

    html += """
      </div>
    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <p style="text-align:center; color:#64748b;">&copy; 2026 DatRey SARL. Tous droits réservés.</p>
    </div>
  </footer>
</body>
</html>
"""

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("blog.html generated successfully.")

if __name__ == "__main__":
    build_blog_index()

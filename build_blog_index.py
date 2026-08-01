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
        <img src="assets/logo.webp" alt="DatRey Logo" class="logo-img" width="40" height="40" />
        <span><span class="logo-blue">D</span>at<span class="logo-blue">R</span>ey</span>
      </a>
      <nav class="nav-links" aria-label="Navigation principale">
        <a href="index.html">Accueil</a>
        <a href="creation-site-web.html">Création Site Web</a>
        <a href="services.html">Nos Services</a>
        <a href="blog.html" class="nav-active">Blog</a>
        <a href="contact.html">Contact</a>
        <a href="contact.html?subject=AuditGratuit" class="btn btn-primary nav-cta">Audit Gratuit</a>
      </nav>
      <div style="display: flex; align-items: center; gap: 16px;">
        <div class="lang-selector">
          <button aria-label="Changer de langue" class="lang-btn">FR ▼</button>
          <div class="lang-dropdown">
            <a href="index.html">Français</a>
            <a href="/en/">English</a>
          </div>
        </div>
        <button aria-label="Basculer le thème" class="theme-toggle" id="themeToggle">
          <svg class="sun-icon" fill="none" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20"><circle cx="12" cy="12" r="5"></circle><line x1="12" x2="12" y1="1" y2="3"></line><line x1="12" x2="12" y1="21" y2="23"></line><line x1="4.22" x2="5.64" y1="4.22" y2="5.64"></line><line x1="18.36" x2="19.78" y1="18.36" y2="19.78"></line><line x1="1" x2="3" y1="12" y2="12"></line><line x1="21" x2="23" y1="12" y2="12"></line><line x1="4.22" x2="5.64" y1="19.78" y2="18.36"></line><line x1="18.36" x2="19.78" y1="5.64" y2="4.22"></line></svg>
          <svg class="moon-icon" fill="none" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
        <button aria-label="Menu" class="mobile-toggle" id="mobileToggle">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div aria-label="Navigation mobile" class="mobile-nav" id="mobileNav" role="navigation">
    <button aria-label="Fermer le menu" class="mobile-nav-close" id="mobileClose">×</button>
    <a href="index.html" onclick="closeMobileNav()">Accueil</a>
    <a href="creation-site-web.html" onclick="closeMobileNav()">Création Site Web</a>
    <a href="services.html" onclick="closeMobileNav()">Nos Services</a>
    <a href="blog.html" class="nav-active" onclick="closeMobileNav()">Blog</a>
    <a href="contact.html" onclick="closeMobileNav()">Contact</a>
    <a class="btn btn-primary magnetic-btn" href="contact.html?subject=AuditGratuit" onclick="closeMobileNav()">Audit Gratuit</a>
  </div>

  <section class="page-hero">
    <div class="container text-center">
      <h1 class="hero-title">Notre Blog &amp; Expertise</h1>
      <p class="hero-subtitle">Guides complets, études de cas et stratégies d'acquisition pour les entreprises exigeantes.</p>
    </div>
  </section>

  <main id="main-content" class="section-padding">
    <div class="container">
      <div class="blog-grid">
"""

    for article in articles:
        desc = article.get("description", article.get("desc", ""))
        raw_date = article.get("date", "2026-08-01")
        raw_time = article.get("publish_time", "13:00")
        formatted_datetime = article.get("formatted_date_time", f"{raw_date} à {raw_time}")
        
        html += f"""
        <article class="blog-card">
          <img src="assets/blog/{article['slug']}-1.webp" alt="{article['title']}" class="blog-card-img" loading="lazy" />
          <div class="blog-card-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span class="blog-card-category">{article['category']}</span>
              <span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">📅 {raw_date} • {raw_time}</span>
            </div>
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
      <div class="footer-grid">
        <div>
          <a href="index.html" class="footer-logo">
            <img src="assets/logo.webp" alt="DatRey Logo" width="36" height="36" style="border-radius:8px;" />
            <span><span class="logo-blue">D</span>at<span class="logo-blue">R</span>ey</span>
          </a>
          <p class="footer-desc">Agence d'acquisition digitale &amp; Growth Hacking au Maroc. Nous transformons votre budget marketing en ROI mesurable.</p>
          <div class="social-links">
            <a aria-label="LinkedIn DatRey" href="https://www.linkedin.com/in/datrey-agency/" rel="noopener noreferrer" target="_blank">
              <svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect height="12" width="4" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle></svg>
            </a>
            <a aria-label="X DatRey" href="https://x.com/Datrey_Agency" rel="noopener noreferrer" target="_blank">
              <svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20"><path d="M4 4l11.73 16h5L9 4H4z"></path><path d="M4 20l6.76-9.33L18 4"></path></svg>
            </a>
            <a aria-label="Instagram DatRey" href="https://www.instagram.com/datrey.agency/" rel="noopener noreferrer" target="_blank">
              <svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20"><rect height="20" rx="5" ry="5" width="20" x="2" y="2"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"></line></svg>
            </a>
            <a aria-label="Pinterest DatRey" href="https://www.pinterest.com/DatreyAgency" rel="noopener noreferrer" target="_blank">
              <svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20"><line x1="12" x2="12" y1="12" y2="22"></line><path d="M12 22c-3.5 0-6.5-2.5-7.5-6s.5-7 4-8.5 7-1 9.5 2 2 6-.5 8.5L12 22z"></path><circle cx="12" cy="7" r="1"></circle></svg>
            </a>
          </div>
        </div>
        <div>
          <h3>Navigation</h3>
          <div class="footer-links">
            <a href="index.html">Accueil</a>
            <a href="creation-site-web.html">Création Site Web</a>
            <a href="services.html">Nos Services</a>
            <a href="transformation-digitale.html">Transformation Digitale</a>
            <a href="blog.html">Blog</a>
            <a href="a-propos.html">À propos</a>
            <a href="cas-clients.html">Cas Clients</a>
            <a href="contact.html">Contact</a>
          </div>
        </div>
        <div>
          <h3>Services</h3>
          <div class="footer-links">
            <a href="services-google-ads.html">Google Ads (SEA)</a>
            <a href="services-meta-ads.html">Meta Ads</a>
            <a href="services-seo.html">SEO &amp; Contenu</a>
            <a href="services-cro.html">CRO &amp; Landing Pages</a>
            <a href="services-emailing.html">Email &amp; Automation</a>
            <a href="services-strategie.html">Stratégie d'Acquisition</a>
            <a href="services-gmb-360.html">Visite Virtuelle 360°</a>
          </div>
        </div>
        <div>
          <h3>Contact</h3>
          <div class="footer-contact-item">
            <span class="footer-contact-icon"><svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg></span>
            <span>5, rue de Dixmude, 1er étage, appt 2,<br/>Benjdia — Casablanca</span>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon"><svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg></span>
            <a href="mailto:contact@datrey.ma" style="color:inherit;">contact@datrey.ma</a>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon"><svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg></span>
            <a href="tel:+212644443059" style="color:inherit;">+212 6 44 44 30 59</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 DatRey. Tous droits réservés.</span>
        <div style="display:flex;gap:20px;">
          <a href="mentions-legales.html">Mentions légales</a>
          <a href="politique-confidentialite.html">Politique de confidentialité</a>
        </div>
      </div>
    </div>
  </footer>
  <a aria-label="Nous contacter sur WhatsApp" class="whatsapp-float" href="https://wa.me/212644443059" rel="noopener noreferrer" target="_blank">
    <svg fill="currentColor" height="28" viewbox="0 0 24 24" width="28"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>
  </a>
</body>
</html>
"""

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("blog.html generated successfully.")

if __name__ == "__main__":
    build_blog_index()

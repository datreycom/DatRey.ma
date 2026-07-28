import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from autopilot.config import MAKE_WEBHOOK_URL

def generate_social_posts(article_data):
    """
    Formats multi-channel social media posts (LinkedIn, Instagram, Facebook) with a rich 250-300 word executive summary,
    hero cover photo URL, and high-reach engagement elements tailored for DatRey.
    """
    title = article_data["title"]
    slug = article_data["slug"]
    desc = article_data["description"]
    category = article_data["category"]
    social_summary = article_data.get("social_summary", desc)
    article_url = f"https://datrey.ma/blog/{slug}.html"
    hero_image_url = f"https://datrey.ma/assets/blog/{slug}-1.webp"

    # Hashtags high-reach
    hashtags = f"#DatRey #MarketingDigital #Maroc #Acquisition #{category.replace(' ', '')} #CroissanceDigital #Casablanca #Rabat #SEO #GoogleAds #ROI"

    # 1. LinkedIn Post (250-300 words executive summary + cover photo + CTA)
    linkedin_post = f"""🚀 [NOUVEL ARTICLE EXPERT] : {title}

{social_summary}

💡 POUR ALLER PLUS LOIN :
Retrouvez notre étude complète avec tous les chiffres, infographies et cas pratiques sur notre blog officiel :
👉 {article_url}

---
 DatRey SARL - Agence de Marketing Digital & Acquisition au Maroc
📍 Casablanca & Rabat | 🌐 datrey.ma

{hashtags}"""

    # 2. Instagram Post (250-300 words summary + cover photo + CTA)
    instagram_post = f"""📌 {title}

{social_summary}

🔗 Cliquez sur le lien dans notre bio pour lire l'article complet ou rendez-vous sur : {article_url}

-
{hashtags}"""

    # 3. Facebook Post (250-300 words summary + cover photo + CTA)
    facebook_post = f"""📌 [DÉCRYPTAGE & STRATÉGIE] : {title}

{social_summary}

👉 Lisez l'analyse intégrale et téléchargez nos recommandations sur notre site :
{article_url}

 DatRey Digital Agency - Votre partenaire croissance au Maroc.
{hashtags}"""

    payload = {
        "event": "new_blog_article",
        "title": title,
        "slug": slug,
        "category": category,
        "description": desc,
        "social_summary": social_summary,
        "url": article_url,
        "hero_image_url": hero_image_url,
        "social": {
            "linkedin": linkedin_post,
            "instagram": instagram_post,
            "facebook": facebook_post
        }
    }

    return payload

def publish_to_make_webhook(payload):
    """
    Sends the article, 250-300 word summary, cover photo URL and social posts payload to Make.com Webhook endpoint.
    """
    if not MAKE_WEBHOOK_URL:
        print("[Social Publisher] Info: MAKE_WEBHOOK_URL is not set. Social payload formatted successfully.")
        return False

    try:
        print(f"[Social Publisher] Dispatching webhook payload to Make.com -> {MAKE_WEBHOOK_URL}")
        res = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=30, verify=False)
        if res.status_code in (200, 201, 202):
            print("[Social Publisher] Make.com Webhook successfully triggered for LinkedIn, Instagram & Facebook!")
            return True
        else:
            print(f"[Social Publisher] Webhook returned status {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[Social Publisher] Webhook error: {e}")

    return False

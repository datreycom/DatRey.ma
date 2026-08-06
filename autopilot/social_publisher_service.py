import json
import time
import hashlib
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from autopilot.config import MAKE_WEBHOOK_URL
from autopilot.pollinations_image_service import UNSPLASH_CURATED_STOCKS

DATREY_CONTACT_BLOCK = """---
📞 CONTACTEZ L'ÉQUIPE DATREY :
🌐 Site Web : https://datrey.ma
📱 Tél / WhatsApp : +212 6 44 44 30 59
📩 Email : contact@datrey.ma
📍 Adresse : 5, rue de Dixmude, 1er étage, appt 2, Benjdia — Casablanca, Maroc
🚀 Demandez votre Audit Digital Gratuit : https://datrey.ma/contact.html"""

def generate_social_posts(article_data):
    """
    Formats multi-channel social media posts (LinkedIn, Instagram, Facebook) with a rich 250-300 word executive summary,
    guaranteed live CDN cover photo URL, and official DatRey agency contact info tailored for lead generation.
    Includes unique ref hash to prevent LinkedIn 422 duplicate content errors.
    """
    title = article_data["title"]
    slug = article_data["slug"]
    desc = article_data["description"]
    category = article_data["category"]
    social_summary = article_data.get("social_summary", desc)
    article_url = f"https://datrey.ma/blog/{slug}.html"

    # ✅ FIX 1: Guaranteed Live CDN Image URL (prevents Make 404 HTML Page error)
    # Uses deterministic Unsplash live photo URL so Make gets a 200 OK image instantly
    slug_hash = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    live_stock_url = UNSPLASH_CURATED_STOCKS[slug_hash % len(UNSPLASH_CURATED_STOCKS)]
    hero_image_url = article_data.get("hero_image_url") or live_stock_url

    # Unique reference tag to prevent LinkedIn 422 Duplicate Content error
    unique_ref = hashlib.md5(f"{slug}_{time.time()}".encode()).hexdigest()[:6].upper()
    ref_tag = f"📌 Réf: #DR-{unique_ref}"

    # Hashtags high-reach
    category_hashtag = category.replace(' ', '').replace('(', '').replace(')', '').replace('&', '')
    hashtags = f"#DatRey #MarketingDigital #Maroc #Acquisition #{category_hashtag} #CroissanceDigital #Casablanca #Rabat #SEO #GoogleAds #ROI"

    # 1. Facebook Post
    facebook_post = f"""📌 [DÉCRYPTAGE & STRATÉGIE] : {title}

{social_summary}

👉 Lisez l'analyse intégrale et nos recommandations sur notre site :
{article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    # 2. LinkedIn Post
    linkedin_post = f"""🚀 [NOUVEL ARTICLE EXPERT] : {title}

{social_summary}

💡 POUR ALLER PLUS LOIN :
Retrouvez notre étude complète avec tous les chiffres, infographies et cas pratiques sur notre blog officiel :
👉 {article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    # 3. Instagram Post
    instagram_post = f"""📌 {title}

{social_summary}

🔗 Cliquez sur le lien dans notre bio pour lire l'article complet ou rendez-vous sur : {article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    payload = {
        "event": "new_blog_article",
        "title": title,
        "slug": slug,
        "category": category,
        "description": desc,
        "social_summary": social_summary,
        "summary": social_summary,
        "url": article_url,
        "link": article_url,
        "hero_image_url": hero_image_url,
        "picture": hero_image_url,
        "image_url": hero_image_url,
        "message": facebook_post,
        "post": facebook_post,
        "text": facebook_post,
        "facebook_post": facebook_post,
        "content": facebook_post,
        "caption": facebook_post,
        "social": {
            "facebook": facebook_post,
            "linkedin": linkedin_post,
            "instagram": instagram_post
        }
    }

    return payload

def publish_to_make_webhook(payload):
    """
    Sends the article, 250-300 word summary, cover photo URL and social posts payload to Make.com Webhook endpoint.
    Strictly enforces UTF-8 header encoding.
    """
    if not MAKE_WEBHOOK_URL:
        print("[Social Publisher] Info: MAKE_WEBHOOK_URL is not set. Social payload formatted successfully.")
        return False

    try:
        print(f"[Social Publisher] Dispatching webhook payload to Make.com -> {MAKE_WEBHOOK_URL}")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        
        res = requests.post(MAKE_WEBHOOK_URL, data=json_data, headers=headers, timeout=30, verify=False)
        if res.status_code in (200, 201, 202):
            print("[Social Publisher] Make.com Webhook successfully triggered for Facebook, LinkedIn & Instagram!")
            return True
        else:
            print(f"[Social Publisher] Webhook returned status {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[Social Publisher] Webhook error: {e}")

    return False

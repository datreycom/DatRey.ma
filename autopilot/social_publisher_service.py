import os
import json
import time
import hashlib
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from autopilot.config import MAKE_WEBHOOK_URL, BASE_DIR
from autopilot.pollinations_image_service import UNSPLASH_CURATED_STOCKS

PENDING_WEBHOOKS_FILE = os.path.join(BASE_DIR, "pending_webhooks.json")

# Delay between each webhook dispatch (seconds) — prevents LinkedIn 422 duplicate
INTER_WEBHOOK_DELAY = 30

# Time to wait for GitHub Pages deployment before dispatching (seconds)
DEPLOY_WAIT_TIME = 180  # 3 minutes

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
    Guarantees article_url is embedded in ALL payload keys (summary, description, message, posts).
    Includes unique ref hash to prevent LinkedIn 422 duplicate content errors.
    """
    title = article_data["title"]
    slug = article_data["slug"]
    desc = article_data["description"]
    category = article_data["category"]
    social_summary = article_data.get("social_summary", desc)
    article_url = f"https://datrey.ma/blog/{slug}.html"

    # Ensure article_url is ALWAYS embedded in social_summary if missing
    if article_url not in social_summary:
        social_summary_with_url = f"{social_summary}\n\n👉 Lisez l'article complet sur notre site :\n🔗 {article_url}"
    else:
        social_summary_with_url = social_summary

    # Primary image: datrey.ma hosted (will be live after deploy)
    # Fallback: guaranteed Unsplash CDN URL
    datrey_image_url = f"https://datrey.ma/assets/blog/{slug}-1.webp"
    slug_hash = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    fallback_image_url = UNSPLASH_CURATED_STOCKS[slug_hash % len(UNSPLASH_CURATED_STOCKS)]

    # Store both so dispatch can verify and pick the right one
    hero_image_url = datrey_image_url

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
🔗 {article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    # 2. LinkedIn Post
    linkedin_post = f"""🚀 [NOUVEL ARTICLE EXPERT] : {title}

{social_summary}

💡 POUR ALLER PLUS LOIN :
Retrouvez notre étude complète avec tous les chiffres, infographies et cas pratiques sur notre blog officiel :
👉 🔗 {article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    # 3. Instagram Post
    instagram_post = f"""📌 {title}

{social_summary}

🔗 Cliquez sur le lien dans notre bio pour lire l'article complet ou rendez-vous sur :
👉 {article_url}

{DATREY_CONTACT_BLOCK}

{hashtags}
{ref_tag}"""

    payload = {
        "event": "new_blog_article",
        "title": title,
        "slug": slug,
        "category": category,
        "description": f"{desc}\n\n👉 🔗 {article_url}",
        "social_summary": social_summary_with_url,
        "summary": social_summary_with_url,
        "url": article_url,
        "link": article_url,
        "article_url": article_url,
        "hero_image_url": hero_image_url,
        "picture": hero_image_url,
        "image_url": hero_image_url,
        "_fallback_image_url": fallback_image_url,
        "message": facebook_post,
        "post": facebook_post,
        "text": facebook_post,
        "facebook_post": facebook_post,
        "linkedin_post": linkedin_post,
        "instagram_post": instagram_post,
        "content": facebook_post,
        "caption": facebook_post,
        "social": {
            "facebook": facebook_post,
            "linkedin": linkedin_post,
            "instagram": instagram_post
        }
    }

    return payload


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1: Save webhook payloads to disk (called during generation)
# ─────────────────────────────────────────────────────────────────────────────

def save_pending_webhook(payload):
    """
    Appends a webhook payload to pending_webhooks.json.
    The webhook will be dispatched AFTER git push + GitHub Pages deploy.
    """
    pending = []
    if os.path.exists(PENDING_WEBHOOKS_FILE):
        try:
            with open(PENDING_WEBHOOKS_FILE, "r", encoding="utf-8") as f:
                pending = json.load(f)
        except (json.JSONDecodeError, Exception):
            pending = []

    pending.append(payload)

    with open(PENDING_WEBHOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)

    print(f"[Social Publisher] Webhook payload saved to pending queue ({len(pending)} total). Will dispatch after deploy.")


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: Dispatch pending webhooks AFTER deployment (called post-deploy)
# ─────────────────────────────────────────────────────────────────────────────

def _verify_image_url(url, max_retries=3):
    """
    Verifies that an image URL returns HTTP 200 with image content-type.
    Retries up to max_retries times with 10s backoff.
    """
    for attempt in range(max_retries):
        try:
            res = requests.head(url, timeout=10, allow_redirects=True)
            content_type = res.headers.get("content-type", "")
            if res.status_code == 200 and ("image" in content_type or "octet" in content_type):
                print(f"[Image Verify] [OK] {url} -> 200 OK ({content_type})")
                return True
            else:
                print(f"[Image Verify] [WARN] Attempt {attempt+1}/{max_retries}: {url} -> {res.status_code} ({content_type})")
        except Exception as e:
            print(f"[Image Verify] [WARN] Attempt {attempt+1}/{max_retries}: {url} -> Error: {e}")

        if attempt < max_retries - 1:
            time.sleep(10)

    return False


def _resolve_image_url(payload):
    """
    Tries the primary datrey.ma image URL. If it returns 404, falls back to Unsplash CDN.
    Updates the payload in-place with the verified URL.
    """
    primary_url = payload.get("hero_image_url", "")
    fallback_url = payload.get("_fallback_image_url", "")

    if primary_url and _verify_image_url(primary_url):
        return primary_url

    print(f"[Image Resolve] Primary image unavailable. Using Unsplash fallback.")
    if fallback_url:
        # Update all image fields in payload
        for key in ("hero_image_url", "picture", "image_url"):
            payload[key] = fallback_url
        return fallback_url

    return primary_url


def dispatch_pending_webhooks():
    """
    Reads pending_webhooks.json, verifies image URLs, and dispatches each webhook
    to Make.com with a 30-second delay between each to prevent duplicate content errors.
    Called by autopilot.dispatch_webhooks AFTER git push + GitHub Pages deploy.
    """
    if not os.path.exists(PENDING_WEBHOOKS_FILE):
        print("[Post-Deploy Dispatcher] No pending webhooks found. Nothing to dispatch.")
        return

    try:
        with open(PENDING_WEBHOOKS_FILE, "r", encoding="utf-8") as f:
            pending = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[Post-Deploy Dispatcher] Error reading pending webhooks: {e}")
        return

    if not pending:
        print("[Post-Deploy Dispatcher] Pending webhooks file is empty. Nothing to dispatch.")
        return

    print(f"[Post-Deploy Dispatcher] Found {len(pending)} pending webhook(s) to dispatch.")
    print(f"[Post-Deploy Dispatcher] Waiting {DEPLOY_WAIT_TIME}s for GitHub Pages deployment...")
    time.sleep(DEPLOY_WAIT_TIME)

    success_count = 0
    fail_count = 0

    for idx, payload in enumerate(pending):
        slug = payload.get("slug", "unknown")
        print(f"\n--- [Dispatch {idx+1}/{len(pending)}] Article: '{slug}' ---")

        # 1. Verify and resolve image URL
        _resolve_image_url(payload)

        # 2. Remove internal fallback field before sending
        payload.pop("_fallback_image_url", None)

        # 3. Send to Make.com
        if publish_to_make_webhook(payload):
            success_count += 1
        else:
            fail_count += 1

        # 4. Wait between dispatches to prevent LinkedIn duplicate content
        if idx < len(pending) - 1:
            print(f"[Post-Deploy Dispatcher] Waiting {INTER_WEBHOOK_DELAY}s before next dispatch...")
            time.sleep(INTER_WEBHOOK_DELAY)

    # 5. Clean up pending file
    try:
        os.remove(PENDING_WEBHOOKS_FILE)
        print(f"\n[Post-Deploy Dispatcher] Cleaned up pending_webhooks.json")
    except Exception:
        pass

    print(f"\n==========================================================")
    print(f"[Post-Deploy Dispatcher] Dispatch complete: {success_count} success, {fail_count} failed")
    print(f"==========================================================")


def publish_to_make_webhook(payload):
    """
    Sends a single webhook payload to Make.com.
    Includes retry logic with exponential backoff for transient failures.
    """
    if not MAKE_WEBHOOK_URL:
        print("[Social Publisher] Info: MAKE_WEBHOOK_URL is not set. Skipping.")
        return False

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[Social Publisher] Dispatching webhook to Make.com (attempt {attempt+1}/{max_retries})")
            headers = {"Content-Type": "application/json; charset=utf-8"}
            json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

            res = requests.post(MAKE_WEBHOOK_URL, data=json_data, headers=headers, timeout=30, verify=False)
            if res.status_code in (200, 201, 202):
                print("[Social Publisher] [OK] Make.com Webhook triggered successfully!")
                return True
            else:
                print(f"[Social Publisher] [WARN] Webhook returned status {res.status_code}: {res.text[:200]}")
                # Don't retry on 4xx client errors (except 429)
                if 400 <= res.status_code < 500 and res.status_code != 429:
                    return False
        except Exception as e:
            print(f"[Social Publisher] [WARN] Webhook error: {e}")

        if attempt < max_retries - 1:
            backoff = (attempt + 1) * 5
            print(f"[Social Publisher] Retrying in {backoff}s...")
            time.sleep(backoff)

    print("[Social Publisher] [ERROR] All retry attempts exhausted.")
    return False


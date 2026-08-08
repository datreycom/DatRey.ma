import os
import json
import time
from datetime import datetime
from autopilot.config import (
    SERVICES,
    get_autopilot_state,
    save_autopilot_state,
    calculate_daily_quota
)
from autopilot.deepseek_client import generate_article_content
from autopilot.humanizer_engine import apply_humanizer_audit, verify_geo_intro
from autopilot.pollinations_image_service import generate_article_images
from autopilot.site_builder_service import build_article_page
from autopilot.social_publisher_service import generate_social_posts, save_pending_webhook

def run_autopilot_cycle(force_count=None, topic_hint=None):
    """
    Runs a complete autopilot cycle based on the progressive schedule:
    - Calculates daily quota for active week.
    - Generates articles, 5 images each, builds HTML pages, updates sitemaps, and triggers social publishing webhooks.
    """
    state = get_autopilot_state()
    schedule_info = calculate_daily_quota(state)

    quota = force_count if force_count is not None else schedule_info["quota"]
    week_num = schedule_info["week"]

    print("==========================================================")
    print(f"[DatRey Autopilot Engine] Starting Cycle")
    print(f"Active Week: Week {week_num} | Daily Quota Target: {quota} articles/day")
    print("==========================================================")

    service_keys = list(SERVICES.keys())
    generated_count = state.get("total_generated", 0)

    # Load 90-Day Editorial Calendar
    calendar_data = []
    calendar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "editorial_calendar_90_days.json")
    if os.path.exists(calendar_path):
        with open(calendar_path, "r", encoding="utf-8") as f:
            calendar_data = json.load(f)

    results = []

    for i in range(quota):
        current_index = generated_count + i
        
        # Check if calendar entry exists
        if current_index < len(calendar_data):
            cal_entry = calendar_data[current_index]
            scheduled_title = cal_entry["title"]
            target_category_name = cal_entry["category"]
            
            # Map category name to slug
            service_slug = "google-ads"
            for slug, name in SERVICES.items():
                if name.lower() == target_category_name.lower():
                    service_slug = slug
                    break
            
            print(f"\n--- [Article {i+1}/{quota}] [Calendar #{cal_entry['post_id']}] Category: '{target_category_name}' ---")
            print(f"Scheduled Title: '{scheduled_title}'")
            
            raw_article = generate_article_content(service_slug=service_slug, topic_hint=scheduled_title)
        else:
            # Fallback round-robin if beyond 256 posts
            cat_idx = current_index % len(service_keys)
            service_slug = service_keys[cat_idx]
            print(f"\n--- [Article {i+1}/{quota}] Generating for Service: '{SERVICES[service_slug]}' ---")
            raw_article = generate_article_content(service_slug=service_slug, topic_hint=topic_hint)

        try:
            # 2. Humanizer & GEO Audit
            raw_article["content"] = apply_humanizer_audit(raw_article["content"])
            raw_article["content"] = verify_geo_intro(raw_article["content"], raw_article["title"], raw_article["category"])

            # 3. Pollinations/Unsplash HD Image Generation (5 Flux/Unsplash images)
            generate_article_images(raw_article["slug"], raw_article.get("image_prompts", []))

            # 4. Site Builder (HTML + Index + Sitemap)
            html_path = build_article_page(raw_article)

            # 5. Social Media Publisher — save payload for post-deploy dispatch
            # Webhook is NOT sent here. It will be dispatched AFTER git push + GitHub Pages deploy.
            social_payload = generate_social_posts(raw_article)
            save_pending_webhook(social_payload)

            results.append({
                "slug": raw_article["slug"],
                "title": raw_article["title"],
                "html_path": html_path,
                "timestamp": datetime.now().isoformat()
            })

            time.sleep(2)  # Cool down between generations

        except Exception as e:
            print(f"[ERROR] Exception during generation of article {i+1}: {e}")

    # Update state
    state["total_generated"] = generated_count + len(results)
    state.setdefault("history", []).extend(results)
    save_autopilot_state(state)

    print("\n==========================================================")
    print(f"[DatRey Autopilot Engine] Cycle Completed! Generated {len(results)}/{quota} articles.")
    print("==========================================================")

    return results

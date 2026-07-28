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
from autopilot.social_publisher_service import generate_social_posts, publish_to_make_webhook

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

    results = []

    for i in range(quota):
        # Pick category in round-robin fashion
        cat_idx = (generated_count + i) % len(service_keys)
        service_slug = service_keys[cat_idx]

        print(f"\n--- [Article {i+1}/{quota}] Generating for Service: '{SERVICES[service_slug]}' ---")

        try:
            # 1. DeepSeek Generation (>= 1300 words)
            raw_article = generate_article_content(service_slug=service_slug, topic_hint=topic_hint)

            # 2. Humanizer & GEO Audit
            raw_article["content"] = apply_humanizer_audit(raw_article["content"])
            raw_article["content"] = verify_geo_intro(raw_article["content"], raw_article["title"], raw_article["category"])

            # 3. Pollinations Image Generation (5 Flux images)
            generate_article_images(raw_article["slug"], raw_article.get("image_prompts", []))

            # 4. Site Builder (HTML + Index + Sitemap)
            html_path = build_article_page(raw_article)

            # 5. Social Media Publisher (LinkedIn / Instagram Payload -> Make.com)
            social_payload = generate_social_posts(raw_article)
            publish_to_make_webhook(social_payload)

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

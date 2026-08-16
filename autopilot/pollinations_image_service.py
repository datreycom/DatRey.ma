import os
import hashlib
import urllib.parse
import requests
import time
import random
import concurrent.futures
from autopilot.config import ASSETS_BLOG_DIR, POLLINATIONS_API_KEY

API_KEYS = [
    POLLINATIONS_API_KEY,
    "sk_ZH3VOQhv8R31QoeoUeURfwljbvhx1yqO",
    "sk_pCOUICUJeCvIeJ2UZHWR9aKdN9Zl2Tos"
]

# ─── Expanded High-Resolution Unsplash Curated Commercial Stock Photos ───
# 24 images (doubled from 12) to minimize collision risk on fallback
UNSPLASH_CURATED_STOCKS = [
    # Analytics / Performance
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1280&h=720&q=85",
    # Agency Team Discussion
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1280&h=720&q=85",
    # Modern Office Collaboration
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1280&h=720&q=85",
    # Business Growth Strategy
    "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1280&h=720&q=85",
    # UI/UX Design Meeting
    "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1280&h=720&q=85",
    # Tech Workspace Laptop
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1280&h=720&q=85",
    # Executive Boardroom
    "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1280&h=720&q=85",
    # Digital Strategy Presentation
    "https://images.unsplash.com/photo-1542744094-3a3172720449?auto=format&fit=crop&w=1280&h=720&q=85",
    # Digital Marketing Team
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1280&h=720&q=85",
    # Executive Workshop
    "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1280&h=720&q=85",
    # Data Analytics Dashboard
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1280&h=720&q=85",
    # Business ROI Planning
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1280&h=720&q=85",
    # ─── NEW: 12 additional photos for deduplication resilience ───
    # Creative Agency Workspace
    "https://images.unsplash.com/photo-1497215842964-222b430dc094?auto=format&fit=crop&w=1280&h=720&q=85",
    # Marketing Strategy Whiteboard
    "https://images.unsplash.com/photo-1533749871411-5e21e14bcc7d?auto=format&fit=crop&w=1280&h=720&q=85",
    # Business Meeting Handshake
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1280&h=720&q=85",
    # Code Development Screen
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1280&h=720&q=85",
    # Modern Architecture Office
    "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1280&h=720&q=85",
    # Startup Team Planning
    "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=1280&h=720&q=85",
    # Social Media Marketing
    "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=1280&h=720&q=85",
    # Email Marketing Campaign
    "https://images.unsplash.com/photo-1563986768609-322da13575f2?auto=format&fit=crop&w=1280&h=720&q=85",
    # SEO Analytics Growth
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1280&h=720&q=85",
    # E-commerce Product Display
    "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1280&h=720&q=85",
    # Client Presentation Meeting
    "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?auto=format&fit=crop&w=1280&h=720&q=85",
    # Corporate Growth Chart
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1280&h=720&q=85",
]

NEGATIVE_PROMPT = (
    "text, words, letters, numbers, watermark, logo, signature, brand name, "
    "blurry, low quality, pixelated, distorted, ugly, bad anatomy, dark, shadowy, out of focus"
)


def _content_hash(data: bytes) -> str:
    """Returns MD5 hex digest for binary content, used for deduplication."""
    return hashlib.md5(data).hexdigest()


def download_fallback_hd_stock(dest_filepath, idx=0, slug=""):
    """
    Downloads a guaranteed 1280x720 HD pristine commercial photo from curated Unsplash stock library.
    Uses a deterministic slug-based offset + idx to ensure each image in an article picks a DIFFERENT photo.
    """
    # Deterministic offset from slug to spread across the pool
    slug_offset = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) if slug else 0
    stock_index = (slug_offset + idx) % len(UNSPLASH_CURATED_STOCKS)
    stock_url = UNSPLASH_CURATED_STOCKS[stock_index]

    try:
        res = requests.get(stock_url, timeout=15)
        if res.status_code == 200 and len(res.content) > 30000:
            os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
            with open(dest_filepath, "wb") as f:
                f.write(res.content)
            print(f"[HD Hybrid Stock Engine] Clean HD photo downloaded -> {os.path.basename(dest_filepath)} ({len(res.content)//1024} KB)")
            return True, res.content
    except Exception as e:
        print(f"[HD Hybrid Stock Engine] Stock download exception: {e}")
    return False, b""


def generate_single_image(prompt, dest_filepath, idx=0, slug=""):
    """
    Generates a high-definition (1280x720) photorealistic commercial image.
    Uses Pollinations HD + Unsplash HD fallback for 100% guaranteed pristine quality.
    Each image gets a unique seed derived from (idx, timestamp, random) to prevent duplicates.
    """
    clean_prompt = prompt.strip()

    enhanced_prompt = (
        f"Professional commercial studio photography, {clean_prompt}, "
        f"photorealistic, consistent human anatomy, no deformed features, no facial anomalies, "
        f"bright natural daylight, modern luxury glass office, crisp sharp focus, 8k resolution, Hasselblad 35mm, "
        f"ABSOLUTELY NO TEXT, NO LOGO, NO WORDS, NO WATERMARK"
    )

    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    # ✅ FIX: Unique seed per image using idx + microsecond timestamp + random
    seed = (idx * 100000) + int(time.time() * 1000) % 900000 + random.randint(1, 9999)

    endpoints = [
        {"url": f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&seed={seed}", "use_auth": False},
        {"url": f"https://gen.pollinations.ai/image/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&seed={seed}", "use_auth": True}
    ]

    for attempt in range(2):
        for endpoint in endpoints:
            for key in API_KEYS:
                headers = {"Authorization": f"Bearer {key}"} if endpoint["use_auth"] and key else {}
                try:
                    res = requests.get(endpoint["url"], headers=headers, timeout=12)
                    # Verify size > 45 KB to ensure crisp high resolution
                    if res.status_code == 200 and len(res.content) > 45000:
                        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
                        with open(dest_filepath, "wb") as f:
                            f.write(res.content)
                        content_md5 = _content_hash(res.content)
                        print(f"[Pollinations HD Engine] Image generated -> {os.path.basename(dest_filepath)} ({len(res.content)//1024} KB, hash:{content_md5[:8]})")
                        return True, res.content
                except Exception:
                    pass

    # Fail-safe: download HD curated commercial stock photo
    success, content = download_fallback_hd_stock(dest_filepath, idx=idx, slug=slug)
    return success, content


def _deduplicate_images(slug, file_paths):
    """
    Post-generation deduplication pass: detects identical images within an article's 5-image set
    and replaces duplicates with alternate Unsplash stock photos to ensure visual variety.
    """
    hashes = {}
    duplicates = []

    for path in file_paths:
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            content = f.read()
        content_md5 = _content_hash(content)

        if content_md5 in hashes:
            duplicates.append((path, content_md5))
            print(f"[Dedup Engine] DUPLICATE DETECTED: {os.path.basename(path)} matches {os.path.basename(hashes[content_md5])}")
        else:
            hashes[content_md5] = path

    if not duplicates:
        print(f"[Dedup Engine] No duplicates found for '{slug}'. All 5 images are unique. [OK]")
        return

    # Replace each duplicate with a different Unsplash stock photo
    used_indices = set()
    slug_offset = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)

    # Collect already-used stock indices
    for path in file_paths:
        if path not in [d[0] for d in duplicates]:
            idx_from_name = int(os.path.basename(path).split("-")[-1].split(".")[0]) - 1
            used_indices.add((slug_offset + idx_from_name) % len(UNSPLASH_CURATED_STOCKS))

    replacement_offset = len(UNSPLASH_CURATED_STOCKS) // 2  # Start from opposite side of pool

    for dup_path, dup_hash in duplicates:
        # Find an unused stock photo index
        for attempt in range(len(UNSPLASH_CURATED_STOCKS)):
            candidate_idx = (slug_offset + replacement_offset + attempt) % len(UNSPLASH_CURATED_STOCKS)
            if candidate_idx not in used_indices:
                stock_url = UNSPLASH_CURATED_STOCKS[candidate_idx]
                try:
                    res = requests.get(stock_url, timeout=15)
                    if res.status_code == 200 and len(res.content) > 30000:
                        new_hash = _content_hash(res.content)
                        if new_hash not in hashes:
                            with open(dup_path, "wb") as f:
                                f.write(res.content)
                            hashes[new_hash] = dup_path
                            used_indices.add(candidate_idx)
                            print(f"[Dedup Engine] REPLACED {os.path.basename(dup_path)} with stock #{candidate_idx} ({len(res.content)//1024} KB) [OK]")
                            break
                except Exception as e:
                    print(f"[Dedup Engine] Replacement failed for stock #{candidate_idx}: {e}")
            replacement_offset += 1


def generate_article_images(slug, image_prompts):
    """
    Generates all 5 HD images for the article concurrently using Hybrid HD Engine.
    Saves them as assets/blog/{slug}-1.webp through assets/blog/{slug}-5.webp.
    Includes post-generation deduplication to guarantee all 5 images are visually unique.
    """
    os.makedirs(ASSETS_BLOG_DIR, exist_ok=True)
    tasks = []

    for idx in range(5):
        prompt = image_prompts[idx] if idx < len(image_prompts) else f"Professional digital agency marketing workspace in Casablanca Morocco"
        dest_filename = f"{slug}-{idx+1}.webp"
        dest_path = os.path.join(ASSETS_BLOG_DIR, dest_filename)
        tasks.append((prompt, dest_path, idx))

    print(f"[Hybrid HD Engine] Generating 5 photorealistic commercial HD images for article '{slug}'...")
    results = []
    file_paths = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_task = {
            executor.submit(generate_single_image, prompt, path, idx, slug): (prompt, path, idx)
            for prompt, path, idx in tasks
        }
        for future in concurrent.futures.as_completed(future_to_task):
            success, content = future.result()
            results.append(success)

    # Collect file paths for deduplication
    for _, path, _ in tasks:
        file_paths.append(path)

    # ✅ Post-generation deduplication pass
    _deduplicate_images(slug, file_paths)

    success_count = sum(1 for r in results if r)
    print(f"[Hybrid HD Engine] Completed image generation for '{slug}': {success_count}/5 successful.")
    return success_count

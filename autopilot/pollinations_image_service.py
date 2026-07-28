import os
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

NEGATIVE_PROMPT = (
    "text, words, letters, numbers, watermark, logo, signature, brand name, "
    "blurry, low quality, pixelated, distorted, ugly, bad anatomy, cartoon, anime, 3d render, illustration"
)

def generate_single_image(prompt, dest_filepath):
    """
    Downloads a high-definition (1280x720) photorealistic commercial image from Pollinations API.
    Enforces strict HD photo quality and zero text.
    """
    clean_prompt = prompt.strip()
    
    # Enhanced prompt for photorealistic commercial studio quality
    enhanced_prompt = (
        f"Award-winning commercial studio photography, {clean_prompt}, "
        f"photorealistic corporate agency style, cinematic morning sunlight, 8k resolution, Hasselblad 35mm lens, hyperdetailed, "
        f"ABSOLUTELY NO TEXT, NO LOGO, NO WORDS, NO WATERMARK"
    )
    
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    encoded_negative = urllib.parse.quote(NEGATIVE_PROMPT)
    seed = random.randint(10000, 999999)

    endpoints = [
        # Flux Pro / Realism HD
        {"url": f"https://gen.pollinations.ai/image/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&enhance=true&seed={seed}&negative_prompt={encoded_negative}", "use_auth": True},
        {"url": f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&enhance=true&seed={seed}&negative_prompt={encoded_negative}", "use_auth": False},
        # Flux Klein fallback
        {"url": f"https://gen.pollinations.ai/image/{encoded_prompt}?model=klein&width=1280&height=720&nologo=true&seed={seed}", "use_auth": True}
    ]

    for attempt in range(3):
        for endpoint in endpoints:
            for key in API_KEYS:
                headers = {"Authorization": f"Bearer {key}"} if endpoint["use_auth"] and key else {}
                try:
                    res = requests.get(endpoint["url"], headers=headers, timeout=40)
                    if res.status_code == 200 and len(res.content) > 15000:
                        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
                        with open(dest_filepath, "wb") as f:
                            f.write(res.content)
                        print(f"[Pollinations HD Engine] Image generated -> {os.path.basename(dest_filepath)} ({len(res.content)//1024} KB)")
                        return True
                    elif res.status_code in (402, 429):
                        time.sleep(1)
                except Exception:
                    time.sleep(1)

    print(f"[Pollinations HD Engine] Failed to generate {os.path.basename(dest_filepath)}.")
    return False

def generate_article_images(slug, image_prompts):
    """
    Generates all 5 HD images for the article concurrently using Pollinations API.
    Saves them as assets/blog/{slug}-1.webp through assets/blog/{slug}-5.webp.
    """
    os.makedirs(ASSETS_BLOG_DIR, exist_ok=True)
    tasks = []

    for idx in range(5):
        prompt = image_prompts[idx] if idx < len(image_prompts) else f"Professional digital agency marketing workspace in Casablanca Morocco"
        dest_filename = f"{slug}-{idx+1}.webp"
        dest_path = os.path.join(ASSETS_BLOG_DIR, dest_filename)
        tasks.append((prompt, dest_path))

    print(f"[Pollinations HD Engine] Generating 5 photorealistic commercial HD images for article '{slug}'...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_task = {
            executor.submit(generate_single_image, prompt, path): (prompt, path)
            for prompt, path in tasks
        }
        for future in concurrent.futures.as_completed(future_to_task):
            res = future.result()
            results.append(res)

    success_count = sum(1 for r in results if r)
    print(f"[Pollinations HD Engine] Completed image generation for '{slug}': {success_count}/5 successful.")
    return success_count

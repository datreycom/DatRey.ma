import os
import urllib.parse
import requests
import time
import concurrent.futures
from autopilot.config import ASSETS_BLOG_DIR, POLLINATIONS_API_KEY

def generate_single_image(prompt, dest_filepath):
    """
    Downloads a single image generated via FLUX.2 Klein 4B (model=klein) from Pollinations API.
    Guarantees ABSOLUTELY NO TEXT in the generated visual art.
    """
    clean_prompt = prompt.strip()
    full_prompt = (
        f"{clean_prompt}. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO WATERMARK, NO SIGNATURE, NO LOGO. "
        f"Pure conceptual digital marketing art illustration, 8k resolution, photorealistic corporate agency style, cinematic lighting"
    )
    encoded_prompt = urllib.parse.quote(full_prompt)

    endpoints = [
        {"url": f"https://gen.pollinations.ai/image/{encoded_prompt}?model=klein&width=1200&height=675&nologo=true", "use_auth": True},
        {"url": f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=klein&width=1200&height=675&nologo=true", "use_auth": False}
    ]

    keys = [POLLINATIONS_API_KEY] if POLLINATIONS_API_KEY else [""]

    for attempt in range(3):
        for endpoint in endpoints:
            for key in keys:
                headers = {"Authorization": f"Bearer {key}"} if endpoint["use_auth"] and key else {}
                try:
                    res = requests.get(endpoint["url"], headers=headers, timeout=35)
                    if res.status_code == 200 and len(res.content) > 5000:
                        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
                        with open(dest_filepath, "wb") as f:
                            f.write(res.content)
                        print(f"[Pollinations Klein Engine] Image generated -> {os.path.basename(dest_filepath)} ({len(res.content)//1024} KB)")
                        return True
                    elif res.status_code in (402, 429):
                        time.sleep(1)
                except Exception:
                    time.sleep(1)

    print(f"[Pollinations Klein Engine] Failed to generate {os.path.basename(dest_filepath)}.")
    return False

def generate_article_images(slug, image_prompts):
    """
    Generates all 5 images for the article concurrently using FLUX.2 Klein 4B (model=klein).
    Saves them as assets/blog/{slug}-1.webp through assets/blog/{slug}-5.webp.
    """
    os.makedirs(ASSETS_BLOG_DIR, exist_ok=True)
    tasks = []

    for idx in range(5):
        prompt = image_prompts[idx] if idx < len(image_prompts) else f"Digital marketing visualization for {slug}"
        dest_filename = f"{slug}-{idx+1}.webp"
        dest_path = os.path.join(ASSETS_BLOG_DIR, dest_filename)
        tasks.append((prompt, dest_path))

    print(f"[Pollinations Klein Engine] Generating 5 FLUX.2 Klein images (NO TEXT) for article '{slug}'...")
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
    print(f"[Pollinations Klein Engine] Completed image generation for '{slug}': {success_count}/5 successful.")
    return success_count

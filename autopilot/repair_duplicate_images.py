"""
DatRey Blog Image Deduplication Repair Script
===============================================
Scans all existing blog images in assets/blog/, detects duplicate images
within each article's 5-image set, and replaces them with unique stock photos.
"""
import os
import sys
import hashlib
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

ASSETS_BLOG_DIR = os.path.join(BASE_DIR, "assets", "blog")

# Same expanded pool from pollinations_image_service.py
UNSPLASH_CURATED_STOCKS = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1542744094-3a3172720449?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1497215842964-222b430dc094?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1533749871411-5e21e14bcc7d?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1563986768609-322da13575f2?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?auto=format&fit=crop&w=1280&h=720&q=85",
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1280&h=720&q=85",
]


def content_hash(filepath):
    """Returns MD5 hex digest for a file."""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def group_by_article(blog_dir):
    """Groups image files by article slug (e.g., 'my-article-1.webp' -> slug='my-article')."""
    articles = {}
    for filename in os.listdir(blog_dir):
        if not filename.endswith(".webp"):
            continue
        # Extract slug: everything before the last '-N.webp'
        parts = filename.rsplit("-", 1)
        if len(parts) == 2 and parts[1].replace(".webp", "").isdigit():
            slug = parts[0]
            if slug not in articles:
                articles[slug] = []
            articles[slug].append(os.path.join(blog_dir, filename))
    return articles


def repair_duplicates():
    """Main repair function: scans all articles and replaces duplicate images."""
    if not os.path.exists(ASSETS_BLOG_DIR):
        print(f"[REPAIR] Blog assets directory not found: {ASSETS_BLOG_DIR}")
        return

    articles = group_by_article(ASSETS_BLOG_DIR)
    total_articles = len(articles)
    total_duplicates_found = 0
    total_replacements = 0
    global_used_stock_indices = set()  # Track used stocks globally to maximize variety

    print(f"[REPAIR] Scanning {total_articles} articles for duplicate images...")
    print("=" * 60)

    for slug, file_paths in sorted(articles.items()):
        file_paths.sort()  # Ensure consistent ordering (slug-1, slug-2, ...)

        # Hash each image
        hashes = {}
        duplicates = []
        for path in file_paths:
            if not os.path.exists(path):
                continue
            h = content_hash(path)
            if h in hashes:
                duplicates.append((path, h))
            else:
                hashes[h] = path

        if not duplicates:
            continue

        total_duplicates_found += len(duplicates)
        print(f"\n[REPAIR] Article: '{slug}' — {len(duplicates)} duplicate(s) found")

        # Replace duplicates with different Unsplash stock photos
        slug_offset = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)

        for dup_path, dup_hash in duplicates:
            replaced = False
            for attempt in range(len(UNSPLASH_CURATED_STOCKS)):
                candidate_idx = (slug_offset + len(UNSPLASH_CURATED_STOCKS) // 2 + attempt) % len(UNSPLASH_CURATED_STOCKS)
                if candidate_idx in global_used_stock_indices:
                    continue  # Try next one for maximum variety

                stock_url = UNSPLASH_CURATED_STOCKS[candidate_idx]
                try:
                    res = requests.get(stock_url, timeout=15)
                    if res.status_code == 200 and len(res.content) > 30000:
                        new_hash = hashlib.md5(res.content).hexdigest()
                        if new_hash not in hashes:
                            with open(dup_path, "wb") as f:
                                f.write(res.content)
                            hashes[new_hash] = dup_path
                            global_used_stock_indices.add(candidate_idx)
                            total_replacements += 1
                            print(f"  [OK] REPLACED: {os.path.basename(dup_path)} -> stock #{candidate_idx} ({len(res.content)//1024} KB)")
                            replaced = True
                            break
                except Exception as e:
                    print(f"  [WARN] Failed stock #{candidate_idx}: {e}")

            if not replaced:
                print(f"  [FAIL] Could not replace: {os.path.basename(dup_path)} (all stocks exhausted)")

    print("\n" + "=" * 60)
    print(f"[REPAIR] COMPLETED")
    print(f"  Articles scanned:    {total_articles}")
    print(f"  Duplicates found:    {total_duplicates_found}")
    print(f"  Replacements made:   {total_replacements}")
    print(f"  Remaining issues:    {total_duplicates_found - total_replacements}")
    print("=" * 60)


if __name__ == "__main__":
    repair_duplicates()

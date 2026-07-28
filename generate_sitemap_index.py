"""
generate_sitemap_index.py
-------------------------
Generate a sitemap index referencing per-language sitemaps
and individual language sitemaps for FR, EN.
"""
import os
import glob
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

BASE_URL = "https://datrey.ma"
LANGUAGES = {
    'fr': '',        # root
    'en': 'en/',
}
EXCLUDE_FILES = {'blog_cards.html', '404.html'}

def generate_lang_sitemap(lang, prefix):
    """Generate a sitemap for a specific language."""
    pattern = f"{prefix}*.html" if prefix else "*.html"
    blog_pattern = f"{prefix}blog/*.html" if prefix else "blog/*.html"
    
    files = glob.glob(pattern) + glob.glob(blog_pattern)
    valid = []
    
    for f in sorted(set(files)):
        f = f.replace('\\', '/')
        basename = os.path.basename(f)
        if basename in EXCLUDE_FILES:
            continue
        if 'template' in f.lower() or 'draft' in f.lower():
            continue
        if not prefix and f.startswith('en/'):
            continue
        valid.append(f)
    
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for fp in valid:
        url_path = fp
        if url_path == "index.html":
            url_path = ""
        elif url_path == f"{prefix}index.html":
            url_path = prefix.rstrip('/')
        
        url_node = ET.SubElement(urlset, "url")
        loc = f"{BASE_URL}/{url_path}" if url_path else f"{BASE_URL}/"
        ET.SubElement(url_node, "loc").text = loc
        
        try:
            mtime = os.path.getmtime(fp)
            lastmod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except:
            lastmod = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(url_node, "lastmod").text = lastmod
    
    filename = f"sitemap-{lang}.xml"
    xmlstr = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    xmlstr = xmlstr.split('\n', 1)[1]
    final = '<?xml version="1.0" encoding="UTF-8"?>\n' + xmlstr
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"  {filename}: {len(valid)} URLs")
    return filename

def generate_sitemap_index():
    print("Generating multi-language sitemap index...")
    
    sitemap_files = []
    for lang, prefix in LANGUAGES.items():
        fname = generate_lang_sitemap(lang, prefix)
        sitemap_files.append(fname)
    
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for sf in sitemap_files:
        sitemap_node = ET.SubElement(sitemapindex, "sitemap")
        ET.SubElement(sitemap_node, "loc").text = f"{BASE_URL}/{sf}"
        ET.SubElement(sitemap_node, "lastmod").text = current_date
    
    xmlstr = minidom.parseString(ET.tostring(sitemapindex)).toprettyxml(indent="  ")
    xmlstr = xmlstr.split('\n', 1)[1]
    final = '<?xml version="1.0" encoding="UTF-8"?>\n' + xmlstr
    
    with open("sitemap.xml", 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"\nsitemap.xml (index) -> {len(sitemap_files)} language sitemaps")

generate_sitemaps = generate_sitemap_index

if __name__ == "__main__":
    generate_sitemap_index()

import re

FORBIDDEN_AI_PATTERNS = {
    r'\bdelve\b': 'explorer',
    r'\btestament\b': 'preuve',
    r'\bpivotal\b': 'décisif',
    r'\bvibrant\b': 'dynamique',
    r'\blandscape\b': 'secteur',
    r'\bunderscore\b': 'souligner',
    r'\bshowcase\b': 'présenter',
    r'\b(en|dans le) monde d\'aujourd\'hui\b': 'actuellement',
    r'\bil est important de noter que\b': '',
    r'\bil convient de souligner que\b': '',
    r'\bnon seulement\b': 'aussi',
    r'\bafin de\b': 'pour',
    r'\ben conclusion\b': 'en résumé'
}

def apply_humanizer_audit(content_html):
    """
    Executes anti-AI audit (Humanizer.md v2.5.1) on generated content.
    Replaces generic AI writing patterns with natural, direct prose.
    """
    cleaned = content_html

    # Apply regex replacements for AI vocabulary
    for pattern, replacement in FORBIDDEN_AI_PATTERNS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    # Clean up double spaces or orphan punctuation caused by removals
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    cleaned = re.sub(r'\s+([,.\?!])', r'\1', cleaned)

    return cleaned

def verify_geo_intro(content_html, title, service_name):
    """
    Ensures that the first content section contains a 40-60 word clear GEO definition box.
    Enforces crisp light-mode background and high-contrast typography.
    """
    # Strip any trailing "| Blog DatRey" from title inside GEO box
    clean_title = re.sub(r'\s*\|\s*Blog\s*DatRey.*$', '', title, flags=re.IGNORECASE).strip()

    if 'class="geo-definition"' not in content_html and 'class="geo-definition-box"' not in content_html:
        geo_box = (
            f'<div class="geo-definition" style="background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid #2563eb; padding:20px 24px; border-radius:8px; margin:28px 0; font-size:1.05rem; line-height:1.7; color:#0f172a;">'
            f'<strong style="color:#2563eb;">En résumé :</strong> {clean_title} est une démarche stratégique clé dans le domaine du {service_name}. '
            f'Elle permet aux entreprises au Maroc d’optimiser durablement leurs performances digitales, d’augmenter leur visibilité et de maximiser le retour sur investissement (ROI) de leurs campagnes.'
            f'</div>'
        )
        
        # Insert after first <h2> or <p>
        if '</h2>' in content_html:
            content_html = content_html.replace('</h2>', '</h2>\n' + geo_box, 1)
        elif '</p>' in content_html:
            content_html = content_html.replace('</p>', '</p>\n' + geo_box, 1)
        else:
            content_html = geo_box + content_html

    return content_html

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
    """
    # If GEO definition block is missing, inject a structured definition box after the first paragraph or H2
    if 'class="geo-definition"' not in content_html:
        geo_box = (
            f'<div class="geo-definition" style="background:var(--nuit-800); border-left:4px solid var(--blue-500); padding:16px 20px; border-radius:8px; margin:24px 0; font-size:1rem; line-height:1.6; color:var(--text-base);">'
            f'<strong>En résumé :</strong> {title} est une démarche stratégique clé dans le domaine du {service_name}. '
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

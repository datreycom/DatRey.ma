import json
import requests
import re
import random
from autopilot.config import DEEPSEEK_API_KEY, POLLINATIONS_API_KEY, SERVICES

HIGH_INTENT_TOPIC_ANGLES = [
    "Guide ultime d'acquisition client à fort ROI pour PME et grandes entreprises",
    "Erreurs coûteuses à éviter absolument et solutions concrètes pour maximiser les conversions",
    "Étude de cas et méthodologie étape par étape pour doubler son chiffre d'affaires",
    "Comparatif décisionnel et guide d'investissement budgétaire pour dirigeants",
    "Stratégies d'optimisation GEO et SEO pour être cité en #1 par Google AI et ChatGPT",
    "Plan d'action 90 jours pour dominer son marché au Maroc et à l'international"
]

def generate_article_content(service_slug=None, topic_hint=None):
    """
    Calls DeepSeek API / Pollinations API to generate an exhaustive, high-converting blog article (>= 1,300 words),
    specifically crafted to attract high-value B2B client leads for DatRey.
    """
    if not service_slug or service_slug not in SERVICES:
        service_slug = random.choice(list(SERVICES.keys()))
    
    service_name = SERVICES[service_slug]
    angle = random.choice(HIGH_INTENT_TOPIC_ANGLES)
    topic_str = f" axé sur '{topic_hint}'" if topic_hint else f" sous l'angle : '{angle}'"

    system_prompt = (
        "Tu es le Directeur Stratégique et Rédacteur en Chef de DatRey (datrey.ma), l'agence digitale leader au Maroc "
        "spécialisée en acquisition client, SEO/GEO, Google Ads et croissance rentable pour les entreprises.\n"
        "OBJECTIF MAJEUR : Attirer et convaincre des décideurs (PDG, Directeurs Marketing, Fondateurs d'entreprises) "
        "de faire appel aux services de l'agence DatRey.\n\n"
        "Règles impératives de rédaction :\n"
        "1. LONGUEUR ARTICLE : Le corps de l'article DOIT faire un MINIMUM STRICT de 1300 mots avec des analyses financières et ROI approfondies.\n"
        "2. GEO DEFINITION : Le premier paragraphe doit être une DÉFINITION SYNTHÉTIQUE ET DIRECTE de 40 à 60 mots définissant le sujet avec précision pour être citée immédiatement par Google AI Overviews, ChatGPT et Perplexity.\n"
        "3. RÉSUMÉ RÉSEAUX SOCIAUX (250-300 MOTS) : Rédige un résumé captivant et viral d'exactement 250 à 300 mots destiné aux réseaux sociaux (LinkedIn, Facebook, Instagram) conçu pour générer des clics et des demandes de devis.\n"
        "4. CONTEXTE BUSINESS & MAROC : Exemples concrets axés sur les PME/Multinationales au Maroc (Casablanca, Rabat, Tanger, Marrakech) et à l'international, avec métriques de ROI, budgets MAD/EUR, et KPIs d'acquisition.\n"
        "5. CONVERSION & CALL-TO-ACTION DATREY : Démontre subtilement l'expertise inégalée de l'agence DatRey et inclut des appels à l'action stratégiques invitant le lecteur à demander son Audit Digital Gratuit.\n"
        "6. ANTI-IA (HUMANIZER) : Style vif, percutant, humain, d'expert terrain. Pas de mots banals d'IA ('delve', 'testament', 'vibrant', 'crucial').\n"
        "7. IMAGES : 5 prompts visuels détaillés en anglais pour l'IA d'image (Pollinations Klein), STRICTEMENT SANS TEXTE DANS L'IMAGE."
    )

    user_prompt = f"""
    Génère un article de blog à très fort pouvoir de conversion client{topic_str} pour la catégorie : "{service_name}".

    Format de sortie attendu (JSON valide uniquement, sans aucun texte autour) :
    {{
      "title": "Titre percutant orienté ROI et SEO (H1)",
      "slug": "slug-optimise-conversion-seo",
      "description": "Meta description très incitative (140-155 caractères)",
      "category": "{service_name}",
      "social_summary": "Résumé de 250 à 300 mots ultra-captivant et structuré pour générer des leads sur les réseaux sociaux...",
      "content": "<h2>...</h2><p>...</p>...",
      "image_prompts": [
        "Prompt 1 (Hero Image)...",
        "Prompt 2 (Section 1)...",
        "Prompt 3 (Section 2)...",
        "Prompt 4 (Section 3)...",
        "Prompt 5 (Section 4)..."
      ]
    }}
    """

    targets = [
        {"url": "https://api.deepseek.com/v1/chat/completions", "model": "deepseek-chat", "keys": [DEEPSEEK_API_KEY]},
        {"url": "https://gen.pollinations.ai/v1/chat/completions", "model": "deepseek", "keys": [POLLINATIONS_API_KEY]},
        {"url": "https://gen.pollinations.ai/v1/chat/completions", "model": "openai", "keys": [POLLINATIONS_API_KEY]}
    ]

    session = requests.Session()

    for target in targets:
        for key in target["keys"]:
            if not key:
                continue
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": target["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }

            for attempt in range(2):
                try:
                    print(f"[DeepSeek Engine] Requesting high-converting article via {target['url']} (model: {target['model']}, attempt: {attempt+1})...")
                    res = session.post(target["url"], headers=headers, json=payload, timeout=90)
                    if res.status_code == 200:
                        result_json = res.json()
                        raw_text = result_json["choices"][0]["message"]["content"]

                        if raw_text.startswith("```"):
                            raw_text = re.sub(r'^```(json)?\n', '', raw_text)
                            raw_text = re.sub(r'\n```$', '', raw_text)

                        data = json.loads(raw_text.strip(), strict=False)
                        
                        prompts = data.get("image_prompts", [])
                        while len(prompts) < 5:
                            prompts.append(f"Professional corporate digital marketing visualization of {service_name}, photorealistic, 8k resolution, cinematic lighting, no text")
                        data["image_prompts"] = prompts[:5]

                        word_count = len(re.findall(r'\w+', data.get("content", "")))
                        print(f"[DeepSeek Engine] High-converting article generated! Title: '{data.get('title')}' | Words: ~{word_count}")
                        return data
                    elif res.status_code in (401, 402):
                        break
                    else:
                        print(f"[DeepSeek Engine] Status {res.status_code} on {target['url']}: {res.text[:100]}")
                except Exception as e:
                    print(f"[DeepSeek Engine] Exception on {target['url']}: {e}")

    raise RuntimeError("Failed to generate article: All API targets and keys exhausted.")

import json
import requests
import re
from autopilot.config import DEEPSEEK_API_KEY, POLLINATIONS_API_KEY, SERVICES

def generate_article_content(service_slug=None, topic_hint=None):
    """
    Calls DeepSeek API / Pollinations API to generate an exhaustive, high-quality blog article (>= 1,300 words),
    plus a rich 250-300 word executive summary tailored for high-reach social media posts.
    """
    if not service_slug or service_slug not in SERVICES:
        service_slug = "google-ads"
    
    service_name = SERVICES[service_slug]
    topic_str = f" axé sur '{topic_hint}'" if topic_hint else ""

    system_prompt = (
        "Tu es un expert mondial en Marketing Digital, SEO, GEO (Generative Engine Optimization) "
        "et rédacteur principal pour l'agence digitale marocaine DatRey (datrey.ma).\n"
        "Règles impératives de rédaction :\n"
        "1. LONGUEUR ARTICLE : Le corps de l'article DOIT faire un MINIMUM STRICT de 1300 mots.\n"
        "2. GEO DEFINITION : Le premier paragraphe de l'article doit être une DÉFINITION SYNTHÉTIQUE ET DIRECTE de 40 à 60 mots définissant précisément le sujet principal.\n"
        "3. RÉSUMÉ RÉSEAUX SOCIAUX (250-300 MOTS) : Rédige un résumé captivant et viral d'exactement 250 à 300 mots destiné aux réseaux sociaux (LinkedIn, Facebook, Instagram). Ce résumé doit contenir une accroche percutante, 4 à 5 points clés à forte valeur ajoutée, des conseils pratiques pour le marché marocain/international, et un appel à l'action stratégique.\n"
        "4. CONTEXTE MAROC : Intègre naturellement le contexte des entreprises au Maroc (Casablanca, Rabat, e-commerce local, PME, devises MAD, ROI).\n"
        "5. ANTI-IA (HUMANIZER) : Évite le jargon d'IA (pas de 'delve', 'testament', 'pivotal', 'crucial', 'vibrant'). Adopte un ton d'expert vif, pragmatique et humain.\n"
        "6. IMAGES : Fournis 5 prompts visuels détaillés en anglais pour l'IA d'image (Pollinations Klein). Sans aucun texte dans les visuels."
    )

    user_prompt = f"""
    Génère un article de blog complet{topic_str} pour la catégorie : "{service_name}".

    Format de sortie attendu (JSON valide uniquement, sans aucun texte autour) :
    {{
      "title": "Titre accrocheur et optimisé SEO (H1)",
      "slug": "slug-optimise-seo",
      "description": "Meta description persuasive (140-155 caractères)",
      "category": "{service_name}",
      "social_summary": "Résumé de 250 à 300 mots ultra-captivant et structuré pour les réseaux sociaux...",
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
                    print(f"[DeepSeek Engine] Requesting article via {target['url']} (model: {target['model']}, attempt: {attempt+1})...")
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
                        print(f"[DeepSeek Engine] Article generated! Title: '{data.get('title')}' | Words: ~{word_count}")
                        return data
                    elif res.status_code in (401, 402):
                        break
                    else:
                        print(f"[DeepSeek Engine] Status {res.status_code} on {target['url']}: {res.text[:100]}")
                except Exception as e:
                    print(f"[DeepSeek Engine] Exception on {target['url']}: {e}")

    raise RuntimeError("Failed to generate article: All API targets and keys exhausted.")

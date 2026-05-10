# Architecture du Site - DatRey.ma

Ce document détaille la structure des URLs générée dans le fichier `sitemap.xml` conformément aux bonnes pratiques SEO.

## Résumé de l'Architecture
- **Total URLs** : 55 pages actives indexables
- **Structure** :
  - `https://datrey.ma/` (Racine) : Pages de services principales, contact, légal
  - `https://datrey.ma/blog/` (Dossier Blog) : Index du blog et 33+ articles de contenu

## Qualité du Sitemap
- **Format** : XML valide sitemaps.org/0.9
- **Tags dépréciés** : `<priority>` et `<changefreq>` ont été retirés pour se conformer aux standards actuels de Google.
- **Mise à jour** : Le champ `<lastmod>` est dynamiquement calculé selon la dernière modification réelle du fichier sur le serveur.

## Structure Détaillée

### 1. Pages Principales (Piliers)
- `/` (Accueil)
- `/services` (Hub Services)
- `/services-google-ads`
- `/services-meta-ads`
- `/services-seo`
- `/services-cro`
- `/services-emailing`
- `/services-strategie`
- `/transformation-digitale`

### 2. Pages Institutionnelles
- `/a-propos`
- `/cas-clients`
- `/contact`
- `/mentions-legales`
- `/politique-confidentialite`

### 3. Contenu Éducatif (Blog)
- `/blog` (Index du blog)
- `/blog/` (Articles générés - 33 pages)
  - Ex: `/blog/roi-google-ads-maroc`
  - Ex: `/blog/agence-seo-casablanca`
  - *Tous les articles sont correctement listés avec des dates dynamiques.*

## Mises à jour futures
- Si des pages doivent être désindexées (ex: pages de remerciement, profils non pertinents), elles doivent être exclues du script `generate_sitemap.py`.
- Actuellement, le script ignore les templates, les drafts, et les traductions (comme demandé) pour concentrer le budget de crawl sur le site principal FR.

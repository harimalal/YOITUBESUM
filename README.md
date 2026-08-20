# 📺 YOITUBESUM — YouTube Magic Summarizer

Application Streamlit qui génère un résumé structuré (Titre, Sujet, Sommaire,
Développement, Key Takeaways) d'une vidéo YouTube à partir de sa transcription,
via l'API Gemini (Google).

## Fonctionnement

1. L'utilisateur colle un lien YouTube (ou un texte manuel en secours).
2. La transcription (FR puis EN) est récupérée via `youtube-transcript-api`.
3. Le texte est envoyé au modèle Gemini (`google-genai`) pour synthèse.
4. Le résumé est affiché dans l'interface.

## Prérequis

- Une clé API Gemini : https://aistudio.google.com/app/apikey
- Python 3.11+ **ou** Docker

## Lancer en local (sans Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configuration de la clé API (2 options)
cp .env.example .env   # puis éditez .env
# ou : mkdir -p .streamlit && cp .env.example .streamlit/secrets.toml (format TOML)

export GEMINI_KEY=your_key   # si vous utilisez .env, exportez-le ou utilisez python-dotenv
streamlit run app.py
```

L'application est accessible sur http://localhost:8501.

## Lancer avec Docker (recommandé pour un déploiement)

```bash
cp .env.example .env   # renseignez GEMINI_KEY
docker compose up --build
```

Ou sans docker-compose :

```bash
docker build -t yoitubesum .
docker run -p 8501:8501 -e GEMINI_KEY=your_key yoitubesum
```

## Tests et qualité

```bash
pip install -r requirements-dev.txt
ruff check .          # lint
pytest tests/ -v      # tests unitaires
```

La CI GitHub Actions (`.github/workflows/ci.yml`) exécute ces mêmes étapes
ainsi que le build de l'image Docker à chaque push.

## Déploiement

- **Streamlit Community Cloud** (gratuit) : connectez ce dépôt, renseignez
  `GEMINI_KEY` dans les *Secrets* de l'application (format TOML,
  `GEMINI_KEY = "..."`).
- **Conteneur (VM, PaaS, Kubernetes)** : utilisez l'image Docker fournie et
  injectez `GEMINI_KEY` / `GEMINI_MODEL` en variables d'environnement.

## Configuration

| Variable       | Description                          | Défaut              |
|----------------|---------------------------------------|----------------------|
| `GEMINI_KEY`   | Clé API Gemini (obligatoire)          | —                    |
| `GEMINI_MODEL` | Nom du modèle Gemini à utiliser       | `gemini-2.5-flash`   |

## Limites connues

- Fonctionne uniquement pour les vidéos disposant de sous-titres FR ou EN
  (sinon, utiliser le champ "Texte manuel").
- Pas de persistance des résumés générés (aucune base de données).

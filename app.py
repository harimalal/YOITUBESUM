import logging
import os
import re

import streamlit as st
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("yoitubesum")

st.set_page_config(page_title="IA Vidéo Summarizer", page_icon="📺")


def _get_config(key: str, default: str | None = None) -> str | None:
    """Lit une valeur de config depuis st.secrets (Streamlit Cloud) puis os.environ (Docker/local)."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)


# --- Configuration ---
API_KEY = _get_config("GEMINI_KEY")
MODEL_NAME = _get_config("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    st.error(
        "Clé API Gemini manquante. Définissez GEMINI_KEY dans `.streamlit/secrets.toml` "
        "ou dans une variable d'environnement (voir `.env.example`)."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)


def extract_id(url: str) -> str | None:
    """Extrait l'identifiant vidéo (11 caractères) d'une URL YouTube."""
    if not url:
        return None
    match = re.search(r"(?:v=|be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None


def fetch_text(v_id: str) -> str | None:
    """Récupère la transcription d'une vidéo YouTube (fr puis en)."""
    if not v_id:
        return None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=["fr", "en"])
        return " ".join(chunk["text"] for chunk in transcript)
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as exc:
        logger.info("Pas de transcription disponible pour %s : %s", v_id, exc)
        return None
    except Exception:
        logger.exception("Erreur inattendue lors de la récupération de la transcription %s", v_id)
        return None


st.title("📺 YouTube Magic Summarizer")
url = st.text_input("Lien YouTube :")
manual_text = st.text_area("Texte manuel (si besoin) :")

if st.button("Générer"):
    v_id = extract_id(url)
    txt = manual_text.strip() if manual_text and manual_text.strip() else fetch_text(v_id)

    if txt:
        if v_id:
            st.image(f"https://img.youtube.com/vi/{v_id}/0.jpg")
        with st.spinner("Rédaction..."):
            prompt = (
                "Fais une synthèse détaillée en français avec Titre, Sujet, Sommaire, "
                f"Développement et Key Takeaways de ce texte : {txt}"
            )
            try:
                res = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                st.markdown(res.text)
            except Exception:
                logger.exception("Erreur lors de l'appel au modèle Gemini")
                st.error("Erreur lors de la génération du résumé. Réessayez plus tard.")
    else:
        st.error("Aucun texte trouvé. Vérifiez le lien ou collez le texte manuellement.")

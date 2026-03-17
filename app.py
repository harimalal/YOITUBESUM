import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Configuration de la page
st.set_page_config(page_title="IA Vidéo Summarizer", page_icon="📺")

# Configuration de l'API Gemini
API_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=API_KEY)

# Initialisation du modèle (version simple)
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_text(v_id):
    try:
        t_list = YouTubeTranscriptApi.list_transcripts(v_id)
        transcript = t_list.find_transcript(['fr', 'en'])
        data = transcript.fetch()
        return " ".join([t['text'] for t in data])
    except:
        return None

# Interface
st.title("📺 YouTube Magic Summarizer")

url = st.text_input("1. Lien de la vidéo :")
manual_text = st.text_area("2. (Optionnel) Colle le texte ici :", height=150)

if st.button("Générer la synthèse"):
    video_id = extract_id(url) if url else "default"
    text_content = None

    if manual_text:
        text_content = manual_text
    elif url:
        with st.spinner("Récupération du texte..."):
            text_content = fetch_text(video_id)
    
    if text_content:
        with st.spinner("L'IA réfléchit..."):
            try:
                prompt = f"Fais une synthèse structurée en français de ce texte. Inclus le titre, le sujet, un sommaire, un développement détaillé avec exemples et citations, et les points clés à retenir. Voici le texte : {text_content}"
                # Ajout de la vignette manuellement dans le markdown
                st.markdown(f"![Vignette](https://img.youtube.com/vi/{video_id}/0.jpg)")
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erreur IA : {str(e)}")
    else:
        st.error("Impossible de récupérer le texte automatiquement.")
        st.info("💡 Utilise la case 'Optionnel' en copiant la transcription depuis l'app YouTube.")
        

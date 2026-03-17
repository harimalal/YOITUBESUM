import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="IA Vidéo Summarizer", page_icon="📺")

# Configure ton API Key ici
# (Astuce : en production, utilise st.secrets)
API_KEY = "TA_CLE_API_GEMINI_ICI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- FONCTIONS UTILES ---
def extract_video_id(url):
    """Extrait l'ID de la vidéo d'une URL YouTube."""
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    """Récupère le texte de la vidéo."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en'])
        return " ".join([t['text'] for t in transcript_list])
    except Exception as e:
        return None

def generate_ai_summary(transcript, video_id):
    """Envoie le texte à Gemini pour la synthèse formatée."""
    prompt = f"""
    Tu es un expert en analyse de contenu. À partir de la transcription suivante, crée une synthèse riche et structurée.
    
    TRANSCRIPTION : {transcript}
    
    FORMAT ATTENDU :
    1. # Titre de la vidéo (trouve un titre percutant)
    2. ![Vignette](https://img.youtube.com/vi/{video_id}/0.jpg)
    3. ## Sujet : (Un résumé global de l'intention)
    4. ## Sommaire : (Liste à puces des grands thèmes)
    5. ## Développement : (Développe chaque point du sommaire avec des détails, des exemples et des citations marquantes du texte)
    6. ## Key Takeaways : (Les points essentiels à retenir)
    
    Réponds en français, avec un ton pro et inspirant.
    """
    response = model.generate_content(prompt)
    return response.text

# --- INTERFACE STREAMLIT ---
st.title("📺 Synthétiseur de Vidéos YouTube")
st.write("Collez un lien pour obtenir une synthèse complète avec structure, citations et vignette.")

url = st.text_input("Lien YouTube :", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Générer la synthèse"):
    if not url:
        st.warning("Veuillez entrer une URL.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("URL YouTube invalide.")
        else:
            with st.spinner("L'IA analyse la vidéo (récupération du texte et rédaction)..."):
                # Étape 1 : Récupérer le texte
                text = get_transcript(video_id)
                
                if text:
                    # Étape 2 : Envoyer à l'IA
                    summary = generate_ai_summary(text, video_id)
                    st.markdown("---")
                    st.markdown(summary)
                else:
                    st.error("Impossible de récupérer les sous-titres de cette vidéo (ils sont peut-être désactivés).")


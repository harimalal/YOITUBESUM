import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="IA Vidéo Summarizer", page_icon="📺")

# Config API
API_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        # On essaie de récupérer n'importe quel sous-titre dispo (fr ou en)
        t_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = t_list.find_transcript(['fr', 'en'])
        data = transcript.fetch()
        return " ".join([t['text'] for t in data])
    except:
        return None

st.title("📺 YouTube Magic Summarizer")

# --- INTERFACE ---
url = st.text_input("1. Lien de la vidéo :")
manual_text = st.text_area("2. (Optionnel) Colle le texte ici si l'automatique échoue :", height=150)

if st.button("Générer la synthèse"):
    video_id = extract_video_id(url) if url else "default"
    text_to_analyze = None

    # Priorité au texte manuel, sinon automatique
    if manual_text:
        text_to_analyze = manual_text
    elif url:
        with st.spinner("Tentative de récupération automatique..."):
            text_to_analyze = get_transcript(video_id)
    
    if text_to_analyze:
        with st.spinner("L'IA rédige votre synthèse..."):
            prompt = f"""
            Transcription : {text_to_analyze}
            Fais une synthèse structurée en français :
            1. Titre percutant
            2. ![Vignette](https://img.youtube.com/vi/{video_id}/0.jpg)
            3. Sujet (résumé global)
            4. Sommaire (points clés)
            5. Développement détaillé (avec exemples et citations du texte)
            6. Key Takeaways
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)
    else:
        st.error("Désolé, YouTube bloque la récupération automatique sur ce serveur.")
        st.info("💡 ASTUCE : Ouvre la vidéo sur ton tel, va dans 'Description' > 'Afficher la transcription', copie tout le texte et colle-le dans la case 'Optionnel' ci-dessus !")
        

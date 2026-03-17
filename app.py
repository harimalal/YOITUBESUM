import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="IA Vidéo Summarizer", page_icon="📺")

# API
API_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=API_KEY)

# MODELE STABLE
model = genai.GenerativeModel('gemini-pro')

def extract_id(url):
    match = re.search(r'(?:v=|be/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

def fetch_text(v_id):
    try:
        t = YouTubeTranscriptApi.get_transcript(v_id, languages=['fr', 'en'])
        return " ".join([i['text'] for i in t])
    except:
        return None

st.title("📺 YouTube Magic Summarizer")
url = st.text_input("Lien YouTube :")
manual_text = st.text_area("Texte manuel (si besoin) :")

if st.button("Générer"):
    v_id = extract_id(url)
    txt = manual_text if manual_text else fetch_text(v_id)
    
    if txt:
        st.image(f"https://img.youtube.com/vi/{v_id}/0.jpg")
        with st.spinner("Rédaction..."):
            prompt = f"Fais une synthèse détaillée en français avec Titre, Sujet, Sommaire, Développement et Key Takeaways de ce texte : {txt}"
            res = model.generate_content(prompt)
            st.markdown(res.text)
    else:
        st.error("Aucun texte trouvé.")
        

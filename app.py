import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os
import uuid

# Streamlit page setup
st.set_page_config(page_title="🌎 Language Translator", page_icon="🔤", layout="wide")
st.title("🌍 Language Translator App")
st.markdown("Translate text, listen to translations, or input text using your voice 🎤.")

translator = Translator()
lang_list = list(LANGUAGES.values())

# Sidebar settings
st.sidebar.header("Translation Settings")
src_lang = st.sidebar.selectbox("Select source language", lang_list, index=21)  # English default
dest_lang = st.sidebar.selectbox("Select target language", lang_list, index=37)  # Hindi default

# Main input
st.subheader("📝 Enter Text")
input_text = st.text_area("Type here...", height=200)

# Buttons
col1, col2, col3 = st.columns(3)

# Translate Function
def translate_text(input_text, src, dest):
    if input_text.strip() == "":
        return ""
    try:
        src_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(src.lower())]
        dest_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest.lower())]
        translated = translator.translate(input_text, src=src_code, dest=dest_code)
        return translated.text
    except Exception as e:
        st.error(f"Translation Error: {str(e)}")
        return ""

# Text-to-Speech
def speak_text(text, lang):
    try:
        lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang.lower())]
        tts = gTTS(text=text, lang=lang_code)
        filename = f"{uuid.uuid4()}.mp3"
        tts.save(filename)
        st.audio(filename, format="audio/mp3")
        os.remove(filename)
    except Exception as e:
        st.error(f"Speech Error: {str(e)}")

# Voice Input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            st.error(f"Voice Error: {str(e)}")
            return ""

# Button actions
if col1.button("🔁 Translate"):
    translated_text = translate_text(input_text, src_lang, dest_lang)
    if translated_text:
        st.success("Translation successful!")
        st.subheader("🗣️ Translated Text:")
        st.write(translated_text)
        st.session_state.translated_text = translated_text

if col2.button("🎤 Voice Input"):
    voice_text = voice_input()
    if voice_text:
        st.success("Captured voice input!")
        st.text_area("Captured Text:", voice_text, height=150, key="voice_text")

if col3.button("🔊 Speak Translation"):
    if "translated_text" in st.session_state:
        speak_text(st.session_state.translated_text, dest_lang)
    else:
        st.warning("Please translate text first before playing sound.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")



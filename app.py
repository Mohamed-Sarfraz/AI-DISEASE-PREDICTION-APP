import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import uuid
import os
import speech_recognition as sr

# Set Page Config
st.set_page_config(page_title="The Ultimate Translator App", page_icon="🌍", layout="centered")

# Theme toggle
theme = st.sidebar.radio("Select Theme", ["🌙 Dark Mode", "☀️ Light Mode"])

# Apply Theme
if theme == "🌙 Dark Mode":
    text_bg_color = "#21262d"
    text_font_color = "#58a6ff"
    st.markdown("""
        <style>
        body { background-color: #0d1117; color: #c9d1d9; }
        .title { color: #58a6ff; text-align: center; font-size: 48px; }
        .subtitle { text-align: center; font-size: 20px; color: #8b949e; }
        .card { background-color: #161b22; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 6px rgba(0,0,0,0.5); margin-bottom: 20px; }
        .stTextArea textarea { background-color: #21262d; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    text_bg_color = "#e1e8f0"
    text_font_color = "#1f77b4"
    st.markdown("""
        <style>
        body { background-color: #f0f2f6; color: #333333; }
        .title { color: #1f77b4; text-align: center; font-size: 48px; }
        .subtitle { text-align: center; font-size: 20px; color: #555555; }
        .card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); margin-bottom: 20px; }
        .stTextArea textarea { background-color: #e1e8f0; color: #000000; }
        </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown('<div class="title">The Ultimate Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type ✏️ or Speak 🎤 and Translate!</div>', unsafe_allow_html=True)
st.write("---")

# About This App Section
with st.expander("ℹ️ About This App"):
    st.markdown("""
    **The Ultimate Translator App** is a multilingual translation tool designed to help you translate text or speech into any language you want! 🚀
    
    ### Features:
    - **Text Input**: Type or paste your text to translate instantly.
    - **Voice Input**: Speak into the microphone, and the app will recognize your speech and translate it.
    - **Auto-Detect Source Language**: The app can automatically detect the language of the text you input.
    - **Text-to-Speech**: Listen to the translated text in the target language using Text-to-Speech (TTS).
    - **Language Options**: Choose from a wide variety of languages for both input and output.
    - **Search History**: Your previous translations will be saved for quick access.
    
    ### How It Works:
    1. Choose the source and target languages.
    2. Enter text or speak into the microphone.
    3. Press "Translate Now" to get the translation.
    4. Optionally, listen to the translation via Text-to-Speech.
    5. View your previous translations in the "Search History".
    
    **Made with 💙 by Mohamed Sarfraz**.
    """)
st.write("---")

# Translator instance
translator = Translator()

# Sidebar Options
with st.sidebar:
    st.title("⚙️ Settings")
    detect_lang = st.checkbox("Auto-Detect Source Language", value=False)
    source_lang = st.selectbox("Source Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index('english'))
    dest_lang = st.selectbox("Target Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index('spanish'))
    if st.button("🔄 Swap Languages"):
        source_lang, dest_lang = dest_lang, source_lang
    voice_language = st.selectbox("🎤 Voice Input Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index('english'))
    mic_timeout = st.slider("🎙️ Microphone Listening Timeout (secs)", 2, 10, 5)

# Initialize or Load Search History
if "history" not in st.session_state:
    st.session_state["history"] = []

# Text Input Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("📝 Text Input")

input_text = st.text_area("Type or paste your text here...", height=150)

col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Clear Text"):
        input_text = ""
with col2:
    translate_now = st.button("🚀 Translate Now")

st.markdown('</div>', unsafe_allow_html=True)

# Voice Input Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("🎤 Voice Input")

if st.button("🎙️ Speak Now"):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... 🎧")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=mic_timeout)
            recognized_text = r.recognize_google(audio, language=list(LANGUAGES.keys())[list(LANGUAGES.values()).index(voice_language.lower())])
            st.success("Recognized Speech:")
            st.write(recognized_text)
            input_text = recognized_text
    except sr.WaitTimeoutError:
        st.error("Listening timed out. Try again.")
    except sr.UnknownValueError:
        st.error("Could not understand audio.")
    except OSError:
        st.error("No microphone detected. Please use text input.")
    except Exception as e:
        st.error(f"Voice Input Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Translation logic
if translate_now:
    if input_text.strip() == "":
        st.warning("Please enter or speak some text first.")
    else:
        try:
            with st.spinner('Translating...'):
                if detect_lang:
                    detected = translator.detect(input_text)
                    src_key = detected.lang
                    st.success(f"🔍 Detected Source Language: {LANGUAGES.get(src_key, 'Unknown').title()}")
                else:
                    src_key = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_lang.lower())]
                
                dest_key = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest_lang.lower())]
                translated = translator.translate(input_text, src=src_key, dest=dest_key)

                st.success(f"✅ Translated Text ({dest_lang.title()}):")
                st.markdown(
                    f"<div style='padding:10px; background-color:{text_bg_color}; border-radius:10px; color:{text_font_color};'>{translated.text}</div>",
                    unsafe_allow_html=True
                )
                st.session_state['translated_text'] = translated.text

                # Save translation to history
                st.session_state.history.append({
                    "source_text": input_text,
                    "translated_text": translated.text,
                    "source_lang": source_lang,
                    "dest_lang": dest_lang
                })
        except Exception as e:
            st.error(f"Translation Error: {e}")

# Text-to-Speech Section
def generate_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        filename = f"{uuid.uuid4()}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        return None

st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("🔊 Text to Speech")

if st.button("🎧 Listen to Translation"):
    translated_text = st.session_state.get('translated_text', None)
    if translated_text:
        try:
            dest_key = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest_lang.lower())]
            audio_file = generate_audio(translated_text, dest_key)
            if audio_file:
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                os.remove(audio_file)
            else:
                st.error("Failed to generate audio.")
        except Exception as e:
            st.error(f"Speech Error: {e}")
    else:
        st.warning("Please translate first!")

# Download Button for Translation
if 'translated_text' in st.session_state:
    st.download_button("⬇️ Download Translation", st.session_state['translated_text'], file_name="translation.txt")

st.markdown('</div>', unsafe_allow_html=True)

# Footer with Copyright Notice
st.write("---")
st.markdown("<center><small>© 2025 The Ultimate Translator | Copyrights All Rights Reserved</small></center>", unsafe_allow_html=True)


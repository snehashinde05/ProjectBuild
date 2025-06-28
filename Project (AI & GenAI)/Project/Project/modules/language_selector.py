# modules/language_selector.py

import streamlit as st
from deep_translator import GoogleTranslator

# Language options
LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te"
}

def language_selector():
    """
    Show dropdown to select language. Returns selected language code and name.
    """
    selected_language = st.selectbox("🌐 Select your preferred language:", list(LANGUAGE_MAP.keys()))
    return LANGUAGE_MAP[selected_language], selected_language

def translate_summary(summary_text, target_lang_code):
    """
    Translate summary text using Deep Translator to the target language.
    """
    if target_lang_code == "en":
        return summary_text

    try:
        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(summary_text)
        return translated
    except Exception as e:
        return f"⚠️ Translation Error: {str(e)}"

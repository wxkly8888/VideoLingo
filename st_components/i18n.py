import pandas as pd
import streamlit as st
import locale
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_locales():
    return pd.read_csv("st_components/locales.csv")

def get_localized_string(key):
    import config
    locale = config.DISPLAY_LANGUAGE
    locales = load_locales()
    try:
        return locales[(locales["locale"] == locale) & (locales["key"] == key)]["value"].iloc[0]
    except IndexError:
        # Unable to find localized string. Print error message with language and key
        print(f"Unable to find localized string. Language: {locale}, Key: {key}")
        return f"Missing: {key}"  # Return a default value if localized string is not found

def get_system_language():
    # Get system default language
    system_lang = locale.getdefaultlocale()[0]
    
    # Map to i18n codes
    lang_map = {
        'zh_CN': 'zh_CN',  # Simplified Chinese
        'zh_TW': 'zh_CN',  # Traditional Chinese also mapped to Simplified Chinese
        'en_US': 'en_US',  # English
        'ja_JP': 'ja_JP',  # Japanese
    }
    
    # If system language is in the mapping, return corresponding i18n code
    # Otherwise return English as default
    return lang_map.get(system_lang, 'en_US')

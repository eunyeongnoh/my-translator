import streamlit as st
from deep_translator import GoogleTranslator

st.title("🌍 나만의 번역기")
st.write("영어 문장을 한국어로 자동 번역해드려요!")

text = st.text_input("영어 문장을 입력하세요:")

if text:
    translated = GoogleTranslator(source='auto', target='ko').translate(text)
    st.success(f"번역 결과: {translated}")


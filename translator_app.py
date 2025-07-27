import streamlit as st
from deep_translator import GoogleTranslator
import csv
import os

# 📂 CSV에서 글로서리 불러오기
GLOSSARY_FILE = "glossary.csv"

def load_glossary():
    glossary = {}
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    glossary[row[0]] = row[1]
    return glossary

def save_glossary(glossary):
    with open(GLOSSARY_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k, v in glossary.items():
            writer.writerow([k, v])

# 🧠 글로서리 불러오기
glossary = load_glossary()

st.title("📘 한일·일한 번역기 + 글로서리 관리")

# 🔤 번역 기능 (최상단)
text = st.text_input("번역할 문장을 입력하세요 (한→일 또는 일→한):")

if text:
    # glossary 우선 적용
    if text in glossary:
        translated = glossary[text]
    elif text in glossary.values():
        translated = list(glossary.keys())[list(glossary.values()).index(text)]
    else:
        translated = GoogleTranslator(source='auto', target='ja' if GoogleTranslator(source='auto', target='ko').translate(text) == text else 'ko').translate(text)
    st.success(f"번역 결과: {translated}")

# ✏️ 글로서리 추가 (토글로 감싸기)
with st.expander("✏️ 글로서리 단어 추가", expanded=False):
    new_kor = st.text_input("한글 단어")
    new_jp = st.text_input("일본어 뜻")
    if st.button("글로서리에 추가하기"):
        if new_kor and new_jp:
            glossary[new_kor] = new_jp
            save_glossary(glossary)
            st.success(f"추가됨: {new_kor} → {new_jp} / {new_jp} → {new_kor}")
            st.experimental_rerun()
        else:
            st.warning("두 항목 모두 입력해 주세요.")

# 🔍 글로서리 검색 + 표시 + 삭제 (토글)
with st.expander("📘 글로서리 보기 / 삭제", expanded=False):
    search_term = st.text_input("검색어를 입력하세요 (한글 또는 일본어):").strip()
    filtered_glossary = {
        kor: jp for kor, jp in glossary.items()
        if search_term in kor or search_term in jp
    } if search_term else glossary

    if filtered_glossary:
        st.write("한→일:")
        for kor, jp in list(filtered_glossary.items()):
            col1, col2, col3 = st.columns([4, 4, 2])
            with col1:
                st.write(f"{kor} → {jp}")
            with col3:
                if st.button("삭제", key=f"del_{kor}"):
                    del glossary[kor]
                    save_glossary(glossary)
                    st.experimental_rerun()

        st.markdown("---")
        st.write("일→한:")
        for kor, jp in list(filtered_glossary.items()):
            st.write(f"{jp} → {kor}")
    else:
        st.info("일치하는 항목이 없습니다.")

import streamlit as st
from deep_translator import GoogleTranslator
import csv
import os

st.title("📘 한일·일한 번역 + 양방향 글로서리")
st.write("자주 쓰는 용어를 글로서리에 추가하고, 양방향으로 번역해보세요!")

GLOSSARY_FILE = "glossary.csv"

# 📂 CSV에서 글로서리 불러오기
def load_glossary():
    glossary = {}
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    glossary[row[0]] = row[1]
    return glossary

# 💾 글로서리 CSV에 저장
def save_glossary(glossary):
    with open(GLOSSARY_FILE, mode="w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        for kor, jp in glossary.items():
            writer.writerow([kor, jp])

# 로딩
glossary = load_glossary()

# 🔍 글로서리 검색 필터
st.subheader("🔍 글로서리 검색")
search_term = st.text_input("검색어를 입력하세요 (한글 또는 일본어):").strip()

filtered_glossary = {
    kor: jp for kor, jp in glossary.items()
    if search_term in kor or search_term in jp
} if search_term else glossary

# 📝 글로서리 표시 (양방향)
if filtered_glossary:
    st.subheader("📝 글로서리")
    st.write("한→일:")
    for kor, jp in filtered_glossary.items():
        st.write(f"{kor} → {jp}")
    st.write("일→한:")
    for kor, jp in filtered_glossary.items():
        st.write(f"{jp} → {kor}")
else:
    st.info("일치하는 항목이 없습니다.")

# ✏️ 글로서리 추가
st.subheader("✏️ 새로운 단어 추가")
new_kor = st.text_input("한글 단어")
new_jp = st.text_input("일본어 뜻")

if st.button("글로서리에 추가하기"):
    if new_kor and new_jp:
        glossary[new_kor] = new_jp
        save_glossary(glossary)
        st.success(f"추가됨: {new_kor} → {new_jp} / {new_jp} → {new_kor}")
    else:
        st.warning("두 항목 모두 입력해 주세요.")

# 🗑️ 글로서리 삭제
st.subheader("🗑️ 단어 삭제")
if glossary:
    delete_target = st.selectbox("삭제할 단어를 선택하세요 (한글 기준):", list(glossary.keys()))
    if st.button("삭제"):
        deleted_value = glossary.pop(delete_target, None)
        save_glossary(glossary)
        if deleted_value:
            st.success(f"삭제됨: {delete_target} → {deleted_value}")
else:
    st.info("삭제할 항목이 없습니다.")

# 🌐 문장 번역
st.subheader("🌐 문장 번역")
text = st.text_input("번역할 문장을 입력하세요 (한→일 또는 일→한):")

if text:
    if text in glossary:
        translated = glossary[text]
    elif text in glossary.values():
        translated = list(glossary.keys())[list(glossary.values()).index(text)]
    else:
        translated = GoogleTranslator(
            source='auto',
            target='ja' if GoogleTranslator(source='auto', target='ko').translate(text) == text else 'ko'
        ).translate(text)
    st.success(f"번역 결과: {translated}")

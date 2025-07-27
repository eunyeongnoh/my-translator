  GNU nano 4.8    /home/eunyeong/translator_app.py              import streamlit as st
from deep_translator import GoogleTranslator
import csv
import os

st.title("📘 한일·일한 번역 + 양방향 글로서리")
st.write("자주 쓰는 용어를 글로서리에 추가하고, 양방향으로 번역>
GLOSSARY_FILE = "glossary.csv"

# 📂 CSV에서 글로서리 불러오기
def load_glossary():
    glossary = {}
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, mode="r", encoding="utf-8") as>            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    glossary[row[0]] = row[1]
    return glossary

# 💾 글로서리 CSV에 저장
def save_glossary(glossary):
    with open(GLOSSARY_FILE, mode="w", encoding="utf-8", newlin>        writer = csv.writer(f)
        for kor, jp in glossary.items():
            writer.writerow([kor, jp])

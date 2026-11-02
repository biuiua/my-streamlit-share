import streamlit as st
from supabase import create_client, Client
import re

BUCKET_NAME = "user-files"

# Проста функція для транслітерації українських літер в англійські
def transliterate(text: str) -> str:
    rules = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye',
        'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
        'Ю': 'Yu', 'Я': 'Ya'
    }
    trans_text = "".join(rules.get(c, c) for c in text)
    trans_text = re.sub(r'[^a-zA-Z0-9._-]', '_', trans_text)
    return trans_text

@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Config error")
    st.stop()

st.title("Download")
st.write("Ready.")

uploaded_file = st.file_uploader("Pick a file", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    safe_name = transliterate(uploaded_file.name)
    
    if st.button("Send->"):
        with st.spinner("Uploading..."):
            try:
                response = supabase.storage.from_(BUCKET_NAME).upload(
                    path=safe_name,
                    file=file_bytes,
                    file_options={"cache-control": "3600", "upsert": "true"}
                )
                st.success(f"File '{uploaded_file.name}' is successfully uploaded as '{safe_name}'!")
            except Exception as e:
                st.error(f"Error while uploading: {e}")

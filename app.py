import streamlit as st
from supabase import create_client, Client
import urllib.parse  # Модуль для безпечного кодування кирилиці

# Назва вашого бакету в Supabase
BUCKET_NAME = "user-files"

# Ініціалізація клієнта Supabase через секрети Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

try:
    # Ось тут створюється змінна supabase, яка раніше зникла
    supabase = init_supabase()
except Exception as e:
    st.error("Помилка конфігурації. Перевірте секрети в налаштуваннях Streamlit.")
    st.stop()

st.title("📁 Глобальне сховище файлів")
st.write("Завантажуйте файли будь-якого формату. Вони будуть надійно збережені в хмарі Supabase.")

# Компонент для вибору файлу
uploaded_file = st.file_uploader("Оберіть файл для завантаження", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # Безпечно кодуємо назву (захист від помилок з українськими літерами)
    file_name = urllib.parse.quote(uploaded_file.name)
    
    if st.button("🚀 Надіслати у сховище"):
        with st.spinner("Завантаження файлу на сервер..."):
            try:
                # Надсилаємо файл у бакет сховища Supabase
                response = supabase.storage.from_(BUCKET_NAME).upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"cache-control": "3600", "upsert": "true"}
                )
                st.success(f"🎉 Файл '{uploaded_file.name}' успішно завантажено в сховище!")
            except Exception as e:
                st.error(f"❌ Помилка при завантаженні: {e}")

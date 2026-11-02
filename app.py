import streamlit as st
from supabase import create_client, Client

# Назва вашого бакету в Supabase, який ви створили на Кроці 1
BUCKET_NAME = "user-files"

# Ініціалізація клієнта Supabase через секрети Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Помилка підключення до сховища. Перевірте секрети в налаштуваннях Streamlit.")
    st.stop()

st.title("📁 Глабальне сховище файлів")
st.write("Завантажуйте файли будь-якого формату. Вони будуть надійно збережені в хмарі.")

# file_uploader без обмеження по `type` приймає абсолютно будь-які формати
uploaded_file = st.file_uploader("Оберіть файл для завантаження", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    
    if st.button("🚀 Надіслати у сховище"):
        with st.spinner("Завантаження файлу на сервер..."):
            try:
                storage_client = supabase.storage
                response = storage_client.from_(BUCKET_NAME).upload(
                path=file_name,
                file=file_bytes,
                file_options={"cache-control": "3600", "upsert": "true"}
)
                st.success(f"🎉 Файл '{file_name}' успішно завантажено! Тепер він доступний в адмінці.")
            except Exception as e:
                st.error(f"❌ Помилка при завантаженні: {e}")

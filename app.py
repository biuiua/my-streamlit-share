import streamlit as st
from supabase import create_client, Client
from storage3 import SupabaseStorageClient  # Імпортуємо прямий клієнт для сховища

BUCKET_NAME = "user-files"

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    
    # Створюємо базовий клієнт Supabase
    client = create_client(url, key)
    
    # Створюємо ізольований клієнт для роботи зі сховищем (захист від помилки PGRST125)
    storage_url = f"{url.rstrip('/')}/storage/v1"
    headers = {
        "apiKey": key,
        "Authorization": f"Bearer {key}"
    }
    storage_client = SupabaseStorageClient(storage_url, headers)
    
    return storage_client

try:
    storage = init_supabase()
except Exception as e:
    st.error("Помилка конфігурації. Перевірте секрети в налаштуваннях Streamlit.")
    st.stop()

st.title("📁 Глобальне сховище файлів")
st.write("Завантажуйте файли будь-якого формату. Вони будуть надійно збережені в хмарі.")

uploaded_file = st.file_uploader("Оберіть файл для завантаження", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    
    if st.button("🚀 Надіслати у сховище"):
        with st.spinner("Завантаження файлу на сервер..."):
            try:
                # Використовуємо ізольоване підключення, яке б'є точно в Storage API
                response = storage.from_(BUCKET_NAME).upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"cache-control": "3600", "upsert": "true"}
                )
                st.success(f"🎉 Файл '{file_name}' успішно завантажено!")
            except Exception as e:
                st.error(f"❌ Помилка при завантаженні: {e}")

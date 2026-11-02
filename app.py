import streamlit as st
from supabase import create_client, Client

# Назва вашого бакету в Supabase (перевірте, щоб збігалося регістром букв)
BUCKET_NAME = "user-files"

@st.cache_resource
def init_supabase() -> Client:
    # Беремо чисті URL та KEY із секретів Streamlit
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Помилка конфігурації. Перевірте секрети в налаштуваннях Streamlit.")
    st.stop()

st.title("📁 Глобальне сховище файлів")
st.write("Завантажуйте файли будь-якого формату. Вони будуть надійно збережені в хмарі Supabase.")

uploaded_file = st.file_uploader("Оберіть файл для завантаження", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    
    if st.button("🚀 Надіслати у сховище"):
        with st.spinner("Завантаження файлу на сервер..."):
            try:
                # Офіційний та правильний шлях для нових версій бібліотеки:
                # Звертаємося до клієнта сховища (.storage), потім до бакету (.from_), потім завантажуємо (.upload)
                response = supabase.storage.from_(BUCKET_NAME).upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"cache-control": "3600", "upsert": "true"}
                )
                st.success(f"🎉 Файл '{file_name}' успішно завантажено в сховище Supabase!")
            except Exception as e:
                st.error(f"❌ Помилка при завантаженні: {e}")

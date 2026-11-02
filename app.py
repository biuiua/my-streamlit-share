import streamlit as st
from supabase import create_client, Client
import urllib.parse  # Імпортуємо модуль для безпечного кодування назв

# ... (ваш попередній код ініціалізації сховища залишається без змін) ...

uploaded_file = st.file_uploader("Оберіть файл для завантаження", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # БЕЗПЕЧНЕ КОДУВАННЯ: перетворює "про.txt" на "%D0%BF%D1%80.txt", що зрозуміло для Supabase
    file_name = urllib.parse.quote(uploaded_file.name)
    
    if st.button("🚀 Надіслати у сховище"):
        with st.spinner("Завантаження файлу на сервер..."):
            try:
                response = supabase.storage.from_(BUCKET_NAME).upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"cache-control": "3600", "upsert": "true"}
                )
                st.success(f"🎉 Файл '{uploaded_file.name}' успішно завантажено в сховище!")
            except Exception as e:
                st.error(f"❌ Помилка при завантаженні: {e}")

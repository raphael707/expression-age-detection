import streamlit as st
import time

# --- PRE-LOADING MODEL ---
# Ini adalah bagian penting untuk Vercel.
# Kita paksa deepface mengunduh dan memuat model SEKARANG
# (saat proses build/deploy), bukan saat pengguna pertama kali membuka web.
def pre_load_models():
    print("Mulai memuat model DeepFace (Age & Emotion)...")
    start_time = time.time()
    
    try:
        # Coba impor dan bangun model secara eksplisit
        from deepface import Age, Emotion
        
        print("Memuat model Umur...")
        Age.load_model()
        print("Model Umur dimuat.")
        
        print("Memuat model Emosi...")
        Emotion.load_model()
        print("Model Emosi dimuat.")
        
        # Tambahan: Lakukan deteksi 'dummy' untuk memastikan backend (tensorflow) siap
        from deepface import DeepFace
        import numpy as np
        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
        DeepFace.analyze(dummy_img, actions=['age', 'emotion'], enforce_detection=False)
        
        end_time = time.time()
        print(f"Semua model berhasil dimuat dalam {end_time - start_time:.2f} detik.")
    
    except Exception as e:
        print(f"Error saat pre-loading model: {e}")
        # Jangan hentikan aplikasi, tapi beri tahu di log
        pass

# Panggil fungsi pre-loading
pre_load_models()

# --- Sisa kode aplikasi Anda (tidak berubah) ---
# Impor modul-modul yang sudah kita pecah
import upload_mode
import webcam_mode

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Analisis Wajah", layout="wide", initial_sidebar_state="expanded")

st.title("Program Deteksi Wajah, Umur, dan Ekspresi 👨‍👩‍👧‍👦")
st.write("Pilih mode di sidebar: unggah gambar statis atau gunakan analisis webcam live.")

# --- Logika Utama / Pilihan Mode ---
with st.sidebar:
    st.header("Pilih Mode")
    app_mode = st.radio("Pilih mode aplikasi:", ["Unggah Gambar", "Live Webcam"])

# Panggil fungsi run() dari modul yang sesuai
if app_mode == "Unggah Gambar":
    upload_mode.run_upload_mode()
elif app_mode == "Live Webcam":
    webcam_mode.run_webcam_mode()

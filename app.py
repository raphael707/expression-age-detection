import streamlit as st
import time

# --- PRE-LOADING MODEL ---
# Ini adalah bagian penting untuk Vercel.
# Kita paksa deepface mengunduh dan memuat model SEKARANG
# (saat proses build/deploy), bukan saat pengguna pertama kali membuka web.

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

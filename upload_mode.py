import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import terjemahkan_ekspresi

# --- Fungsi untuk Mode Unggah Gambar ---

def proses_gambar(uploaded_image):
    from deepface import DeepFace
    """
    Membaca gambar yang diunggah, menjalankan analisis DeepFace, 
    dan menggambar hasilnya.
    """
    try:
        # 1. Baca gambar
        image = Image.open(uploaded_image).convert('RGB')
        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        st.image(image, caption="Gambar Asli", use_column_width=True)
        st.subheader("Hasil Analisis:")
        
        # 2. Jalankan Analisis DeepFace
        with st.spinner("Menganalisis wajah... Ini mungkin memerlukan waktu..."):
            try:
                results = DeepFace.analyze(
                    img_path=image_cv, 
                    actions=['age', 'emotion'],
                    enforce_detection=True
                )
                
                if isinstance(results, dict):
                    results_list = [results]
                elif isinstance(results, list):
                    results_list = results
                else:
                    st.error("Format hasil analisis tidak terduga.")
                    return

                st.success(f"Berhasil mendeteksi {len(results_list)} wajah!")
                image_result = image_cv.copy()

                # 3. Iterasi hasil dan gambar di gambar
                for i, face_info in enumerate(results_list):
                    region = face_info['region']
                    age = face_info['age']
                    dominant_emotion = face_info['dominant_emotion']
                    emotion_id = terjemahkan_ekspresi(dominant_emotion)
                    
                    x, y, w, h = region['x'], region['y'], region['w'], region['h']
                    cv2.rectangle(image_result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    st.markdown(f"---")
                    st.markdown(f"**Wajah {i + 1}:**")
                    st.write(f"- Perkiraan Umur: **{age} tahun**")
                    st.write(f"- Ekspresi Dominan: **{emotion_id}** ({dominant_emotion.capitalize()})")
                    
                    text_age = f"Umur: ~{age}"
                    text_emotion = f"Ekspresi: {emotion_id}"
                    text_y = y - 10 if y - 10 > 10 else y + h + 20
                    
                    cv2.putText(image_result, text_age, (x, text_y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
                    cv2.putText(image_result, text_age, (x, text_y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(image_result, text_emotion, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
                    cv2.putText(image_cv, text_emotion, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # Bug fix: seharusnya image_result

                # --- FIX KECIL ---
                # Saya menemukan bug kecil di kode sebelumnya saat menyalin. 
                # Baris terakhir di atas seharusnya menggambar di 'image_result', bukan 'image_cv'.
                # Karena kita memisahkan file, saya perbaiki di sini:
                cv2.putText(image_result, text_emotion, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # ------------------


                # 4. Tampilkan gambar hasil
                image_result_rgb = cv2.cvtColor(image_result, cv2.COLOR_BGR2RGB)
                st.image(image_result_rgb, caption="Gambar Hasil Analisis", use_column_width=True)

            except ValueError as e:
                if "Face could not be detected" in str(e):
                    st.error("Error: Tidak ada wajah yang dapat dideteksi di gambar ini.")
                else:
                    st.error(f"Terjadi error Value: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan yang tidak terduga saat analisis: {e}")

    except Exception as e:
        st.error(f"Gagal memuat gambar: {e}")

# --- Fungsi utama untuk menjalankan mode ini ---
def run_upload_mode():
    st.header("Analisis Gambar Unggahan")
    with st.sidebar:
        st.header("Unggah")
        uploaded_file = st.file_uploader("Pilih file gambar (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        proses_gambar(uploaded_file)
    else:
        st.info("Silakan unggah gambar melalui panel di sebelah kiri.")
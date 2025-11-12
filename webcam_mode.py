import streamlit as st
import cv2
from deepface import DeepFace
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
from utils import terjemahkan_ekspresi # Ambil dari utils

# --- Kelas untuk Prosesor Video Real-time ---

class FaceAnalyzerTransformer(VideoTransformerBase):
    def __init__(self):
        pass

    def recv(self, frame):
        # Konversi frame dari streamlit-webrtc (format av.VideoFrame) ke format OpenCV (BGR)
        image_cv = frame.to_ndarray(format="bgr24")
        
        try:
            # Jalankan analisis DeepFace
            results = DeepFace.analyze(
                img_path=image_cv, 
                actions=['age', 'emotion'],
                enforce_detection=False
            )
            
            if isinstance(results, dict):
                results_list = [results]
            elif isinstance(results, list):
                results_list = results
            else:
                results_list = []

            # Iterasi dan gambar HANYA jika 'region' (wajah) ditemukan
            for face_info in results_list:
                if 'region' in face_info:
                    region = face_info['region']
                    age = face_info.get('age', '?') 
                    dominant_emotion = face_info.get('dominant_emotion', 'N/A')
                    emotion_id = terjemahkan_ekspresi(dominant_emotion)
                    
                    x, y, w, h = region['x'], region['y'], region['w'], region['h']
                    
                    cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    text_age = f"Umur: ~{age}"
                    text_emotion = f"Ekspresi: {emotion_id}"
                    text_y = y - 10 if y - 10 > 10 else y + h + 20
                    
                    cv2.putText(image_cv, text_age, (x, text_y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
                    cv2.putText(image_cv, text_age, (x, text_y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(image_cv, text_emotion, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
                    cv2.putText(image_cv, text_emotion, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        except Exception as e:
            print(f"Error di transformer: {e}")

        # Konversi kembali frame (yang sudah dimodifikasi) ke av.VideoFrame
        return av.VideoFrame.from_ndarray(image_cv, format="bgr24")

# --- Fungsi utama untuk menjalankan mode ini ---
def run_webcam_mode():
    st.header("Analisis Live Webcam")
    st.write("Klik 'START' untuk memulai webcam Anda. Analisis akan berjalan secara real-time.")
    st.warning("Analisis real-time (DeepFace) membutuhkan komputasi berat dan mungkin akan terasa lambat/patah-patah, terutama saat pertama kali memuat model.")
    
    rtc_config = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    webrtc_streamer(
        key="live_analysis",
        video_transformer_factory=FaceAnalyzerTransformer,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        rtc_configuration=rtc_config
    )
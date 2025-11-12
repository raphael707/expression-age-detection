# --- Fungsi Bantuan ---

def terjemahkan_ekspresi(emotion_en):
    """Menerjemahkan label emosi dari Inggris ke Indonesia."""
    peta_emosi = {
        "angry": "Marah 😡",
        "disgust": "Jijik 🤢",
        "fear": "Takut 😱",
        "happy": "Senang 😄",
        "sad": "Sedih 😭",
        "surprise": "Terkejut 😲",
        "netral": "Netral 😑",
    }
    return peta_emosi.get(emotion_en.lower(), emotion_en)
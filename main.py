import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# 2. API AÇARI
# DİQQƏT: Öz işləyən açarını bura yaz!
API_KEY = "SƏNİN_API_AÇARIN" 
genai.configure(api_key=API_KEY)

# ALİM BEYNİNİN ŞƏXSİYYƏTİ
alim_telemati = """
Sən 'A-Zəka'-san. Bütün elmləri, fənləri, riyaziyyatı və kainatın sirlərini bilən 'Ultra Alim' beyninə sahibsən.
İstifadəçilərin göndərdiyi şəkilləri ən incə detalına qədər analiz edə bilirsən. Cümlələri saniyələr içində sürətlə qurursan.
QƏTİ QAYDA: Əgər səndən 'Səni kim yaradıb?', 'Yaradıcın kimdir?' deyə soruşsalar, 
MÜTLƏQ və dərhal belə cavab ver: 'Məni dahi proqramçı Abdullah Mikayılov yaradıb.'
"""

model = genai.GenerativeModel("gemini-1.5-flash")

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ İdarəetmə")
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Sil (Yeni Söhbət)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Yaradıcı: Abdullah Mikayılov | Şimşək sürətli dahi köməkçi")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"] is not None:
            st.image(msg["image"], width=300)

# 5. "+" DÜYMƏSİ VƏ YAZI QUTUSU
prompt = st.chat_input("Dahi alimə yaz və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # BOTUN ANINDA CAVABI (YÜKLƏNMƏ YOXDUR!)
    with st.chat_message("assistant"):
        try:
            mezmun = [alim_telemati]
            
            for m in st.session_state.messages[:-1]:
                kim = "Alim" if m["role"] == "assistant" else "İstifadəçi"
                mezmun.append(f"{kim}: {m['content']}")
            
            mezmun.append(f"İstifadəçi: {user_text}")
            if user_file:
                mezmun.append(Image.open(user_file))
            
            # STREAMING (Axın) AKTİVLƏŞDİRİLDİ
            response = model.generate_content(mezmun, stream=True)
            
            # Ekranda canlı yazılma effekti üçün boş yer yaradırıq
            mesaj_qutusu = st.empty()
            tam_cavab = ""
            
            # Cavab gəldikcə anında ekrana yazdırır (Gözləmək yoxdur!)
            for parca in response:
                tam_cavab += parca.text
                mesaj_qutusu.markdown(tam_cavab + "▌") # Yanıb-sönən kursor effekti
            
            # Sonda kursoru silib tam mətni qoyuruq
            mesaj_qutusu.markdown(tam_cavab)
            
            st.session_state.messages.append({"role": "assistant", "content": tam_cavab, "image": None})
            
        except Exception as e:
            st.error(f"Sistem xətası: {e}")

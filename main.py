import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka | Model Seçici", page_icon="🧠", layout="wide")

# 2. API AÇARI (Bura öz açarını daxil et)
API_KEY = "SƏNİN_API_AÇARIN" 
genai.configure(api_key=API_KEY)

# 3. SOL PANEL: BEYİN (MODEL) SEÇİCİ
with st.sidebar:
    st.title("⚙️ Beyin Ayarları")
    st.markdown("Əgər model xəta (404) versə, siyahıdan başqasını seç!")
    
    # Sənə bütün mümkün Google beyinlərini siyahı kimi verirəm
    secilen_beyin = st.selectbox(
        "Aktiv Beyni Seç:",
        [
            "gemini-pro",           # Ən köhnə və ən problemsiz model
            "gemini-1.0-pro",       # Bir az yenilənmiş baza
            "gemini-1.5-flash",     # Şimşək sürətli (Bizi yoran budur)
            "gemini-1.5-pro"        # Ən güclü ultra alim
        ]
    )
    
    st.markdown("---")
    if st.button("🗑️ Söhbəti Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. ƏSAS EKRAN
st.title(f"🧠 A-Zəka Ultra Alim")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Hazırkı beyin: {secilen_beyin}")

# Yaddaş Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# 5. YAZI QUTUSU (Şəkil dəstəkli)
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

    # BOTUN CAVABI
    with st.chat_message("assistant"):
        with st.spinner(f"{secilen_beyin} düşünür..."):
            try:
                # Köhnə modellər xəta verməsin deyə təlimatı birbaşa sualın içinə gizledirik
                gizli_telimat = """
                Sən A-Zəka adlı Ultra Alimsən. Səni Abdullah Mikayılov yaradıb. 
                Sualları mütləq addım-addım, ən dəqiq şəkildə izah et.
                
                İstifadəçinin sualı: 
                """
                
                # Mətn və Şəkli paketləyirik
                mezmun = [gizli_telimat + user_text]
                if user_file:
                    mezmun.append(Image.open(user_file))

                # Seçilən modeli işə salırıq
                model = genai.GenerativeModel(secilen_beyin)
                response = model.generate_content(mezmun)
                
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "image": None})

            except Exception as e:
                # Əgər 404 versə, istifadəçini başqa model seçməyə yönləndiririk
                st.error(f"❌ Bu açarın '{secilen_beyin}' modelinə icazəsi yoxdur (və ya şəkil dəstəkləmir).\n\nZƏHMƏT OLMASA SOL PANELDƏN BAŞQA BİR BEYİN SEÇİB YENİDƏN YOXLA!\n\nDetal: {e}")

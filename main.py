import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka | Model Seçici", page_icon="🧠", layout="wide")

# 2. API AÇARI (Bura öz açarını daxil et)
API_KEY = "SƏNİN_API_AÇARIN" 
genai.configure(api_key=API_KEY)

# 3. SOL PANEL: BEYİN SEÇİCİ
with st.sidebar:
    st.title("⚙️ Beyin Ayarları")
    st.markdown("Əgər model xəta versə və ya donsa, siyahıdan başqasını seç!")
    
    secilen_beyin = st.selectbox(
        "Aktiv Beyni Seç:",
        [
            "gemini-pro",           # Ən köhnə və dözümlü model
            "gemini-1.0-pro",       # Baza model
            "gemini-1.5-flash",     # Şimşək sürətli
            "gemini-1.5-pro"        # Ultra alim
        ]
    )
    
    st.markdown("---")
    if st.button("🗑️ Söhbəti Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Hazırkı beyin: {secilen_beyin}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# 5. YAZI QUTUSU
prompt = st.chat_input("Dahi alimə yaz və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # BOTUN CAVABI
    with st.chat_message("assistant"):
        with st.spinner(f"{secilen_beyin} düşünür..."):
            try:
                telimat = "Sən A-Zəka adlı Ultra Alimsən. Səni Abdullah Mikayılov yaradıb. Sualları mütləq addım-addım izah et. İstifadəçinin sualı: "
                
                mezmun = [telimat + user_text]
                if user_file:
                    mezmun.append(Image.open(user_file))

                model = genai.GenerativeModel(secilen_beyin)
                response = model.generate_content(mezmun)
                
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "image": None})

            except Exception as e:
                st.error(f"❌ XƏTA: Bu açarın '{secilen_beyin}' modelinə icazəsi yoxdur. Zəhmət olmasa sol paneldən başqa model seçib yenidən yoxla!\n\nDetal: {e}")

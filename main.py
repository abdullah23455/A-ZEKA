import streamlit as st
import requests

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Birbaşa", page_icon="⚡", layout="wide")

# 2. API AÇARI
# DİQQƏT: Öz işləyən AIza... açarını bura yazmağı unutma!
API_KEY = "SƏNİN_API_AÇARIN" 

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. ƏSAS EKRAN
st.title("⚡ A-Zəka (Birbaşa Bağlantı)")
st.caption("Yaradıcı: Abdullah Mikayılov | Donmayan Sistem")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. YAZI QUTUSU
prompt = st.chat_input("Dahi alimə yaz (məsələn: 2*9)...")

if prompt:
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # BOTUN BİRBAŞA CAVABI (REST API)
    with st.chat_message("assistant"):
        with st.spinner("Google serverinə birbaşa qoşulur..."):
            
            # Google-un birbaşa API ünvanı
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            # Göndəriləcək sual paketi
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            try:
                # Birbaşa sorğu göndəririk (Donma ehtimalı SIFIRDIR)
                cavab = requests.post(url, json=payload)
                
                # Əgər cavab 200 (Uğurlu) olarsa:
                if cavab.status_code == 200:
                    bot_mətni = cavab.json()['candidates'][0]['content']['parts'][0]['text']
                    st.write(bot_mətni)
                    st.session_state.messages.append({"role": "assistant", "content": bot_mətni})
                
                # Əgər Google açarı qəbul etməsə, əsl xətanı göstər:
                else:
                    st.error(f"❌ Google xəta qaytardı (Açarınızı yoxlayın!):\n\n{cavab.text}")
                    
            except Exception as e:
                st.error(f"İnternet bağlantısı xətası: {e}")

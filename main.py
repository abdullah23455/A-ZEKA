import streamlit as st
import google.generativeai as genai

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Avto-Beyin", page_icon="🤖", layout="wide")
st.title("🤖 A-Zəka (Avtomatik Beyin)")
st.caption("Yaradıcı: Abdullah Mikayılov | 404 Xətasına qarşı qorunan sistem")

# 2. API AÇARI
API_KEY = "SƏNİN_API_AÇARIN" # Bura öz açarını yazmağı unutma!
genai.configure(api_key=API_KEY)

# 3. AVTOMATİK MODEL AXTARIŞI (404 xətasının qarşısını alır)
@st.cache_resource
def icazeli_modeli_tap():
    try:
        # Açarın icazəsi olan bütün modelləri axtarırıq
        uygun_modeller = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                uygun_modeller.append(m.name)
        
        if uygun_modeller:
            # Tapılan ilk işlək modeli seçirik
            return genai.GenerativeModel(uygun_modeller[0])
        else:
            return None
    except Exception as e:
        return f"XƏTA: {e}"

model = icazeli_modeli_tap()

# 4. YADDAŞ VƏ İNTERFEYS
if "messages" not in st.session_state:
    st.session_state.messages = []

if isinstance(model, str):
    # Əgər API açarı tamamilə bloklanıbsa, əsl xətanı göstər
    st.error(f"API Açarınız Google tərəfindən rədd edildi. Zəhmət olmasa təzə açar alın. Detal: {model}")
elif model is None:
    st.warning("Bu açarın heç bir mətn modelinə icazəsi yoxdur.")
else:
    st.success(f"Sistem aktivdir! İstifade edilen beyin: {model.model_name}")
    
    # Köhnə mesajlar
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Sual Qutusu
    prompt = st.chat_input("Dahi sistemə sual ver...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analiz edilir..."):
                try:
                    # Seçilmiş işlək modelə sualı göndəririk
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Sual göndərilərkən xəta yarandı: {e}")

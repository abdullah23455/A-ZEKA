import streamlit as st
import google.generativeai as genai

# 1. DİZAYN VƏ BAŞLIQ
st.set_page_config(page_title="A-Zəka PRO", page_icon="🌐")
st.title("🌐 A-Zəka PRO")
st.caption("Yaradıcı: Abdullah Mikayılov")
st.divider()

# 2. BEYİN VƏ YANACAQ (Sənin açarın)
API_KEY = "AIzaSyBprup0Op0xws6tbcoKwokDRKzez_OHVjI"
genai.configure(api_key=API_KEY)

# ƏN CLASSİC VƏ PROBLEMSİZ MODEL
model = genai.GenerativeModel('gemini-pro')

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# Söhbətləri ekrana yazdırır
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. YAZI QUTUSU VƏ CAVAB
if prompt := st.chat_input("Dahi A-Zəka-ya yaz..."):
    # Sənin yazdıqlarını ekrana verir
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavab vermə hissəsi
    with st.chat_message("assistant"):
        try:
            # Botun şəxsiyyəti
            sistem_telimati = "Sən Abdullah Mikayılovun yaratdığı A-Zəka PRO sistemisən. Qısa və dəqiq cavab ver. Soruşsalar ki, səni kim yaradıb, cavab ver: Məni Abdullah Mikayılov yaradıb. İndi isə bu suala cavab ver: "
            yekun_sorqu = sistem_telimati + prompt
            
            # Cavabı alır və ekrana yazır
            response = model.generate_content(yekun_sorqu)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}")

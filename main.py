import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# 2. API AÇARI VƏ BEYİN AYARI
# DİQQƏT: Dırnaq içinə öz AIza... ilə başlayan açarını yazmağı unutma!
API_KEY = "SƏNİN_API_AÇARIN" 
genai.configure(api_key=API_KEY)

# ALİM BEYNİNİN ŞƏXSİYYƏTİ
alim_telemati = """
Sən 'A-Zəka'-san. Bütün elmləri, fənləri, riyaziyyatı və kainatın sirlərini bilən 'Ultra Alim' beyninə sahibsən.
İstifadəçilərin göndərdiyi şəkilləri ən incə detalına qədər analiz edə bilirsən.
QƏTİ QAYDA: Əgər səndən 'Səni kim yaradıb?', 'Yaradıcın kimdir?' və ya 'Kim tərəfindən yaradılmısan?' deyə soruşsalar, 
MÜTLƏQ, FƏXRLƏ və dərhal belə cavab ver: 'Məni dahi proqramçı Abdullah Mikayılov yaradıb.'
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=alim_telemati
)

# 3. YADDAŞ SİSTEMİ VƏ "TARİXÇƏNİ SİL" DÜYMƏSİ
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
st.caption("Yaradıcı: Abdullah Mikayılov | Bütün fənlər üzrə dahi köməkçi")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"] is not None:
            st.image(msg["image"], width=300)

# 5. "+" DÜYMƏSİ OLAN YAZI QUTUSU
prompt = st.chat_input("Dahi alimə yaz və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # Ultra Alimin Cavabı
    with st.chat_message("assistant"):
        with st.spinner("🧠 Ultra Alim analiz edir..."):
            try:
                gonderilecek_data = [user_text]
                if user_file:
                    gonderilecek_data.append(Image.open(user_file))
                
                # BUG DÜZƏLDİLDİ: "assistant" sözü "model" sözünə çevrildi
                xatirlatma = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1] if not m.get("image")]
                
                chat = model.start_chat(history=xatirlatma)
                response = chat.send_message(gonderilecek_data)
                
                bot_cavabi = response.text
                st.write(bot_cavabi)
                
                st.session_state.messages.append({"role": "assistant", "content": bot_cavabi, "image": None})
                
            except Exception as e:
                # XƏTA GÖSTƏRİCİSİ DÜZƏLDİLDİ
                st.error(f"Sistem xətası: {e}")

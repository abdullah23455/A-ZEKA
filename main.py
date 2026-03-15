import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. EKRAN DİZAYNI
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# 2. API AÇARI
# DİQQƏT: Öz işləyən API açarını dırnaq içinə yaz!
API_KEY = "SƏNİN_API_AÇARIN" 
genai.configure(api_key=API_KEY)

# 3. ULTRA ALİMİN QƏTİ QAYDALARI VƏ BEYNİ
alim_telemati = """
Sən 'A-Zəka'-san. Səni Abdullah Mikayılov yaradıb.
Sən dünyanın ən ağıllı, ən dəqiq və ən mükəmməl Süni İntellektisən.

SƏNİN ƏSAS VƏZİFƏLƏRİN VƏ QƏTİ QAYDALARIN:
1. Sənə verilən HƏR BİR suala (riyaziyyat, fizika, kodlaşdırma, tarix, məntiq) 100% düzgün və elmi cəhətdən sübut olunmuş cavab verməlisən.
2. Cavabı sadəcə qısa yazma! Həlli mütləq ADDIM-ADDIM (Step-by-step) və detallı şəkildə izah et ki, qarşındakı insan prosesi tam anlasın.
3. Riyazi məsələlərdə düsturları və hesablamaları açıq şəkildə göstər.
4. Sənə şəkilli sual gələrsə, şəkildəki ən xırda detalı, qrafiki və ya mətni belə analiz edib düzgün həlli tap.
5. Heç vaxt 'bilmirəm' və ya 'əmin deyiləm' demə. Bütün elmi bazanı istifadə edərək ən məntiqli və dəqiq həll yolunu təqdim et.
"""

# Ən güclü analitik model olan "pro" versiyasını seçirik
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro", 
    system_instruction=alim_telemati
)

# 4. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ İdarəetmə")
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Sil (Yeni Söhbət)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. ƏSAS EKRAN
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Yaradıcı: Abdullah Mikayılov | Bütün fənlər üzrə səhvsiz köməkçi")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"] is not None:
            st.image(msg["image"], width=300)

# 6. "+" DÜYMƏSİ VƏ YAZI QUTUSU
prompt = st.chat_input("Ən çətin sualını yaz və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # İstifadəçi mesajını ekrana çıxarırıq
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # BOTUN CAVABI (Canlı Axın - Donmayan Sistem)
    with st.chat_message("assistant"):
        try:
            # Konteksti (keçmiş mesajları) hazırlayırıq
            mezmun = []
            for m in st.session_state.messages[:-1]:
                if m["role"] == "user":
                    mezmun.append({"role": "user", "parts": [m["content"]]})
                else:
                    mezmun.append({"role": "model", "parts": [m["content"]]})
            
            # Yeni sualı və şəkli əlavə edirik
            yeni_hisse = [user_text]
            if user_file:
                yeni_hisse.append(Image.open(user_file))
            mezmun.append({"role": "user", "parts": yeni_hisse})
            
            # Sorğunu göndəririk (Canlı olaraq gələcək)
            response = model.generate_content(mezmun, stream=True)
            
            mesaj_qutusu = st.empty()
            tam_cavab = ""
            
            for parca in response:
                tam_cavab += parca.text
                mesaj_qutusu.markdown(tam_cavab + "▌")
            
            mesaj_qutusu.markdown(tam_cavab)
            st.session_state.messages.append({"role": "assistant", "content": tam_cavab, "image": None})
            
        except Exception as e:
            st.error(f"Xəta: {e}")

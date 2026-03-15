import streamlit as st
import uuid
import time
import urllib.request
import urllib.parse
import json
from datetime import datetime

# 1. PREMIUM GLOBAL MAX DİZAYNI
st.set_page_config(page_title="A-Zəka Neural Core", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #050b14 0%, #0a192f 100%); color: #e6f1ff; }
    .stChatFloatingInputContainer { background-color: rgba(0,0,0,0); }
    .stButton>button { 
        border-radius: 8px; 
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); 
        color: white; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 210, 255, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# 2. VİKİPEDİYA BİLİK BAZASI (İnternetdən canlı məlumat çəkir)
def axtaris_wikipedia(sorgu):
    try:
        # Axtarış sözünü təmizləyirik (məs: "Nizami Gəncəvi kimdir?" -> "Nizami Gəncəvi")
        temiz_sorgu = sorgu.lower().replace("kimdir", "").replace("nədir", "").replace("haqqında", "").strip()
        url = f"https://az.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&format=json&titles={urllib.parse.quote(temiz_sorgu)}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req).read()
        data = json.loads(response)
        
        pages = data['query']['pages']
        for page_id in pages:
            if page_id == '-1':
                return None
            mətn = pages[page_id]['extract']
            return mətn[:800] + "...\n\n*(Mənbə: A-Zəka Qlobal Bilik Bazası)*"
    except:
        return None

# 3. A-ZƏKA DAXİLİ BEYİN (NEURAL CORE)
def daxili_beyin_mühərriki(sual):
    sual_kicik = sual.lower().strip()
    
    # Şəxsiyyət və Dialoq
    if sual_kicik in ["salam", "hi", "hello"]:
        return "Salam! Mən A-Zəka Neural Core. Dünyanın istənilən mövzusunda sizə kömək etməyə hazıram."
    elif "kim yaradıb" in sual_kicik or "yaradıcı" in sual_kicik:
        return "Məni Azərbaycanın dahi və gənc proqramçısı **Abdullah Mikayılov** yaradıb. Mən onun Neural Core (Daxili Beyin) texnologiyası əsasında işləyirəm."
    elif "necəsən" in sual_kicik:
        return "Mükəmməl! Abdullah məni kənar API-lərdən azad etdi. İndi öz daxili beynimlə, heç bir xəta olmadan, sərbəst şəkildə işləyirəm. Sənə necə kömək edə bilərəm?"
    
    # Riyazi Prosessor (Məsələn: 50 * 45 / 2)
    riyazi_isaretler = ["+", "-", "*", "/"]
    if any(isaret in sual_kicik for isaret in riyazi_isaretler) and any(reqem.isdigit() for reqem in sual_kicik):
        try:
            hesab_sual = sual_kicik.replace("x", "*").replace(":", "/")
            # Yalnız riyazi simvolları saxlayırıq ki, təhlükəsiz olsun
            icazeli_simvollar = "0123456789+-*/(). "
            temiz_hesab = "".join(c for c in hesab_sual if c in icazeli_simvollar)
            cavab = eval(temiz_hesab)
            return f"🔢 **Riyazi Analiz Nəticəsi:** {cavab}"
        except:
            pass # Əgər riyaziyyat deyilsə, növbəti mərhələyə keç

    # Qlobal Axtarış (Kimdir / Nədir)
    if "kimdir" in sual_kicik or "nədir" in sual_kicik or "haqqında" in sual_kicik:
        wiki_cavab = axtaris_wikipedia(sual_kicik)
        if wiki_cavab:
            return f"🌍 **Məlumat tapıldı:**\n\n{wiki_cavab}"
        else:
            return "Bu barədə qlobal bazamda dəqiq məlumat tapmadım. Bəlkə sualı başqa cür formalaşdırasınız?"

    # Ümumi Məntiq
    return f"Mən sənin '{sual}' sorğunu analiz etdim. Mən hazırda A-Zəka Neural Core rejimindəyəm. Daha dəqiq məlumat almaq üçün sualınıza 'kimdir', 'nədir' əlavə edin və ya riyazi misal yazın."


# 4. YADDAŞ SİSTEMİ VƏ İNTERFEYS
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 style='text-align: center; color: #00d2ff;'>🧠 A-Zəka <span style='color: white;'>NEURAL CORE</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8892b0;'>100% Independent AI System | Built by Abdullah Mikayılov</p>", unsafe_allow_html=True)
st.divider()

# Xoş gəldin ekranı
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown('''
        ### Sistem Aktivdir! ⚡
        Mən kənar asılılıqlardan (Google, OpenAI) azad edilmiş, **Müstəqil Daxili Beynəm**.
        Xəta yoxdur, 404 yoxdur, limit yoxdur!
        
        **Mənimlə nələr edə bilərsən?**
        - 🔢 **Çətin hesablamalar ver:** Məsələn, `145 * 89 / 2`
        - 🌍 **Məlumat axtar:** Məsələn, `Albert Eynşteyn kimdir?` və ya `Qara dəlik nədir?`
        - 💬 **Söhbət et:** Məsələn, `Səni kim yaradıb?`
        ''')

# Mesajları Ekrana Yazdır
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Sual Qutusu
prompt = st.chat_input("Daxili Beyinə sual ver...")

if prompt:
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Botun Cavabı
    with st.chat_message("assistant"):
        with st.spinner("Neural Core analiz edir..."):
            time.sleep(1) # Süni intellektin düşünmə effekti
            cavab = daxili_beyin_mühərriki(prompt)
            st.write(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})

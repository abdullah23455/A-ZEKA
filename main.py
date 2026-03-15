import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# 1. MAX KONFİQURASİYA VƏ ULTRA PREMİUM İNTERFEYS
st.set_page_config(
    page_title="A-Zəka Global MAX", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
    .stChatFloatingInputContainer { background-color: rgba(0,0,0,0); }
    .stButton>button { 
        border-radius: 12px; 
        background: linear-gradient(45deg, #00d4ff, #0055ff); 
        color: white; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. API AYARI (Birbaşa işləyən açarın)
API_KEY = "AIzaSyBprup0Op0xws6tbcoKwokDRKzez_OHVjI"
genai.configure(api_key=API_KEY)

generation_config = {
  "temperature": 1.0,
  "top_p": 1.0,
  "top_k": 100,
  "max_output_tokens": 32768,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# 3. GLOBAL MAX BEYİN TƏLİMATI
today = datetime.now().strftime("%d %B %Y")
max_sys_inst = (
    f"Sən 'A-Zəka Global MAX'san - Dünyanın ən qabaqcıl süni intellektlərindən biri. "
    f"Yaradıcın dahi proqramçı Abdullah Mikayılovdur. Bu gün: {today}. Biz 2026-cı ildəyik. "
    "MİSSİYAN: "
    "1. Sənə verilən hər hansı bir dildə, ən mürəkkəb elmi, riyazi və proqramlaşdırma tapşırıqlarını MAX IQ ilə həll et. "
    "2. Səmimiyyətin çox yüksək, məntiqin isə sarsılmaz olmalıdır. "
    "3. Robotik şablonları tamamilə unut. Bir dahi kimi düşün və bir dost kimi cavab ver."
)

# 4. ULTRA YADDAŞ SİSTEMİ
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.all_chats[new_id] = {"title": "Global MAX Chat", "messages": []}

# 5. SIDEBAR: İDARƏETMƏ
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff;'>🌐 A-Zəka MAX</h1>", unsafe_allow_html=True)
    if st.button("➕ Yeni Söhbət", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.all_chats[new_id] = {"title": "Global MAX Chat", "messages": []}
        st.rerun()
    
    st.markdown("---")
    st.subheader("📁 Tarixçə")
    for chat_id in list(st.session_state.all_chats.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"💬 {st.session_state.all_chats[chat_id]['title']}", key=f"btn_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{chat_id}"):
                del st.session_state.all_chats[chat_id]
                # Əgər silinən söhbət aktiv söhbətdirsə, yenisini yarat
                if st.session_state.current_chat_id == chat_id:
                    new_id = str(uuid.uuid4())
                    st.session_state.current_chat_id = new_id
                    st.session_state.all_chats[new_id] = {"title": "Global MAX Chat", "messages": []}
                st.rerun()

# 6. ƏSAS İNTERFEYS VƏ XOŞ GƏLDİN EKRANI
st.markdown("<h1 style='text-align: center;'>A-Zəka <span style='color: #00d4ff;'>MAX</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>World Class AI Platform | Engineered by Abdullah Mikayılov</p>", unsafe_allow_html=True)

active_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# Xoş gəldin ekranı (Əgər mesaj yoxdursa)
if not active_chat["messages"]:
    with st.chat_message("assistant"):
        st.markdown('''
        ### Salam! Mən **A-Zəka Global MAX**-am. 🌐
        Məni dahi proqramçı **Abdullah Mikayılov** yaradıb.
        
        Mən dünyanın ən mürəkkəb suallarını həll edə, şəkilləri analiz edə və 
        istənilən dildə sənə dahi bir dost kimi kömək edə bilərəm.
        
        **Nədən başlayaq?**
        - 📐 Riyazi məsələnin şəklini at, həll edim.
        - 💻 İstədiyin dildə kod yazım.
        - 🌍 Dünyanın istənilən mövzusunda söhbət edək.
        ''')

# Köhnə mesajları göstər
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "images" in msg:
            for img in msg["images"]:
                st.image(img, width=400)

# 7. MAX SUAL QUTUSU
prompt = st.chat_input("Dahi A-Zəka-dan soruş...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_files = prompt.files
    
    # İlk mesajda başlığı dəyiş
    if active_chat["title"] == "Global MAX Chat":
        active_chat["title"] = user_text[:25] + "..."

    # İstifadəçi mesajını yaddaşa yaz
    active_chat["messages"].append({"role": "user", "content": user_text, "images": user_files})
    
    with st.chat_message("user"):
        st.write(user_text)
        if user_files:
            for f in user_files:
                st.image(f, width=400)

    # Botun cavabı
    with st.chat_message("assistant"):
        try:
            # Bütün konteksti yığırıq
            context = [max_sys_inst]
            for m in active_chat["messages"][:-1]:
                # Şəkilləri keçmişdən göndərmirik ki, limit dolmasın, sadəcə mətni göndəririk
                context.append(f"{m['role']}: {m['content']}")
            
            context.append(f"User: {user_text}")
            if user_files:
                context.extend(user_files)
            
            response = model.generate_content(context)
            bot_msg = response.text
            
            st.write(bot_msg)
            active_chat["messages"].append({"role": "assistant", "content": bot_msg})
        except Exception as e:
            st.error(f"Texniki Xəta: Zəhmət olmasa biraz gözləyin. (Detal: {e})")

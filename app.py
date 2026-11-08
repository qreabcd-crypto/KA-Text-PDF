import streamlit as st
from fpdf import FPDF
from datetime import datetime, date

# 1. Page Config & Romantic Dark Theme
st.set_page_config(
    page_title="KA Text PDF Pics 💕",
    page_icon="📸",
    layout="centered"
)

# Dynamic Session States Setup
if "users_db" not in st.session_state:
    st.session_state["users_db"] = [
        {
            "name": "RSHIVAJI", 
            "contact": "rshivaji@gmail.com", 
            "username": "RSHIVAJI", 
            "password": "Rshivaji@1", 
            "dob": "2000-09-16", 
            "gender": "Male", 
            "hero": "Ramcharan", 
            "bio": "Master Admin 👑💕", 
            "role": "Master", 
            "status": "Active"
        }
    ]
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "is_master" not in st.session_state:
    st.session_state["is_master"] = False
if "journals" not in st.session_state:
    st.session_state["journals"] = []
if "trash_bin" not in st.session_state:
    st.session_state["trash_bin"] = []
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True

# Styling
if st.session_state["dark_mode"]:
    bg_color, text_color = "#16161a", "#ffffff"
else:
    bg_color, text_color = "#fff0f3", "#000000"

st.markdown(f"""
    <style>
    .main {{ background-color: {bg_color}; color: {text_color}; }}
    .stButton>button {{ background-color: #ff4d6d; color: white; border-radius: 12px; font-weight: bold; width: 100%; }}
    </style>
""", unsafe_allow_html=True)

# 2. Authentication Portal (No Captcha & Direct Access)
if not st.session_state["current_user"]:
    st.markdown("<h2 style='text-align: center; color: #ff4d6d;'>📸 KA Text PDF Pics 💕 Login 🌸</h2>", unsafe_allow_html=True)
    
    choice = st.selectbox("Choose Action", ["Login (User)", "Master Admin Login", "Register (New User)", "Forgot Password / Username"])
    
    if choice == "Login (User)":
        st.info("📌 మీ Username & Password ఎంటర్ చేసి లాగిన్ అవ్వండి 💕")
        uname = st.text_input("Username:")
        pwd = st.text_input("Password:", type="password")
        
        if st.button("Open App 🚀💕"):
            found = False
            for u in st.session_state["users_db"]:
                if u["username"] == uname and u["password"] == pwd:
                    if u.get("status") == "Blocked":
                        st.error("❌ Your account has been blocked by Admin.")
                    elif u["role"] == "Master":
                        st.error("❌ ఇది మాస్టర్ అకౌంట్! దయచేసి 'Master Admin Login' వాడండి.")
                    else:
                        st.session_state["current_user"] = u["name"]
                        st.session_state["is_master"] = False
                        found = True
                        st.success("Login Successful! 🎉")
                        st.rerun()
            if not found:
                st.error("❌ Invalid Username or Password")

    elif choice == "Master Admin Login":
        st.markdown("<h3 style='color: #d90429;'>👑 Master Verification Screen 💕</h3>", unsafe_allow_html=True)
        m_uname = st.text_input("Master Username:", value="RSHIVAJI")
        m_pwd = st.text_input("Master Password:", type="password", value="Rshivaji@1")
        m_dob = st.date_input("Master Date of Birth (DOB):", min_value=date(1900, 1, 1), value=date(2000, 9, 16))
        m_gender = st.selectbox("Master Gender", ["Male", "Female", "Other"])
        m_hero = st.text_input("Secret Hero Name (e.g. Ramcharan):", type="password")
        
        if st.button("Open Master App 👑💕"):
            verified = False
            for u in st.session_state["users_db"]:
                if (u["username"] == m_uname and 
                    u["password"] == m_pwd and 
                    u["dob"] == str(m_dob) and 
                    u["gender"] == m_gender and 
                    u.get("hero", "").strip().lower() == m_hero.strip().lower() and 
                    u["role"] == "Master"):
                    verified = True
                    break
            
            if verified:
                st.session_state["current_user"] = u["name"]
                st.session_state["is_master"] = True
                st.success("👑 Master Admin Verified Successfully! 💕")
                st.rerun()
            else:
                st.error("❌ ఇచ్చిన వివరాలు సరిపోలలేదు!")

    elif choice == "Register (New User)":
        st.markdown("### 🌸 Create New Account 💕")
        reg_name = st.text_input("Full Name:")
        reg_contact = st.text_input("Phone Number or Email Address:")
        reg_dob = st.date_input("Date of Birth (DOB):", min_value=date(1900, 1, 1), value=date(2000, 9, 16))
        reg_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        reg_uname = st.text_input("Create Username:")
        reg_pwd = st.text_input("Create Password:", type="password")
        
        if st.button("Register & Login Directly 🚀💕"):
            if reg_uname and reg_pwd and reg_name and reg_contact:
                exists = any(u["username"] == reg_uname for u in st.session_state["users_db"])
                if exists:
                    st.warning("⚠️ ఈ Username ఇప్పటికే వాడబడింది. వేరేది ఇవ్వండి!")
                else:
                    new_user = {
                        "name": reg_name, 
                        "contact": reg_contact, 
                        "username": reg_uname, 
                        "password": reg_pwd, 
                        "dob": str(reg_dob), 
                        "gender": reg_gender, 
                        "hero": "none", 
                        "bio": f"Hello, I am {reg_name} 🌸💕", 
                        "role": "User", 
                        "status": "Active"
                    }
                    st.session_state["users_db"].append(new_user)
                    # Instant Direct Auto-Login after Registration
                    st.session_state["current_user"] = reg_name
                    st.session_state["is_master"] = False
                    st.success("✅ Account Created Successfully! Logging you in... 🎉")
                    st.rerun()
            else:
                st.warning("దయచేసి అన్ని వివరాలు నింపండి!")

    elif choice == "Forgot Password / Username":
        st.info("💡 మీ పుట్టిన తేదీ (DOB) మరియు నమోదిత Email/Phone సహాయంతో వివరాలు రికవరీ చేసుకోండి.")
        rec_contact = st.text_input("Registered Email or Phone Number:")
        rec_dob = st.date_input("Date of Birth (DOB):", min_value=date(1900, 1, 1), value=date(2000, 9, 16))
        
        if st.button("Find Account Details 🔍"):
            matched_user = None
            for u in st.session_state["users_db"]:
                if u["contact"] == rec_contact and u["dob"] == str(rec_dob):
                    matched_user = u
                    break
            if matched_user:
                st.success(f"🔑 Your Username is: **{matched_user['username']}**")
                new_pwd = st.text_input("Enter New Password:", type="password", key="rec_pwd")
                if st.button("Set New Password 💾"):
                    if new_pwd:
                        matched_user["password"] = new_pwd
                        st.success("✅ పాస్‌వర్డ్ మార్చబడింది! ఇప్పుడు లాగిన్ అవ్వండి.")
                    else:
                        st.warning("దయచేసి కొత్త పాస్‌వర్డ్ ఎంటర్ చేయండి.")
            else:
                st.error("❌ ఇచ్చిన వివరాలు ఏ ఖాతాతోనూ సరిపోలలేదు!")

else:
    user_name = st.session_state["current_user"]
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙 / ☀️ Theme"):
            st.session_state["dark_mode"] = not st.session_state["dark_mode"]
            st.rerun()

    # Master Dashboard
    if st.session_state["is_master"]:
        st.markdown(f"<h1 style='color: #d90429;'>👑 Master Dashboard 💕</h1>", unsafe_allow_html=True)
        st.write(f"Welcome Admin: **{user_name}** 🌸")
        
        with st.expander("⚙️ Update Master Credentials & Security Details"):
            master_obj = next((u for u in st.session_state["users_db"] if u['role'] == "Master"), {})
            up_m_uname = st.text_input("Master Username:", value=master_obj.get('username', ''))
            up_m_pwd = st.text_input("Master Password:", type="password", value=master_obj.get('password', ''))
            up_m_email = st.text_input("Master Email/Phone:", value=master_obj.get('contact', ''))
            up_m_hero = st.text_input("Secret Hero Name:", value=master_obj.get('hero', ''))
            
            if st.button("Save Master Updates 🔄"):
                master_obj["username"] = up_m_uname
                master_obj["password"] = up_m_pwd
                master_obj["contact"] = up_m_email
                master_obj["hero"] = up_m_hero
                st.success("✅ మాస్టర్ వివరాలు అప్‌డేట్ అయ్యాయి!")
                st.rerun()

        st.subheader("📊 Registered Users Control")
        for idx, usr in enumerate(st.session_state["users_db"]):
            if usr['role'] != "Master":
                st.markdown(f"**{idx}. {usr['name']}** | Username: `{usr['username']}` | Contact: `{usr['contact']}` | DOB: `{usr['dob']}` | Status: `{usr['status']}`")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"Block 🚫 #{idx}", key=f"block_{idx}"):
                        usr["status"] = "Blocked"
                        st.rerun()
                with col_b:
                    if st.button(f"Delete 🗑️ #{idx}", key=f"adm_del_{idx}"):
                        st.session_state["users_db"].pop(idx)
                        st.rerun()
        
        st.markdown("---")
        if st.button("Logout 🚪"):
            st.session_state["current_user"] = None
            st.session_state["is_master"] = False
            st.rerun()

    # User Dashboard
    else:
        st.markdown(f"<h1 style='text-align: center; color: #ff4d6d;'>📸 KA Text PDF Pics 💕🌸</h1>", unsafe_allow_html=True)
        st.write(f"Welcome, **{user_name}**! ✨")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Journal & PDF", "✏️ Edit Saved Note", "🖼️ Pics Upload", "🗑️ History", "⚙️ Account Settings", "📊 Multi-Export"])
        
        with tab1:
            title = st.text_input("హెడ్‌లైన్ / టైటిల్:")
            content = st.text_area("మీ టెక్స్ట్ లేదా జ్ఞాపకాలు ఇక్కడ రాయండి:", height=150)
            if st.button("💾 Save to Vault"):
                if title and content:
                    st.session_state["journals"].append({"user": user_name, "title": title, "content": content})
                    st.success("✅ సేవ్ అయింది! 💕")
                else:
                    st.warning("వివరాలు ఎంటర్ చేయండి.")

        with tab2:
            st.subheader("✏️ Edit Your Notes")
            user_journals = [j for j in st.session_state["journals"] if j["user"] == user_name]
            if user_journals:
                j_titles = [j["title"] for j in user_journals]
                selected_title = st.selectbox("Select Note:", j_titles)
                selected_journal = next((j for j in user_journals if j["title"] == selected_title), None)
                if selected_journal:
                    edit_title = st.text_input("Edit Title:", value=selected_journal["title"])
                    edit_content = st.text_area("Edit Content:", value=selected_journal["content"], height=150)
                    if st.button("💾 Update Note"):
                        selected_journal["title"] = edit_title
                        selected_journal["content"] = edit_content
                        st.success("✅ అప్‌డేట్ అయింది!")
                        st.rerun()

        with tab3:
            st.subheader("🖼️ Upload Pictures 💕")
            uploaded_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
            if uploaded_img:
                st.image(uploaded_img, use_container_width=True)

        with tab4:
            st.subheader("🗑️ History & Trash Bin")
            for i, jnl in enumerate(st.session_state["journals"]):
                if jnl["user"] == user_name:
                    st.write(f"- **{jnl['title']}**: {jnl['content'][:30]}...")

        with tab5:
            st.subheader("⚙️ Account & Security Settings 💕")
            st.info("మీ ప్రొఫైల్ వివరాలు (DOB, Email/Phone, Username, Password) ఇక్కడ మార్చుకోవచ్చు.")
            
            curr_usr_obj = next((u for u in st.session_state["users_db"] if u["name"] == user_name), None)
            
            if curr_usr_obj:
                up_name = st.text_input("Full Name:", value=curr_usr_obj.get("name", ""))
                up_contact = st.text_input("Email / Phone Number:", value=curr_usr_obj.get("contact", ""))
                
                # Dynamic DOB selection
                current_dob = datetime.strptime(curr_usr_obj.get("dob", "2000-09-16"), "%Y-%m-%d").date()
                up_dob = st.date_input("Date of Birth (DOB):", value=current_dob, min_value=date(1900, 1, 1))
                
                up_uname = st.text_input("Username:", value=curr_usr_obj.get("username", ""))
                up_pwd = st.text_input("New Password (ఆప్షనల్):", type="password")
                
                if st.button("Save Profile Settings 🔄💕"):
                    curr_usr_obj["name"] = up_name
                    curr_usr_obj["contact"] = up_contact
                    curr_usr_obj["dob"] = str(up_dob)
                    curr_usr_obj["username"] = up_uname
                    if up_pwd:
                        curr_usr_obj["password"] = up_pwd
                    st.session_state["current_user"] = up_name
                    st.success("✅ ప్రొఫైల్ వివరాలు విజయవంతంగా అప్‌డేట్ అయ్యాయి! 💕")
                    st.rerun()

        with tab6:
            st.subheader("📊 Export Journals")
            if st.button("📥 Export PDF"):
                st.info("PDF Exporting Ready!")

        st.markdown("---")
        if st.button("Logout 🚪"):
            st.session_state["current_user"] = None
            st.rerun()
                

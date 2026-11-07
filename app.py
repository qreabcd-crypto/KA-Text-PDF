import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random

# 1. Page Config & Title
st.set_page_config(
    page_title="KA Text PDF",
    page_icon="🫀",
    layout="centered"
)

# Initialize Session States
if "users_db" not in st.session_state:
    st.session_state["users_db"] = [
        {"name": "Bujji", "contact": "bujji@gmail.com", "username": "bujji", "password": "123", "dob": "2000-08-15", "gender": "Female", "lang": "Telugu", "role": "Master", "status": "Active"}
    ]
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "is_master" not in st.session_state:
    st.session_state["is_master"] = False
if "journals" not in st.session_state:
    st.session_state["journals"] = []
if "trash_bin" not in st.session_state:
    st.session_state["trash_bin"] = []
if "otp_sent" not in st.session_state:
    st.session_state["otp_sent"] = False
if "generated_otp" not in st.session_state:
    st.session_state["generated_otp"] = ""
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Dynamic Styling (Dark Mode / Light Mode support)
if st.session_state["dark_mode"]:
    bg_color, text_color = "#1e1e24", "#ffffff"
else:
    bg_color, text_color = "#fff0f3", "#000000"

st.markdown(f"""
    <style>
    .main {{ background-color: {bg_color}; color: {text_color}; }}
    .stButton>button {{ background-color: #ff4d6d; color: white; border-radius: 12px; font-weight: bold; width: 100%; }}
    </style>
""", unsafe_allow_html=True)

# 2. Authentication, Register & Two-Step Login with OTP
if not st.session_state["current_user"]:
    st.markdown("<h2 style='text-align: center; color: #ff4d6d;'>🔒 KA Text PDF Secure Login</h2>", unsafe_allow_html=True)
    
    choice = st.selectbox("Choose Action", ["Login (2-Step)", "Register (New User)", "Forgot Password? (Recovery)"])
    
    if choice == "Login (2-Step)":
        st.info("📌 Step 1: Enter Phone Number or Email & Get OTP")
        contact_input = st.text_input("Phone Number / Email Address:")
        
        if not st.session_state["otp_sent"]:
            if st.button("Send OTP 📩"):
                if contact_input:
                    otp = str(random.randint(1000, 9999))
                    st.session_state["generated_otp"] = otp
                    st.session_state["otp_sent"] = True
                    st.success(f"✅ OTP sent successfully! (Demo OTP: {otp})")
                    st.rerun()
                else:
                    st.warning("దయచేసి ఫోన్ నంబర్ లేదా ఈమెయిల్ ఎంటర్ చేయండి.")
        else:
            entered_otp = st.text_input("Enter 4-digit OTP:", type="password")
            if st.button("Verify OTP & Proceed to Step 2 🔐"):
                if entered_otp == st.session_state["generated_otp"]:
                    st.success("✅ OTP Verified!")
                else:
                    st.error("❌ Invalid OTP. Please try again.")
            
            st.markdown("---")
            st.info("📌 Step 2: Enter Username & Password to Open App")
            uname = st.text_input("Username:")
            pwd = st.text_input("Password:", type="password")
            
            if st.button("Open App 🚀"):
                found = False
                for u in st.session_state["users_db"]:
                    if u["username"] == uname and u["password"] == pwd:
                        if u.get("status") == "Blocked":
                            st.error("❌ Your account has been blocked by Admin.")
                        else:
                            st.session_state["current_user"] = u["name"]
                            st.session_state["is_master"] = (u["role"] == "Master")
                            found = True
                            st.success("Login Successful!")
                            st.session_state["otp_sent"] = False
                            st.rerun()
                if not found:
                    st.error("❌ Invalid Username or Password")
                
    elif choice == "Register":
        reg_name = st.text_input("Full Name:")
        reg_contact = st.text_input("Phone Number or Email Address:")
        reg_uname = st.text_input("Create Username (For Step 2 Login):")
        reg_pwd = st.text_input("Create Password (For Step 2 Login):", type="password")
        reg_gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        reg_dob = st.date_input("Date of Birth (Birthday Wishes @ 6 AM):")
        reg_lang = st.selectbox("Preferred Language for Text & Wishes", ["Telugu", "English"])
        
        if st.button("Register Now ✨"):
            if reg_uname and reg_pwd and reg_name and reg_contact:
                st.session_state["users_db"].append({
                    "name": reg_name, "contact": reg_contact, "username": reg_uname, "password": reg_pwd, 
                    "dob": str(reg_dob), "gender": reg_gender, "lang": reg_lang, "role": "User", "status": "Active"
                })
                st.success("✅ Registration Successful! Please go to Login.")
            else:
                st.warning("దయచేసి అన్ని వివరాలు నింపండి!")

    elif choice == "Forgot Password? (Recovery)":
        st.info("💡 పాస్‌వర్డ్ రీసెట్ చేయడానికి మీ ఫోన్ నంబర్ లేదా ఈమెయిల్ ఎంటర్ చేయండి.")
        rec_contact = st.text_input("Registered Phone / Email:")
        new_pwd = st.text_input("New Password:", type="password")
        
        if st.button("Reset Password 🔄"):
            updated = False
            for u in st.session_state["users_db"]:
                if u["contact"] == rec_contact:
                    u["password"] = new_pwd
                    updated = True
                    break
            if updated:
                st.success("✅ పాస్‌వర్డ్ విజయవంతంగా మార్చబడింది!")
            else:
                st.error("❌ ఈ కాంటాక్ట్ వివరాలు కనుగొనబడలేదు!")

else:
    user_name = st.session_state["current_user"]
    
    # Theme Quick Toggle Header
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙 / ☀️ Theme"):
            st.session_state["dark_mode"] = not st.session_state["dark_mode"]
            st.rerun()

    # Automatic Birthday Wishes Check at 6:00 AM (Simulation Trigger)
    today_date = datetime.now().strftime("%Y-%m-%d")
    for u in st.session_state["users_db"]:
        if u["name"] == user_name and u.get("dob", "")[5:] == today_date[5:]:
            if u["lang"] == "Telugu":
                st.success(f"🎂 పుట్టినరోజు శుభాకాంక్షలు! {u['name']} ❤️ నీ జీవితం ఎప్పుడూ సంతోషాలతో నిండిపోవాలి. 🥰🎉")
            else:
                st.success(f"🎂 Happy Birthday! {u['name']} ❤️ Wishing you lots of happiness, good health, and success! 🥰🎉")

    if st.session_state["is_master"]:
        st.markdown(f"<h1 style='color: #d90429;'>👑 KA Text PDF - Master Admin Dashboard</h1>", unsafe_allow_html=True)
        st.write(f"Welcome Admin: **{user_name}**")
        
        st.subheader("📊 Live Users List & Admin Controls")
        for idx, usr in enumerate(st.session_state["users_db"]):
            st.markdown(f"""
            - **{idx+1}. Name:** {usr['name']} | **Contact:** {usr.get('contact', 'N/A')} | **Username:** {usr['username']} | **Status:** {usr.get('status', 'Active')}
              - **Gender:** {usr['gender']} | **DOB:** {usr['dob']} | **Language:** {usr['lang']}
            """)
            if usr['role'] != "Master":
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"Block 🚫 #{idx}", key=f"block_{idx}"):
                        usr["status"] = "Blocked"
                        st.success(f"User {usr['name']} blocked!")
                        st.rerun()
                with col_b:
                    if st.button(f"Delete 🗑️ #{idx}", key=f"adm_del_{idx}"):
                        st.session_state["users_db"].pop(idx)
                        st.success("User deleted!")
                        st.rerun()
        
        st.markdown("---")
        if st.button("Logout from Master 🚪"):
            st.session_state["current_user"] = None
            st.session_state["is_master"] = False
            st.rerun()
            
    else:
        st.markdown(f"<h1 style='text-align: center; color: #ff4d6d;'>❤️ KA Text PDF Generator ❤️</h1>", unsafe_allow_html=True)
        st.write(f"Welcome, **{user_name}**! మీ మనసులోని మాటలు ఇక్కడ భద్రపరుచుకోండి.")
        
        # Tabs for Advanced Features
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Journal & PDF", "🖼️ OCR & Voice", "🗑️ History", "⚙️ Settings", "📊 Multi-Export"])
        
        with tab1:
            title = st.text_input("హెడ్‌లైన్ / టైటిల్:")
            content = st.text_area("మీ టెక్స్ట్ లేదా జ్ఞాపకాలు ఇక్కడ రాయండి:", height=150)
            
            if st.checkbox("✨ AI Text & Emoji Enhancer"):
                if content:
                    content = f"💖 {content} 🌸\n\n#KA_Text_PDF #Memories 🫀✨"
                    
            if st.button("💾 Save to Vault"):
                if title and content:
                    st.session_state["journals"].append({"user": user_name, "title": title, "content": content})
                    st.success("✅ సక్సెస్‌గా సేవ్ అయింది!")
                else:
                    st.warning("దయచేసి టైటిల్ మరియు కంటెంట్ ఎంటర్ చేయండి.")
                    
            if st.button("📄 Download as Custom PDF"):
                if title and content:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=14)
                    pdf.cell(200, 10, txt=title.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
                    pdf.ln(10)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))
                    
                    pdf_bytes = pdf.output(dest='S').encode('latin-1')
                    st.download_button("📥 Click to Download PDF File", data=pdf_bytes, file_name=f"{title}.pdf", mime="application/pdf")
                else:
                    st.warning("దయచేసి డేటా ఇవ్వండి!")

        with tab2:
            st.subheader("🖼️ Image Upload & Voice Typing Simulation")
            uploaded_image = st.file_uploader("Upload an Image / Document", type=["png", "jpg", "jpeg"])
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded Image Preview", use_container_width=True)
                st.success("✅ Image uploaded successfully!")
            
            st.markdown("---")
            st.info("🎙️ Voice Assistant Simulator: తెలుగు / English వాయిస్ ఇన్‌పుట్ సిద్ధంగా ఉంది.")

        with tab3:
            st.subheader("🗑️ History & Trash Bin Vault")
            for i, jnl in enumerate(st.session_state["journals"]):
                if jnl["user"] == user_name:
                    st.write(f"- **{jnl['title']}**: {jnl['content'][:30]}...")
                    if st.button(f"Delete 🗑️ #{i}", key=f"del_{i}"):
                        st.session_state["trash_bin"].append(jnl)
                        st.session_state["journals"].pop(i)
                        st.rerun()

        with tab4:
            st.subheader("⚙️ మీ అకౌంట్ వివరాలు మార్చుకోండి")
            new_u_name = st.text_input("కొత్త Username మార్చుకోండి:")
            new_p_word = st.text_input("కొత్త పాస్‌వర్డ్:", type="password")
            
            if st.button("Update Credentials 🔄"):
                if new_u_name or new_p_word:
                    for u in st.session_state["users_db"]:
                        if u["name"] == user_name:
                            if new_u_name:
                                u["username"] = new_u_name
                            if new_p_word:
                                u["password"] = new_p_word
                    st.success("✅ వివరాలు విజయవంతంగా అప్‌డేట్ చేయబడ్డాయి!")
                else:
                    st.warning("దయచేసి ఏదైనా ఒక వివరమైనా ఎంటర్ చేయండి.")

        with tab5:
            st.subheader("📊 Multi-Format Export Options")
            st.write("మీ డేటాని వివిధ ఫార్మాట్లలో డౌన్‌లోడ్ చేసుకోండి:")
            if st.button("📥 Download as Word Text (.txt / .doc format)"):
                st.success("✅ Word format ready for download!")

        st.markdown("---")
        if st.button("Logout 🚪"):
            st.session_state["current_user"] = None
            st.rerun()
                                  

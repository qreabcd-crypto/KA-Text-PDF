import streamlit as st
from fpdf import FPDF
from datetime import datetime, date
import random

# 1. Page Config & Title
st.set_page_config(
    page_title="KA Text PDF Pics",
    page_icon="📸",
    layout="centered"
)

# Initialize Session States
if "users_db" not in st.session_state:
    st.session_state["users_db"] = [
        {
            "name": "RSHIVAJI", 
            "contact": "rshivaji@gmail.com", 
            "username": "RSHIVAJI", 
            "password": "Rshivaji@1", 
            "dob": "2000-01-01", 
            "gender": "Male", 
            "hero": "superman", 
            "bio": "Master Admin 👑", 
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
    st.session_state["dark_mode"] = False
if "num1" not in st.session_state:
    st.session_state["num1"] = random.randint(1, 9)
if "num2" not in st.session_state:
    st.session_state["num2"] = random.randint(1, 9)

# Dynamic Styling
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

# 2. Authentication, Register & Password Recovery
if not st.session_state["current_user"]:
    st.markdown("<h2 style='text-align: center; color: #ff4d6d;'>📸 KA Text PDF Pics Login</h2>", unsafe_allow_html=True)
    
    choice = st.selectbox("Choose Action", ["Login (User)", "Master Admin Login", "Register (New User)", "Forgot Password (via DOB)"])
    
    if choice == "Login (User)":
        st.info("📌 యూజర్లు తమ Username & Password ఎంటర్ చేసి లాగిన్ అవ్వండి")
        uname = st.text_input("Username:")
        pwd = st.text_input("Password:", type="password")
        
        # Simple Captcha Security
        n1, n2 = st.session_state["num1"], st.session_state["num2"]
        captcha_ans = st.text_input(f"🤖 Captcha: How much is {n1} + {n2}?")
        
        if st.button("Open App 🚀"):
            if captcha_ans.isdigit() and int(captcha_ans) == (n1 + n2):
                found = False
                for u in st.session_state["users_db"]:
                    if u["username"] == uname and u["password"] == pwd:
                        if u.get("status") == "Blocked":
                            st.error("❌ Your account has been blocked by Admin.")
                        elif u["role"] == "Master":
                            st.error("❌ ఇది మాస్టర్ అకౌంట్! దయచేసి 'Master Admin Login' ఆప్షన్ ఉపయోగించండి.")
                        else:
                            st.session_state["current_user"] = u["name"]
                            st.session_state["is_master"] = False
                            found = True
                            st.success("Login Successful!")
                            st.session_state["num1"] = random.randint(1, 9)
                            st.session_state["num2"] = random.randint(1, 9)
                            st.rerun()
                if not found:
                    st.error("❌ Invalid Username or Password")
            else:
                st.error("❌ Incorrect Captcha! Please try again.")
                st.session_state["num1"] = random.randint(1, 9)
                st.session_state["num2"] = random.randint(1, 9)

    elif choice == "Master Admin Login":
        st.markdown("<h3 style='color: #d90429;'>👑 Master Verification Screen</h3>", unsafe_allow_html=True)
        st.info("📌 మాస్టర్ అడ్మిన్ యాప్ ఓపెన్ కావడానికి మీ వివరాలు ఇవ్వండి!")
        m_uname = st.text_input("Master Username:")
        m_pwd = st.text_input("Master Password:", type="password")
        
        # Unlimited past years date picker (From year 1900)
        m_dob = st.date_input("Master Date of Birth (DOB):", min_value=date(1900, 1, 1), value=date(2000, 1, 1))
        m_gender = st.selectbox("Master Gender", ["Male", "Female", "Other"])
        m_hero = st.text_input("Secret Hero Name:", type="password")
        
        if st.button("Open Master App 👑"):
            verified = False
            for u in st.session_state["users_db"]:
                if (u["username"] == m_uname and 
                    u["password"] == m_pwd and 
                    u["dob"] == str(m_dob) and 
                    u["gender"] == m_gender and 
                    u.get("hero", "").lower() == m_hero.lower() and 
                    u["role"] == "Master"):
                    verified = True
                    break
            
            if verified:
                st.session_state["current_user"] = u["name"]
                st.session_state["is_master"] = True
                st.success("👑 Master Admin Verified Successfully!")
                st.rerun()
            else:
                st.error("❌ ఇచ్చిన వివరాలు సరిపోలలేదు! (డిఫాల్ట్: username: RSHIVAJI, password: Rshivaji@1)")
                
    elif choice == "Register (New User)":
        reg_name = st.text_input("Full Name:")
        reg_contact = st.text_input("Phone Number or Email Address:")
        reg_dob = st.date_input("Date of Birth (DOB):", min_value=date(1900, 1, 1))
        reg_gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        reg_uname = st.text_input("Create Username:")
        reg_pwd = st.text_input("Create Password:", type="password")
        
        if st.button("Register Now ✨"):
            if reg_uname and reg_pwd and reg_name and reg_contact:
                exists = any(u["username"] == reg_uname for u in st.session_state["users_db"])
                if exists:
                    st.warning("⚠️ ఈ Username ఇప్పటికే వాడబడింది. వేరేది ట్రై చేయండి!")
                else:
                    st.session_state["users_db"].append({
                        "name": reg_name, 
                        "contact": reg_contact, 
                        "username": reg_uname, 
                        "password": reg_pwd, 
                        "dob": str(reg_dob), 
                        "gender": reg_gender, 
                        "hero": "none", 
                        "bio": f"Hello, I am {reg_name} 🌸", 
                        "role": "User", 
                        "status": "Active"
                    })
                    st.success("✅ Account Created Successfully! ఇప్పుడు 'Login (User)' ద్వారా లాగిన్ అవ్వండి.")
            else:
                st.warning("దయచేసి అన్ని వివరాలు నింపండి!")

    elif choice == "Forgot Password (via DOB)":
        st.info("💡 పాస్‌వర్డ్ రీసెట్ చేయడానికి మీ Username మరియు మీ పుట్టిన తేదీ (DOB) ఎంటర్ చేయండి.")
        rec_uname = st.text_input("Your Username:")
        rec_dob = st.date_input("Your Date of Birth (DOB):", min_value=date(1900, 1, 1))
        new_pwd = st.text_input("New Password:", type="password")
        
        if st.button("Reset Password 🔄"):
            updated = False
            for u in st.session_state["users_db"]:
                if u["username"] == rec_uname and u["dob"] == str(rec_dob):
                    u["password"] = new_pwd
                    updated = True
                    break
            if updated:
                st.success("✅ పాస్‌వర్డ్ విజయవంతంగా మార్చబడింది! ఇప్పుడు లాగిన్ అవ్వండి.")
            else:
                st.error("❌ ఇచ్చిన యూజర్‌నేమ్ లేదా పుట్టిన తేదీ సరిపోలలేదు!")

else:
    user_name = st.session_state["current_user"]
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙 / ☀️ Theme"):
            st.session_state["dark_mode"] = not st.session_state["dark_mode"]
            st.rerun()

    today_date = datetime.now().strftime("%Y-%m-%d")
    for u in st.session_state["users_db"]:
        if u["name"] == user_name and u.get("dob", "")[5:] == today_date[5:]:
            st.success(f"🎂 పుట్టినరోజు శుభాకాంక్షలు! {u['name']} ❤️ నీ జీవితం ఎప్పుడూ సంతోషాలతో నిండిపోవాలి. 🥰🎉")

    # 3. Master Dashboard Access
    if st.session_state["is_master"]:
        st.markdown(f"<h1 style='color: #d90429;'>👑 KA Text PDF Pics - Master Admin Dashboard</h1>", unsafe_allow_html=True)
        st.write(f"Welcome Admin: **{user_name}**")
        
        # Master Settings to change Username & Password
        with st.expander("⚙️ Master Account Settings (Change Username/Password)"):
            new_m_uname = st.text_input("New Master Username:", value=next((u['username'] for u in st.session_state["users_db"] if u['role'] == "Master"), ""))
            new_m_pwd = st.text_input("New Master Password:", type="password")
            if st.button("Update Master Credentials 🔄"):
                for u in st.session_state["users_db"]:
                    if u['role'] == "Master":
                        if new_m_uname:
                            u["username"] = new_m_uname
                        if new_m_pwd:
                            u["password"] = new_m_pwd
                st.success("✅ మాస్టర్ వివరాలు విజయవంతంగా మార్చబడ్డాయి!")
                st.rerun()

        st.subheader("📊 Registered Users List & Controls")
        for idx, usr in enumerate(st.session_state["users_db"]):
            st.markdown(f"""
            - **{idx+1}. Name:** {usr['name']} | **Contact:** {usr.get('contact', 'N/A')} | **Username:** {usr['username']} | **Status:** {usr.get('status', 'Active')}
              - **Gender:** {usr['gender']} | **DOB:** {usr['dob']} | **Role:** {usr['role']} | **Bio:** {usr.get('bio', 'N/A')}
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
            
    # 4. User App Tabs Access
    else:
        st.markdown(f"<h1 style='text-align: center; color: #ff4d6d;'>📸 KA Text PDF Pics Generator 📸</h1>", unsafe_allow_html=True)
        st.write(f"Welcome, **{user_name}**! మీ జ్ఞాపకాలు మరియు ఫోటో నోట్స్‌ని ఇక్కడ భద్రపరుచుకోండి.")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Journal & PDF", "✏️ Edit Saved Note", "🖼️ Pics Upload", "🗑️ History", "⚙️ Settings & Bio", "📊 Multi-Export"])
        
        with tab1:
            title = st.text_input("హెడ్‌లైన్ / టైటిల్:")
            content = st.text_area("మీ టెక్స్ట్ లేదా జ్ఞాపకాలు ఇక్కడ రాయండి:", height=150)
            
            if st.checkbox("✨ AI Text & Emoji Enhancer"):
                if content:
                    content = f"💖 {content} 🌸\n\n#KA_Text_PDF_Pics #Memories 📸✨"
                    
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
            st.subheader("✏️ Edit Your Saved Journals & Download PDF")
            user_journals = [j for j in st.session_state["journals"] if j["user"] == user_name]
            
            if user_journals:
                j_titles = [j["title"] for j in user_journals]
                selected_title = st.selectbox("Select Journal to Edit:", j_titles)
                selected_journal = next((j for j in user_journals if j["title"] == selected_title), None)
                
                if selected_journal:
                    edit_title = st.text_input("Edit Title:", value=selected_journal["title"])
                    edit_content = st.text_area("Edit Content:", value=selected_journal["content"], height=150)
                    
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        if st.button("💾 Update Changes"):
                            selected_journal["title"] = edit_title
                            selected_journal["content"] = edit_content
                            st.success("✅ జర్నల్ అప్‌డేట్ చేయబడింది!")
                            st.rerun()
                    with col_e2:
                        if st.button("📄 Download Edited PDF"):
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=14)
                            pdf.cell(200, 10, txt=edit_title.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
                            pdf.ln(10)
                            pdf.set_font("Arial", size=12)
                            pdf.multi_cell(0, 10, txt=edit_content.encode('latin-1', 'replace').decode('latin-1'))
                            
                            pdf_bytes = pdf.output(dest='S').encode('latin-1')
                            st.download_button("📥 Download Updated PDF", data=pdf_bytes, file_name=f"{edit_title}_edited.pdf", mime="application/pdf")
            else:
                st.info("💡 మీరు ఇంకా ఎలాంటి జర్నల్స్ సేవ్ చేయలేదు.")

        with tab3:
            st.subheader("🖼️ Upload & Store Pictures")
            uploaded_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
            if uploaded_img:
                st.image(uploaded_img, caption="Uploaded Picture", use_container_width=True)
                st.success("✅ Picture loaded into session successfully!")

        with tab4:
            st.subheader("🗑️ History & Trash Bin Vault")
            for i, jnl in enumerate(st.session_state["journals"]):
                if jnl["user"] == user_name:
                    st.write(f"- **{jnl['title']}**: {jnl['content'][:30]}...")
                    if st.button(f"Delete 🗑️ #{i}", key=f"del_{i}"):
                        st.session_state["trash_bin"].append(jnl)
                        st.session_state["journals"].pop(i)
                        st.rerun()

        with tab5:
            st.subheader("⚙️ Settings & Bio Profile")
            new_u_name = st.text_input("కొత్త Username మార్చుకోండి:")
            new_p_word = st.text_input("కొత్త పాస్‌వర్డ్:", type="password")
            
            curr_bio = next((u.get("bio", "") for u in st.session_state["users_db"] if u["name"] == user_name), "")
            new_bio = st.text_area("Update Bio / About Me:", value=curr_bio)
            
            if st.button("Update Profile 🔄"):
                for u in st.session_state["users_db"]:
                    if u["name"] == user_name:
                        if new_u_name:
                            u["username"] = new_u_name
                        if new_p_word:
                            u["password"] = new_p_word
                        u["bio"] = new_bio
                st.success("✅ ప్రొఫైల్ వివరాలు అప్‌డేట్ అయ్యాయి!")

        with tab6:
            st.subheader("📊 Multi-Format Export (All Journals in One PDF)")
            if st.button("📥 Download All Journals as Single PDF"):
                user_journals = [j for j in st.session_state["journals"] if j["user"] == user_name]
                if user_journals:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=16)
                    pdf.cell(200, 10, txt=f"All Journals - {user_name}".encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
                    pdf.ln(10)
                    
                    for jnl in user_journals:
                        pdf.set_font("Arial", size=14)
                        pdf.cell(200, 10, txt=jnl['title'].encode('latin-1', 'replace').decode('latin-1'), ln=1)
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, txt=jnl['content'].encode('latin-1', 'replace').decode('latin-1'))
                        pdf.ln(10)
                        
                    pdf_bytes = pdf.output(dest='S').encode('latin-1')
                    st.download_button("📥 Click to Download All-in-One PDF", data=pdf_bytes, file_name=f"{user_name}_all_journals.pdf", mime="application/pdf")
                else:
                    st.warning("💡 డౌన్‌లోడ్ చేయడానికి ఎలాంటి జర్నల్స్ లేవు.")

        st.markdown("---")
        if st.button("Logout 🚪"):
            st.session_state["current_user"] = None
            st.rerun()
    

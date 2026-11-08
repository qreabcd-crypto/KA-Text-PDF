import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Gemini AI", page_icon="🤖", layout="centered")

# API Key Check
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# Initialize Model safely using gemini-1.5-flash
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Model Error: {e}")
    st.stop()

st.title("🤖 Gemini AI Assistant")
st.write("మీకు ఏ ప్రశ్న కావాలన్నా కింద టైప్ చేయండి, క్షణాల్లో సమాధానం వస్తుంది.")

# User Input
user_query = st.text_input("మీ ప్రశ్న ఇక్కడ రాయండి...", key="query")

if st.button("పంపండి (Send)", type="primary"):
    if user_query.strip():
        with st.spinner("బదులు సిద్ధమవుతోంది..."):
            try:
                response = model.generate_content(user_query)
                st.success("సమాధానం:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది: {e}")
    else:
        st.warning("దయచేసి ఏదో ఒకటి టైప్ చేయండి.")
        

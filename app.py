import streamlit as st
import google.generativeai as genai
from PIL import Image

# Streamlit Page Configuration
st.set_page_config(page_title="Ultra Fast Gemini AI", page_icon="⚡", layout="centered")

# Retrieve Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No API key provided. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini Client
genai.configure(api_key=api_key)

# High-Speed Gemini Model setup with fast generation options
generation_config = {
    "temperature": 0.3, # Low temperature for faster & precise output
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel("gemini-3.8-flash", generation_config=generation_config)

st.title("⚡ Ultra Fast Gemini AI Pro")
st.write("అతి వేగంగా టెక్స్ట్, ఇమేజ్ మరియు డ్యాక్యుమెంట్లను అనలైజ్ చేయండి.")

# Language Switcher
language = st.selectbox(
    "భాషను ఎంచుకోండి / Select Language:",
    ["తెలుగు (Telugu)", "English"]
)

# Set system instruction based on language selection
if language == "తెలుగు (Telugu)":
    lang_instruction = "దయచేసి ఎటువంటి అక్షర దోషాలు లేకుండా, శీఘ్రంగా మరియు అత్యంత స్పష్టమైన తెలుగులో సమాధానం ఇవ్వండి."
else:
    lang_instruction = "Please provide fast, highly accurate responses with zero spelling or grammatical errors in English."

# Multi-file Uploader (Images and PDFs)
uploaded_file = st.file_uploader("ఫైల్ అప్‌లోడ్ చేయండి (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

# User Text Input
user_prompt = st.text_area("మీ ప్రశ్న ఇక్కడ టైప్ చేయండి...", height=100, key="prompt_input")

if st.button("⚡ పంపండి (Send)", type="primary"):
    if user_prompt or uploaded_file:
        with st.spinner("రెస్పాన్స్ సిద్ధమవుతోంది..."):
            try:
                full_prompt = f"{lang_instruction}\n\nUser Query: {user_prompt}"
                content_input = [full_prompt]

                if uploaded_file is not None:
                    if uploaded_file.type.startswith("image/"):
                        image = Image.open(uploaded_file)
                        content_input.append(image)
                    elif uploaded_file.type == "application/pdf":
                        # Process PDF using bytes for fast inline processing
                        pdf_data = {
                            "mime_type": "application/pdf",
                            "data": uploaded_file.getvalue()
                        }
                        content_input.append(pdf_data)

                # Fast Gemini API Call
                response = model.generate_content(content_input)
                output_text = response.text

                st.success("రెస్పాన్స్ సిద్ధం!")
                st.markdown(output_text)

                # Download Button for Output Result
                st.download_button(
                    label="📄 రెస్పాన్స్‌ని డౌన్‌లోడ్ చేయండి (Download Output)",
                    data=output_text,
                    file_name="gemini_response.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది: {e}")
    else:
        st.warning("దయచేసి ఏదైనా ఒక ప్రశ్నను టైప్ చేయండి లేదా ఫైల్‌ని అప్‌లోడ్ చేయండి.")
        

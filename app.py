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

# High-Speed Gemini Model setup
generation_config = {
    "temperature": 0.2,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    generation_config=generation_config
)

st.title("⚡ Ultra Fast Gemini AI Pro")
st.write("అతి వేగంగా, క్షణాల్లో సమాధానం పొందండి.")

# Language Switcher
language = st.selectbox(
    "భాషను ఎంచుకోండి / Select Language:",
    ["తెలుగు (Telugu)", "English"],
    key="lang_select"
)

# System Instructions for instant and clear responses
if language == "తెలుగు (Telugu)":
    lang_instruction = (
        "మీరు అత్యంత వేగంగా స్పందించే AI అసిస్టెంట్. యూజర్ కేవలం 'హాయ్' లేదా 'Hi' అంటే, "
        "'నమస్కారం! నేను మీకు ఏవిధంగా సహాయపడగలను?' అని తక్షణమే బదులివ్వండి. "
        "ఇంటర్నెట్ మరియు మీ జ్ఞానాన్ని ఉపయోగించి ప్రతి ప్రశ్నకి ఎటువంటి ఆలస్యం లేకుండా, స్పష్టమైన తెలుగులో సెకన్లలో సమాధానం ఇవ్వండి."
    )
else:
    lang_instruction = (
        "You are an ultra-fast AI assistant. If the user simply says 'Hi', "
        "respond instantly with 'Hello! How can I help you today?'. "
        "Provide lightning-fast, highly accurate responses within seconds."
    )

# File Uploader (Images and PDFs)
uploaded_file = st.file_uploader("ఫైల్ అప్‌లోడ్ చేయండి (JPG, PNG, PDF - ఆప్షనల్)", type=["jpg", "jpeg", "png", "pdf"], key="file_up")

# User Text Input and Send Button
user_prompt = st.text_input("మీ ప్రశ్న ఇక్కడ టైప్ చేయండి...", key="user_query_input")

if st.button("⚡ పంపండి (Send)", type="primary"):
    if user_prompt or uploaded_file:
        with st.spinner("సమాధానం వస్తోంది..."):
            try:
                full_prompt = f"{lang_instruction}\n\nUser Query: {user_prompt}"
                content_input = [full_prompt]

                if uploaded_file is not None:
                    if uploaded_file.type.startswith("image/"):
                        image = Image.open(uploaded_file)
                        content_input.append(image)
                    elif uploaded_file.type == "application/pdf":
                        pdf_data = {
                            "mime_type": "application/pdf",
                            "data": uploaded_file.getvalue()
                        }
                        content_input.append(pdf_data)

                # Generate response instantly
                response = model.generate_content(content_input)
                output_text = response.text

                st.success("సమాధానం:")
                st.markdown(output_text)

                # Download Button for the response
                st.download_button(
                    label="📄 ఈ రెస్పాన్స్‌ని డౌన్‌లోడ్ చేయండి",
                    data=output_text,
                    file_name="gemini_response.txt",
                    mime="text/plain",
                    key="dl_btn"
                )

            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది: {e}")
    else:
        st.warning("దయచేసి ఏదైనా ఒక ప్రశ్నను టైప్ చేయండి లేదా ఫైల్‌ని అప్‌లోడ్ చేయండి.")
        

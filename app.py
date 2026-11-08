import streamlit as st
import google.generativeai as genai
from PIL import Image

# Streamlit Page Configuration
st.set_page_config(page_title="Ultra Fast Gemini AI", page_icon="⚡", layout="centered")

# Hide Streamlit Footer, Header toolbar & "Manage app" button completely
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    .viewerBadge_container__1QSob {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Retrieve Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No API key provided. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini Client
genai.configure(api_key=api_key)

# High-Speed Gemini Model setup with Google Search Grounding Enabled
generation_config = {
    "temperature": 0.2,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    generation_config=generation_config,
    tools=["google_search"]
)

st.title("⚡ Ultra Fast Gemini AI (Live Search)")
st.write("గూగుల్ లాగా లైవ్ వెబ్ సెర్చ్ చేసి క్షణాల్లో సమాధానం పొందండి.")

# Language Switcher
language = st.selectbox(
    "భాషను ఎంచుకోండి / Select Language:",
    ["తెలుగు (Telugu)", "English"],
    key="lang_select"
)

# System Instructions
if language == "తెలుగు (Telugu)":
    lang_instruction = (
        "మీరు చాలా వేగంగా స్పందించే AI అసిస్టెంట్ మరియు అవసరమైనప్పుడు గూగుల్ ద్వారా లైవ్ సమాచారాన్ని వెతికి తెలపగలరు. "
        "యూజర్ కేవలం 'హాయ్' లేదా 'Hi' అంటే, 'నమస్కారం! నేను మీకు ఏవిధంగా సహాయపడగలను?' అని తక్షణమే బదులివ్వండి. "
        "మిగతా ప్రశ్నలకు వెబ్ నుండి తాజా సమాచారాన్ని సేకరించి, ఎటువంటి అక్షర దోషాలు లేకుండా స్పష్టంగా మరియు సెకన్లలో సమాధానం ఇవ్వండి."
    )
else:
    lang_instruction = (
        "You are an ultra-fast AI assistant with live Google Search capabilities. "
        "If the user simply says 'Hi', respond instantly with 'Hello! How can I help you today?'. "
        "For other queries, search the web live and provide lightning-fast, highly accurate responses with zero errors."
    )

# Initialize Chat History in Session State if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File Uploader (Images and PDFs)
uploaded_file = st.file_uploader("ఫైల్ అప్‌లోడ్ చేయండి (JPG, PNG, PDF - ఆప్షనల్)", type=["jpg", "jpeg", "png", "pdf"], key="file_up")

# User Text Input via Streamlit Chat Input for a native mobile experience
if user_prompt := st.chat_input("మీ ప్రశ్న ఇక్కడ టైప్ చేయండి..."):
    # Append user message to state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("లైవ్ వెబ్ సెర్చ్ జరుగుతోంది..."):
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

                # Generate response
                response = model.generate_content(content_input)
                output_text = response.text

                st.markdown(output_text)
                
                # Append assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": output_text})

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
            

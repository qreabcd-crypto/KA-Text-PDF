import streamlit as st
from google import genai
from PIL import Image
import os

st.set_page_config(page_title="Gemini Pro App", page_icon="✨", layout="centered")

st.title("✨ Google Gemini Pro App")
st.write("నమస్కారం! మీ ప్రశ్నలను ఇక్కడ అడగవచ్చు లేదా ఫోటోలను అప్లోడ్ చేయవచ్చు.")

# క్లయింట్ ఇనిషియలైజేషన్
try:
    client = genai.Client()
except Exception as e:
    st.error(f"వినతిని ప్రారంభించడంలో లోపం: {e}")

# చాట్ హిస్టరీ మెమొరీ
if "messages" not in st.session_state:
    st.session_state.messages = []

# పాత మెసేజ్ లు డిస్ప్లే చేయడం
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message and message["image"]:
            st.image(message["image"], width=200)
        st.markdown(message["content"])

# ఇన్‌పుట్ ఫీల్డ్స్
uploaded_file = st.file_uploader("ఫోటో అప్లోడ్ చేయండి (ఆప్షనల్)", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("Gemini ని అడగండి...")

if prompt or uploaded_file:
    user_content = []
    image_pil = None
    
    if uploaded_file:
        image_pil = Image.open(uploaded_file)
        user_content.append(image_pil)
    
    if prompt:
        user_content.append(prompt)
    else:
        user_content.append("ఈ ఫోటోలో ఏముంది? దీని గురించి వివరించండి.")

    # యూజర్ మెసేజ్ చూపించడం
    with st.chat_message("user"):
        if uploaded_file:
            st.image(image_pil, width=200)
        if prompt:
            st.markdown(prompt)
            
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt if prompt else "ఫోటో అటాచ్ చేయబడింది", 
        "image": uploaded_file
    })

    # AI రెస్పాన్స్ జనరేట్ చేయడం
    with st.chat_message("assistant"):
        with st.spinner("యోచిస్తోంది..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_content,
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది: {e}")
                

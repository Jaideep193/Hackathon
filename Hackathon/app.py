import streamlit as st
import mimetypes
import google.generativeai as genai
from PIL import Image
import io
from PIL import Image
from io import BytesIO

import PIL.Image

# ---------- API Setup ----------

API_KEY = "AIzaSyBNh5wWTTShQ13uA_rJyGj0VNHZnHOMQuQ"  
MODEL_ID = "gemini-2.0-flash-001"


genai.configure(api_key=API_KEY)
client = genai.GenerativeModel(model_name=MODEL_ID)

# ---------- Setup Page ----------
def setup_page():
    st.set_page_config(page_title="⚡ AI Chatbot", layout="wide")
    st.header("AI Chatbot using Gemini 2.0 Flash!")
    st.sidebar.header("Options", divider='rainbow')

# ---------- Display Chat History ----------

def display_chat():
    for message in st.session_state["history"]:
        with st.chat_message(message["role"], avatar=message.get("avatar", "")):
            st.markdown(message["content"])

# ---------- Converse with Gemini 2.0 ----------

def converse_with_gemini():
    st.subheader("Chat with Gemini 2.0")
    display_chat()

    prompt = st.chat_input("Enter your question here")

    if prompt:
        st.session_state["history"].append({"role": "user", "content": prompt, "avatar": "🧑"})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        chat = st.session_state["chat"]
        response = chat.send_message(prompt)
        response_text = response.text if response else "Error generating response"

        st.session_state["history"].append({"role": "model", "content": response_text, "avatar": "🤖"})
        with st.chat_message("model", avatar="🤖"):
            st.markdown(response_text)

# ---------- Handle File Upload ----------

def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.read()
    return None

# ---------- Handle PDF Upload ----------

def handle_pdf(uploaded_file):
    st.subheader("Chat with a PDF")
    
    if uploaded_file:
        file_content = handle_file_upload(uploaded_file)  
        mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "application/pdf"

        if file_content:
            chat = client.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [{"mime_type": mime_type, "data": file_content}] 
                    }
                ]
            )

            prompt = st.chat_input("Enter your question here")
            if prompt:
                with st.chat_message("user"):
                    st.write(prompt)

                response = chat.send_message(prompt)
                with st.chat_message("model", avatar="🤖"):
                    st.markdown(response.text)


# ---------- Handle Image Upload  ----------
def handle_image():
    st.subheader("Chat with an Image")
    uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
         # Read file as bytes
        file_content = handle_file_upload(uploaded_file) 
        mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "image/png"

        chat = client.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [{"mime_type": mime_type, "data": file_content}] 
                }
            ]
        )

        prompt = st.chat_input("Ask something about the image...")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)

            response = chat.send_message(prompt)
            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)


# ---------- Handle Audio Upload ----------

def handle_audio():
    st.subheader("Chat with Audio")
    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3'])

    if uploaded_file:
        file_content = handle_file_upload(uploaded_file)  
        mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "audio/wav"

        chat = client.start_chat(
            history=[
                {  
                    "role": "user",  
                    "parts": [{"mime_type": mime_type, "data": file_content}]   
                }
            ]
        )

        prompt = st.chat_input("Ask something about the audio...")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)

            response = chat.send_message(prompt)
            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)


# ---------- Handle Video Upload ----------

def handle_video():
    st.subheader("Chat with Video")
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov'])

    if uploaded_file:
        file_content = handle_file_upload(uploaded_file)  
        mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "video/mp4"

        chat = client.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [{"mime_type": mime_type, "data": file_content}] 
                }
            ]
        )

        prompt = st.chat_input("Ask something about the video...")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)

            response = chat.send_message(prompt)
            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)




# ---------- Get User Choice ----------

def get_choice():
    return st.sidebar.selectbox(
        "Choose an option",
        [
            "Converse with Gemini 2.0",
            "Chat with a PDF",
            "Chat with an image",
            "Chat with audio",
            "Chat with video"
            
        ]
    )

# ---------- Initialize Session ----------

def initialize_session():
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "chat" not in st.session_state:
        st.session_state["chat"] = client.start_chat(history=[])

# ---------- Main Function ----------

def main():
    setup_page()
    initialize_session()
    choice = get_choice()

    if choice == "Converse with Gemini 2.0":
        converse_with_gemini()
    elif choice == "Chat with a PDF":
        handle_pdf(st.file_uploader("Choose a PDF file", type=['pdf']))
    elif choice == "Chat with an image":
        handle_image()
    elif choice == "Chat with audio":
        handle_audio()
    elif choice == "Chat with video":
        handle_video()   

# ---------- Run the App ----------

if __name__ == "__main__":
    main()
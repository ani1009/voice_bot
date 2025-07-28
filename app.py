import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import requests
import os

API_URL = "http://localhost:8000/ask"

DURATION = 10
SAMPLE_RATE = 44100  
FILENAME = "recorded_audio.wav"

# --- Initialize chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Function to record audio ---
def record_audio():
    st.info("🎙️ Recording... Speak now!")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()  
    wav.write(FILENAME, SAMPLE_RATE, audio_data)  
    st.success("✅ Recording complete!")

# --- Function to send audio and get bot response ---
def send_audio():
    if not os.path.exists(FILENAME):
        st.error("No audio file found. Please record first.")
        return None

    files = {"audio": open(FILENAME, "rb")}
    st.info("📤 Sending audio to server...")

    try:
        response = requests.post(API_URL, files=files)
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend is not running. Start FastAPI first.")
        return None

    if response.status_code == 200:
        data = response.json()
        transcription = data.get("transcription", "You (via voice)")
        reply = data.get("reply", "No response received.")

        # Add to history
        st.session_state.history.append((transcription, reply))
        
        st.success("🤖 Bot: " + reply)
        return transcription, reply
    else:
        st.error(f"❌ Failed to process the request. Error: {response.text}")
        return None

# --- Streamlit App UI ---
st.set_page_config(layout="wide")
st.title("🎙️ AI Voice Bot")

st.write("Speak your questions and get responses from the AI assistant!")

# --- Action Buttons ---
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("🎤 Record Audio"):
        record_audio()

    if st.button("📤 Send to AI Bot"):
        send_audio()

    if st.button("🔄 Clear Chat History"):
        st.session_state.history = []
        st.success("🗑️ Chat history cleared.")

# --- Sidebar for Chat History ---
with st.sidebar:
    st.header("🗂️ Chat History")
    if st.session_state.history:
        for i, (user_msg, bot_msg) in enumerate(st.session_state.history, 1):
            st.markdown(f"**🧑 You:** {user_msg}")
            st.markdown(f"**🤖 Bot:** {bot_msg}")
            st.markdown("---")
    else:
        st.write("No conversation yet.")

# --- Main Area for Bot Response (optional if you want to display again)
if st.session_state.history:
    last_user, last_bot = st.session_state.history[-1]
    st.subheader("🔊 Last Exchange")
    st.markdown(f"**🧑 You said:** {last_user}")
    st.markdown(f"**🤖 Bot replied:** {last_bot}")

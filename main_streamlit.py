import streamlit as st
import requests
from datetime import datetime
import time
import random

st.set_page_config(page_title="Tom AI", page_icon="🤖")

# === ONLINE INDICATOR ===
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

col1, col2 = st.columns([4,1])
with col1:
    st.title("🤖 Tom AI")
with col2:
    if check_internet():
        st.success("🟢 Online")
    else:
        st.error("🔴 Offline")

st.caption(f"Last checked: {datetime.now().strftime('%H:%M:%S')}")

# === YOUR CHAT CODE STARTS HERE ===
user_input = st.chat_input("Ask Tom anything...")
if user_input:
    st.chat_message("user").write(user_input)
    
    # === Tom typing animation + WhatsApp double ticks ===
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Typing dots with random pause
        for i in range(3):
            message_placeholder.markdown(f"**Tom is typing{'.' * (i+1)}**")
            time.sleep(random.uniform(0.3, 0.6))
        
        # === YOUR REPLY LOGIC HERE - 100% YOUR CODE ===
        # Replace this with your intent detection + math + handle_responses()
        reply = "Yo, I dey here for you 💪"
        
        # Type out with random speed per character
        full_response = ""
        for char in reply:
            full_response += char
            # WhatsApp blue double ticks at the end
            message_placeholder.markdown(
                f"**Tom:** {full_response} <span style='color: #53bdeb; font-size:16px;'>✓</span>", 
                unsafe_allow_html=True
            )
            
            # Random speed: spaces/punctuation faster, letters slower
            if char in " .,!?":
                time.sleep(random.uniform(0.01, 0.03))
            else:
                time.sleep(random.uniform(0.02, 0.08))

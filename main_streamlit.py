import streamlit as st
import time
import random

st.set_page_config(page_title="Tom AI", page_icon="🤖")

# Online indicator
col1, col2 = st.columns([4,1])
with col1:
    st.title("🤖 Tom AI")
with col2:
    st.markdown("<p style='color:green; font-size:14px;'>● Online</p>", unsafe_allow_html=True)

user_input = st.chat_input("Type a message...")

if user_input:
    st.chat_message("user").write(user_input)
    
    # Tom's response with typing + ticks
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        
        # Typing dots
        for i in range(3):
            msg_placeholder.markdown(f"*Tom is typing{'.' * (i+1)}*")
            time.sleep(0.4)
        
        # Generate reply
        reply = f"You said: {user_input}"  # Replace with your Tom AI logic
        
        # Show reply with blue double ticks like WhatsApp
        msg_placeholder.markdown(f"{reply} <span style='color: #53bdeb; font-size: 16px;'>✓</span>", unsafe_allow_html=True)

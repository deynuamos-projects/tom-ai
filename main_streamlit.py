import streamlit as st
import random
from datetime import date, datetime
import re
from time import strftime
import os
import time
import importlib
from response_lib import get_extra_response
try:
    r = importlib.import_module("responses")
    bot_name = getattr(r, "BOT_NAME", "Tom AI")
except ImportError:
    bot_name = "Tom AI"

# Copy your exact code below, just swap print/input
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "setup_done" not in st.session_state:
    st.session_state.setup_done = False

memory = {}

def clean_name(raw_text):
    text = raw_text.lower().strip()
    prefixes = ["give me the name", "you can call me", "i am known as", "i'm known as", "i'm called", "they call me", "my name is", "call me", "i am", "i'm"]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text.replace(prefix, "", 1).strip()
    junk_words = ["no", "actually", "well", "so", "uh", "umm"]
    words = text.split()
    cleaned_words = [w for w in words if w not in junk_words]
    text = " ".join(cleaned_words)
    return text.title() if text else "Guest"

def type_print(text, delay=0.02):
    placeholder = st.empty()
    full_text = ""

    for char in text:
        full_text += char
        placeholder.markdown(full_text + "▌")
        time.sleep(delay)

    placeholder.markdown(full_text)

def handle_responses(user_input: str) -> str:
    username = st.session_state.username
    response = get_extra_response(user_input, username)
    return response

# Streamlit UI
st.title(f"{bot_name} 🤖")
st.subheader("I can chat, tell time, do math, or tell you about **[Amos Deynu](mailto:deynuamos@gmail.com)**, my brilliant creator! Just ask me anything!😊")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Username setup
if not st.session_state.setup_done:
    st.write(f"Hello! I'm {bot_name}, your friendly AI assistant. What's your name?")
    
    if prompt := st.chat_input("You: "):
        reply = ""
        raw_input = prompt.strip()
        username = clean_name(raw_input)
        
        if len(username) < 2:
            st.warning(f"{bot_name}: That doesn't look like a name. Try again")
        elif len(username) > 20:
            st.warning(f"{bot_name}: Woah😲, that's too long for a name. Try again.")
        elif any(char.isdigit() for char in username):
            st.warning(f"{bot_name}: Names can't contain numbers. Try again.")
        elif any(char in "!@#$%^&*()_+=[]{}|\\;:'\"<>,.?/" for char in username):
            st.warning(f"{bot_name}: Names can't contain special characters. Try again.")
        elif len(username.split()) > 2:
            st.warning(f"{bot_name}: Just give me your first name, not your whole life story!😅")
        else:
            st.session_state.username = username
            st.session_state.setup_done = True
            st.success(f"{bot_name}: Nice to meet you, {username}!")
            time.sleep(0.5)
            st.rerun()
else:
    # Main chat loop
    if prompt := st.chat_input("You: "):
        st.session_state.messages.append({"role": "user", "content": f"You: {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"You: {prompt}")
        
        user_input = prompt.lower().strip()
        
        if user_input in ("exit", "quit", "bye","goodbye", "see you again", "see you later", "talk later", "later", "i have to go", "i gotta go","i need to go", "i must go", "i'm leaving", "i am leaving", "i'm out", "i am out","catch you later", "talk to you later", "good night", "night","good bye"):
            reply = f"{bot_name}: Goodbye, {st.session_state.username}!"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.stop()
        
        # time/date
        now = datetime.now()
        if "time" in user_input or "date" in user_input or "now" in user_input or "day" in user_input or "year" in user_input:
            parts = []
            if "time" in user_input:
                parts.append(f"The time is {now.strftime('%I:%M %p')}")
            if "date" in user_input:
                parts.append(f"Today's date is {now.strftime('%A, %B %d, %Y')}")
            if "year" in user_input:
                parts.append(f"The current year is {now.strftime('%Y')}")
            if "day" in user_input:
                parts.append(f"Today is {now.strftime('%A')}")
            if "now" in user_input:
                parts.append(f"It's {now.strftime('%A, %B %d, %Y at %I:%M %p')}")
            reply = f"{bot_name}: {'; '.join(parts)}"
        
        # math
        elif user_input.startswith("add "):
            cleaned = user_input[4:].replace("and", "").replace("plus", "").strip()
            parts = cleaned.split()
            try:
                if len(parts) == 2:
                    result = float(parts[0]) + float(parts[1])
                    reply = f"{bot_name}: {parts[0]} + {parts[1]} = {result}"
                else:
                    reply = f"{bot_name}: Use: add 5 3 or add 5 and 3"
            except:
                reply = f"{bot_name}: Numbers only. Try add 5 and 3"
        
        elif user_input.startswith("minus "):
            cleaned = user_input[6:].replace("and", "").replace("from", "").strip()
            parts = cleaned.split()
            try:
                if len(parts) == 2:
                    result = float(parts[0]) - float(parts[1])
                    reply = f"{bot_name}: {parts[0]} - {parts[1]} = {result}"
                else:
                    reply = f"{bot_name}: Use: minus 10 3 or minus 10 and 3"
            except:
                reply = f"{bot_name}: Numbers only. Try: minus 10 and 3"
        
        elif user_input.startswith("mul "):
            parts = user_input.split()
            if len(parts) == 3:
                try:
                    result = float(parts[1]) * float(parts[2])
                    reply = f"{bot_name}: {parts[1]} * {parts[2]} = {result}"
                except:
                    reply = f"{bot_name}: Use: mul 3 4"
            else:
                reply = f"{bot_name}: Use: mul 3 4"
        
        elif user_input.startswith("div "):
            parts = user_input.split()
            if len(parts) == 3:
                try:
                    result = float(parts[1]) / float(parts[2])
                    reply = f"{bot_name}: {parts[1]} / {parts[2]} = {result}"
                except:
                    reply = f"{bot_name}: Use: div 20 4"
            else:
                reply = f"{bot_name}: Use: div 20 4"
        
        elif re.match(r'^\s*\d+.*[\+\-\*/].*\d+\s*$', user_input):
            try:
                expr = user_input.replace('\\', '/')
                result = eval(expr, {})
                reply = f"{bot_name}: The result of {expr} = {result}"
            except:
                reply = f"{bot_name}: That doesn't look like a valid math expression. Try again."
        
        else:
            reply = handle_responses(user_input)

            st.session_state.messages.append({"role": "assistant", "content": reply})

with st.chat_message("assistant"):
    placeholder = st.empty()
    full_response = ""

    for char in reply:
        full_response += char
        placeholder.markdown(full_response + "▌")
        time.sleep(0.015)

    placeholder.markdown(full_response)

st.stop()
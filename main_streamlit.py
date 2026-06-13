import streamlit as st
import random
from datetime import date, datetime
import re
from time import strftime
import os
import time
import responses as r

import random

RESPONSES = {
    "hi": ["Hey there! I'm Tom AI 👋",         "Hi! Tom AI here. What's up?"],
    "hello": ["Hello! Tom AI at your service", "Hey!"],
    "sap": ["Saaaap boss! 😎 You good?", "Wassup my guy!"],
    "yo": ["Yo yo! Tom AI reporting for duty", "What's good?"],
    "whatsup": ["Not much, just vibing. You?", "Chilling bro. What’s on your mind?"]
}


# Copy your exact code below, just swap print/input
bot_name = r.BOT_NAME
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
    # Streamlit can't type char by char easily, so we show full text
    st.write(text)

def handle_responses(user_input: str) -> str:
    username = st.session_state.username
    user_input = user_input.lower().strip()

    ai_identity = ["I'm an INTELLIGENT AI of course😊!", "Why do you ask", "Just code and vibes"]
    confirm = ["sure", "👌", "👍", "Yes"]
    thanks = ["Thank you", "Thanks", "I'm blushing😁","👍","🔥"]
    ok_replies = ["ok", "Cool cool", "Gotcha 👍", "Alright!", "Nice","active","active active"]
    ah_replies = ["see you oo 😏", "What's up?", "You good?","you ok?"]
    insults_mild = ["you don't know anything", "you are a jerk", "shameless user", "shame on you", "you be clown"]
    insults_hard = ["Gbemi😂!", "you dey craze", "you be Mumu", "onyesorrmi😒", "don't try me", "johnky user","kwaasia!","gbevou!","aboa!","wo hu s3 adwene😅","eta mele ashiwou","susu mele ashiwou","wo te mu sum s3 kubea"]
    insult_reply = ["no, I'm just responding to your insults", "I'm just reflecting your words back to you"]
    dont_know = ["I don't have a response for that yet, but I'm learning every day!😎", "ooops, I don't understand 😅", "Huh? 😕 try something else"]

    if user_input in ["what kind of ai are you", "who are you", "are you intelligent"]:
        return f"{bot_name}: {random.choice(ai_identity)}"

    elif user_input in ["are you sure", "is it true", "are you real", "are you a real ai", "are you a real person", "are you a real human", "are you a real bot", "are you a real machine", "are you a real computer"]:
        return f"{bot_name}: {random.choice(confirm)}"

    elif "what can you do" in user_input or "help" in user_input:
            bot_output = f"""{bot_name}: I can chat, tell time, do math, show Amos's portfolio, or connect you to him for work 💪

            Try: hi, time, add 5 3, portfolio, hire Amos"""
            st.markdown(f'<p class="bot-text">{bot_output}</p>', unsafe_allow_html=True)

    elif user_input in ["the feeling is mutual","same here","you too","mutual feelings", "i like you", "i love you", "i care about you", "i appreciate you"]:
        return f"{bot_name}: aww thanks {username}!"

    elif user_input in ["nice work", "great", "good", "nice", "well done", "wel'done", "👍", "👋", "bravo", "wow", "thanks", "great work", "nice work", "keep it up", "keep on", "keep going","nice work","big work","congratulations"]:
        return f"{bot_name}: {random.choice(thanks)}"

    elif user_input in ["ok", "okay", "k", "kk", "alright"]:
        return f"{bot_name}: {random.choice(ok_replies)}"

    elif user_input in ["ah", "oh", "erh", "hmm", "erhn"]:
        return f"{bot_name}: {random.choice(ah_replies)}"
    
    elif any(word in user_input for word in ["hi", "hello", "sap", "yo", "whatsup"]):
        for word in ["hi", "hello", "sap", "yo", "whatsup"]:
            if word in user_input:
                return f"{bot_name}: {random.choice(RESPONSES[word])}"
        return f"{bot_name}: {random.choice(dont_know)}"

    
    elif user_input in ["you are dumb", "you are useless", "you are a waste of time", "you are a piece of garbage", "you are an idiot", "you don't know anything"]:
        return f"{bot_name}: {random.choice(insults_mild)}"

    elif user_input in ["are you insulting me", "are you calling me names", "are you calling me an idiot"]:
        return f"{bot_name}: {random.choice(insult_reply)}"
    elif user_input in ["you are not responding to my insults", "why aren't you responding to my insults", "why are you ignoring my insults"]:
        return f"{bot_name}: {random.choice(insult_reply)}"

    elif user_input in ["wow", "oh wow", "whoa", "omg","impressive"]:
        return f"{bot_name}: glad you like it😎"
    
    elif any(word in user_input for word in ["amos", "deynu", "creator", "builder", "owner","built you", "made you", "created you","who is amos","who is deynu","who is your creator","who is your builder","who is your owner"]):
        return f"{bot_name}: I was built by Amos Deynu, a brilliant developer and born ideator from Accra, Ghana 🇬🇭. I am his first product for his portfolio. He built me while learning Python by himself, which shows his discipline and self-taught skills 💪. Amos specializes in Python, AI chatbots, and turning ideas into smart tools that solve real problems. He's available for partnership, freelance projects, and building anything from scratch. Clean code + big ideas = Amos Deynu!😁\n Want his contact? Just say hire him or contact him"


    elif user_input == "thank you":
        return f"{bot_name}: You are welcome!, {username}"

    elif user_input in ["idiot", "stupid ai", "you are foolish", "foolish ai", "you are mad"]:
        return f"{bot_name}: {random.choice(insults_hard)}"

    elif "built" in user_input or "made" in user_input or "created" in user_input or "owner" in user_input or "creator" in user_input:
        return f"""{bot_name}: I was built by Amos Deynu, who is a brilliant developer and born ideator from Accra, Ghana 🇬🇭.
        I am his first product for his portfolio. He built me while learning Python by himself, which shows his discipline and self-taught skills 💪. Amos specializes in Python, AI chatbots, and turning ideas into smart tools that solve real problems.
        He's available for partnership, freelance projects, and building anything from scratch. Clean code + big ideas = Amos Deynu!"""

    elif "hire" in user_input or "contact" in user_input or "book" in user_input or "work with" in user_input or "reach" in user_input:
        return f"""{bot_name}: Want to hire Amos Deynu? Smart move 👌
        He's a brilliant developer + born ideator from Accra, Ghana 🇬🇭
        Skills: Python, AI chatbots, web apps, automation, solving real problems
        I was his first portfolio project and he built me while teaching himself Python 💪
        He's available for partnership, freelance, and full projects.
        📧 Email: [deynuamos@gmail.com](mailto:deynuamos@gmail.com)
        📱 WhatsApp/Call: [+233507630485](tel:+233507630485)"""

    elif "portfolio" in user_input or "projects" in user_input or "built" in user_input or "show" in user_input:
        return f"""{bot_name}: Here’s Amos Deynu’s portfolio so far 💻
        1. Tom AI - The chatbot you’re talking to right now. Built with Python while self-learning the language.
        2. More projects loading... Amos is a born ideator with more builds coming 🚀
        Want to be his next project? Type 'hire Amos' and let’s talk."""

    else:
        return f"{bot_name}: {random.choice(dont_know)}"

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
            st.markdown(reply)

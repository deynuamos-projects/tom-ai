# ==========================================================
# TOM AI - Portfolio Assistant
# Author: Amos Deynu
# Version: 2.0
# ==========================================================

# =========================
# Imports
# =========================

import importlib
import importlib.util
import json
import os
import random
import re
import time
from datetime import datetime

# =========================
# Configuration
# =========================

BOT_NAME = "TOM AI"

# Load custom responses module if available
responses = None

if importlib.util.find_spec("responses") is not None:
    responses = importlib.import_module("responses")
    BOT_NAME = getattr(responses, "BOT_NAME", BOT_NAME)

# Enable UTF-8 terminal on Windows
os.system("chcp 65001 > nul")

# =========================
# Global Variables
# =========================

username = ""
memory = {}
bot_name = BOT_NAME
VISITORS_FILE = os.path.join(os.path.dirname(__file__), "visitors.json")

EXIT_COMMANDS = (
    "exit", "quit", "bye", "goodbye", "see you again", "see you later",
    "talk later", "later", "i have to go", "i gotta go", "i need to go",
    "i must go", "i'm leaving", "i am leaving", "i'm out", "i am out",
    "catch you later", "talk to you later", "good night", "night", "good bye"
)

HELP_PHRASES = (
    "what can you do",
    "help",
    "what do you do",
    "can you help",
    "how can you help",
    "portfolio assistant",
)


def speak(message: str) -> None:
    print(f"{bot_name}: {message}")


def contains_any(text, keywords):
    return any(word in text for word in keywords)


def ensure_visitors_file() -> None:
    if not os.path.exists(VISITORS_FILE):
        with open(VISITORS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=2)


def load_visitors() -> list[str]:
    ensure_visitors_file()
    try:
        with open(VISITORS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def save_visitors(visitors: list[str]) -> None:
    with open(VISITORS_FILE, "w", encoding="utf-8") as file:
        json.dump(visitors, file, indent=2)


def register_visitor(name: str) -> None:
    visitors = load_visitors()
    if name not in visitors:
        visitors.append(name)
        save_visitors(visitors)

# =========================
# Utility Functions
# =========================

def type_print(text: str, delay: float = 0.02):
    """
    Print text with a typing animation.
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def clean_name(raw_text: str) -> str:
    """
    Clean the user's name input.
    """

    text = raw_text.lower().strip()

    prefixes = [
        "give me the name",
        "you can call me",
        "i am known as",
        "i'm known as",
        "i'm called",
        "they call me",
        "my name is",
        "call me",
        "i am",
        "i'm",
    ]

    for prefix in prefixes:
        if text.startswith(prefix):
            text = text.replace(prefix, "", 1).strip()

    junk_words = [
        "no",
        "actually",
        "well",
        "so",
        "uh",
        "umm",
    ]

    words = text.split()

    cleaned = [word for word in words if word not in junk_words]

    text = " ".join(cleaned)

    return text.title() if text else "Guest"


# =========================
# Random Response Library
# =========================

AI_IDENTITY = [
    "I'm an INTELLIGENT AI of course 😊!",
    "Why do you ask?",
    "Just code and vibes."
]

CONFIRM_REPLIES = [
    "Sure.",
    "👌",
    "👍",
    "Yes."
]

THANKS_REPLIES = [
    "Thank you!",
    "Thanks!",
    "I'm blushing 😁",
    "👍",
    "🔥"
]

OK_REPLIES = [
    "Okay.",
    "Cool.",
    "Gotcha 👍",
    "Alright!",
    "Nice!"
]

AH_REPLIES = [
    "See you 😏",
    "What's up?",
    "You good?"
]

INSULTS_MILD = [
    "You don't know anything.",
    "You are a jerk.",
    "Shameless user.",
    "Shame on you.",
    "You be clown."
]

INSULTS_HARD = [
    "Gbemi 😂",
    "You dey craze.",
    "You be mumu.",
    "Onyesorrmi 😒",
    "Don't try me.",
    "Johnky user.",
    "Kwaasia!",
    "Gbevou!",
    "Aboa!",
    "Wo hu sɛ adwene 😅",
    "Eta mele ashiwou.",
    "Susu mele ashiwou.",
    "Wo te mu sum sɛ kubea."
]

INSULT_REPLY = [
    "No, I'm simply responding to your insults.",
    "I'm just reflecting your words back to you."
]

UNKNOWN_REPLY = [
    "I don't have a response for that yet, but I'm learning every day! 😎",
    "Oops... I don't understand that yet. 😅",
    "Huh? 😕 Try asking another way."
]

CREATOR_KEYWORDS = ["built", "made", "created", "creator", "owner", "amos", "deynu"]
HIRE_CONTACT_KEYWORDS = [
    "hire", "contact", "email", "whatsapp", "linkedin", "github",
    "book", "work with", "reach", "repo", "link", "links", "linkdin"
]
PORTFOLIO_KEYWORDS = ["portfolio", "projects", "show projects", "my work", "work"]
PORTFOLIO_ASSISTANT_KEYWORDS = [
    "portfolio assistant", "portfolio help", "build my portfolio",
    "portfolio ideas", "portfolio guidance", "strong portfolio",
    "portfolio advice", "portfolio strategy", "portfolio review",
    "ai portfolio assistant", "portfolio assistant ai"
]
EXPERIENCE_KEYWORDS = ["experience", "background", "career", "work history"]
IDEATOR_KEYWORDS = ["ideator", "hub", "web3"]
SKILLS_KEYWORDS = ["skills", "technologies"]
FEELINGS_TRIGGERS = [
    "the feeling is mutual", "same here", "you too", "mutual feelings",
    "i like you", "i love you", "i care about you", "i appreciate you"
]
GENERIC_THANKS_TRIGGERS = [
    "nice work", "great", "good", "nice", "well done", "wel'done", "👍", "👋",
    "bravo", "thanks", "great work", "keep it up", "keep on", "keep going",
    "big work", "congratulations"
]

# TOM AI's Memory
memory = {}


def handle_responses(user_input: str) -> None:
    global username, bot_name
    normalized = user_input.lower().strip()

    if normalized in ["what kind of ai are you", "who are you", "are you intelligent"]:
        speak(random.choice(AI_IDENTITY))
        return

    if normalized in [
        "are you sure", "is it true", "are you real", "are you a real ai",
        "are you a real person", "are you a real human", "are you a real bot",
        "are you a real machine", "are you a real computer"
    ]:
        speak(random.choice(CONFIRM_REPLIES))
        return

    if normalized in FEELINGS_TRIGGERS:
        speak(f"aww thanks {username}!")
        return

    if any(phrase in normalized for phrase in HELP_PHRASES):
        speak(
            "I can chat, tell time, do math, show Amos's portfolio, or connect you to him for work 💪 "
            "Try: hi, time, add 5 3, portfolio, hire Amos"
        )
        return

    if normalized in GENERIC_THANKS_TRIGGERS:
        speak(random.choice(THANKS_REPLIES))
        return

    if normalized in ["ok", "okay", "k", "kk", "alright"]:
        speak(random.choice(OK_REPLIES))
        return

    if normalized in ["ah", "oh", "erh", "hmm", "erhn"]:
        speak(random.choice(AH_REPLIES))
        return

    if normalized in [
        "you are dumb", "you are useless", "you are a waste of time",
        "you are a piece of garbage", "you are an idiot", "you don't know anything"
    ]:
        speak(random.choice(INSULTS_MILD))
        return

    if normalized in [
        "are you insulting me", "are you calling me names", "are you calling me an idiot",
        "you are not responding to my insults", "why aren't you responding to my insults",
        "why are you ignoring my insults"
    ]:
        speak(random.choice(INSULT_REPLY))
        return

    if normalized in ["wow", "oh wow", "whoa", "omg", "impressive"]:
        speak("glad you like it😎")
        return

    if normalized == "thank you":
        speak(f"You are welcome!, {username}")
        return

    if normalized in ["idiot", "stupid ai", "you are foolish", "foolish ai", "you are mad"]:
        speak(random.choice(INSULTS_HARD))
        return

    if contains_any(normalized, CREATOR_KEYWORDS):
        type_print(
            f"{bot_name}: 👋 I was built by Amos Deynu, a Python Developer, AI Engineer, Prompt Engineer, FastAPI Developer, "
            "Web3 Community Builder, Crypto Educator, and Founder of THE IDEATOR'S HUB.\n\n"
            "Amos is passionate about building AI-powered software, backend systems, automation tools, and "
            "innovative products that solve real-world problems.\n\n"
            "He is currently focused on developing intelligent applications for Ghana and Africa while continuously "
            "expanding his skills in AI, Python, and software engineering.\n\n"
            "Want to know more? Ask about:\n• My projects\n• DEKA AI\n• FootballGame Master\n• Skills\n• Experience\n• Contact"
        )
        return

    if contains_any(normalized, HIRE_CONTACT_KEYWORDS):
        type_print(
            f"{bot_name}: \033[92mWant to hire Amos Deynu? Smart move 👌\n"
            "He's a brilliant developer + born ideator from Accra, Ghana 🇬🇭\n"
            "Skills: Python, AI chatbots, web apps, automation, solving real problems\n"
            "I was his first portfolio project and he built me while teaching himself Python 💪\n"
            "He's available for partnership, freelance, and full projects.\n"
            "📧 Email: \033[94mdeynuamos@gmail.com\033[92m\n"
            "📱 WhatsApp/Call: \033[94m+233507630485\033[92m\n"
            "💼 LinkedIn: \033[94mhttps://www.linkedin.com/in/amos-deynu-4787253b3\033[92m\n"
            "💻 GitHub: \033[94mhttps://github.com/deynuamos-projects\033[0m"
        , 0.02)
        return

    if contains_any(normalized, PORTFOLIO_KEYWORDS):
        type_print(
            f"{bot_name}: 🚀 Amos Deynu's Portfolio\n\n"
            "Amos is a strong AI portfolio assistant focused on helping you present skills, experience, and tech projects clearly.\n\n"
            "He can explain your work in AI, Python, FastAPI, Web3, and automation so recruiters and clients understand your value.\n\n"
            "Current projects include portfolio builders, AI chatbots, and developer tools with a real focus on practical, high-impact outcomes.\n\n"
            "Ask me about the portfolio, projects, or how I can help you build a stronger presence."
        )
        return

    if contains_any(normalized, PORTFOLIO_ASSISTANT_KEYWORDS):
        type_print(
            f"{bot_name}: 💡 As your AI portfolio assistant, I can help you:\n"
            "• Summarize your skills and experience clearly\n"
            "• Explain your projects in simple terms\n"
            "• Highlight why your work matters to employers\n"
            "• Recommend portfolio ideas and next steps\n"
            "• Show how Amos builds AI tools and web apps for real results\n\n"
            "Ask me for portfolio advice, project ideas, or how to make your profile stronger."
        )
        return

    if contains_any(normalized, EXPERIENCE_KEYWORDS):
        type_print(
            f"{bot_name}: 💼 Amos Deynu's Experience\n\n"
            "Amos has worked extensively in Python development, AI engineering, and web application design.\n\n"
            "He builds intelligent software, REST APIs with FastAPI, and AI chatbots that solve real problems.\n\n"
            "His portfolio includes portfolio assistants, simulation projects, and automation tools, with a strong focus on practical, user-centered solutions.\n\n"
            "Amos is also active in crypto education, Web3 community building, and mentoring beginner developers."
        )
        return

    if "deka" in normalized:
        type_print(
            f"{bot_name}: 🇬🇭 DEKA AI\n\n"
            "DEKA AI is Amos Deynu's flagship AI project.\n\n"
            "Current Progress:\n✅ FastAPI Backend\n✅ REST API\n✅ Ghana Knowledge Base\n✅ Semantic Search\n✅ Conversation Memory\n🔄 AI Model Integration\n\n"
            "Future Features:\n• Local language support\n• Translation\n• Voice AI\n• Story generation\n• Poetry generation\n• Authentication\n• Web & Mobile Apps\n• Premium subscription\n\n"
            "Vision:\nTo build Ghana's leading AI ecosystem that understands Ghanaian languages, culture, and everyday needs."
        )
        return

    if "football" in normalized or "soccer" in normalized:
        type_print(
            f"{bot_name}: ⚽ FootballGame Master\n\n"
            "A football simulation game currently in development.\n\n"
            "Current Phase:\n🟡 Phase 2 — Core Match Engine\n\n"
            "Completed:\n✅ Match interface\n✅ Controls\n✅ Scoreboard\n✅ Match timer\n✅ Prototype players\n✅ Prototype ball\n\n"
            "Upcoming Features:\n• Intelligent AI\n• Career Mode\n• Manager Mode\n• Online Multiplayer\n• Team Management\n• Full Football Rules\n• FastAPI Backend\n\n"
            "Vision:\nTo create a realistic football simulation with intelligent gameplay and modern online features."
        )
        return

    if contains_any(normalized, IDEATOR_KEYWORDS):
        type_print(
            f"{bot_name}: 🌍 THE IDEATOR'S HUB\n\n"
            "Founder:\nAmos Deynu\n\n"
            "A growing crypto and Web3 community dedicated to helping beginners learn about:\n\n"
            "• Blockchain\n• Cryptocurrency\n• Mining\n• Trading\n• Web3\n• DeFi\n• Airdrops\n\n"
            "Motto:\nLearn • Mine • Trade • Earn • Grow"
        )
        return

    if contains_any(normalized, SKILLS_KEYWORDS):
        type_print(
            f"{bot_name}: 🛠 Amos Deynu's Skills\n\n"
            "Programming\n• Python\n\n"
            "Backend\n• FastAPI\n• REST APIs\n\n"
            "AI\n• AI Engineering\n• Prompt Engineering\n• Semantic Search\n• AI Chatbots\n\n"
            "Development\n• Streamlit\n• Git\n• GitHub\n\n"
            "Other\n• Graphic Design\n• Video Editing\n• Community Building\n• Crypto Education\n• Web3 Education"
        )
        return

    speak(random.choice(UNKNOWN_REPLY))


def main_loop():
    global username
    now = None
    while True:
        user_input = input(f"You: ").strip()
        if not user_input:
            continue
        if user_input in ("exit", "quit", "bye","goodbye", "see you again", "see you later", "talk later", "later", "i have to go", "i gotta go","i need to go", "i must go", "i'm leaving", "i am leaving", "i'm out", "i am out","catch you later", "talk to you later", "good night", "night","good bye"):
            print(f"{bot_name}: Goodbye, {username}!")
            break

        user_input = user_input.lower()

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
            print(f"{bot_name}: {'; '.join(parts)}")
            continue

        # simple commands: add, minus, mul, div, or math expressions
        if user_input.startswith("add "):
            cleaned = user_input[4:].replace("and", "").replace("plus", "").strip()
            parts = cleaned.split()
            try:
                if len(parts) == 2:
                    result = float(parts[0]) + float(parts[1])
                    print(f"{bot_name}: {parts[0]} + {parts[1]} = {result}")
                else:
                    print(f"{bot_name}: Use: add 5 3 or add 5 and 3")
            except Exception:
                print(f"{bot_name}: Numbers only. Try add 5 and 3")
            continue

        if user_input.startswith("minus "):
            cleaned = user_input[6:].replace("and", "").replace("from", "").strip()
            parts = cleaned.split()
            try:
                if len(parts) == 2:
                    result = float(parts[0]) - float(parts[1])
                    print(f"{bot_name}: {parts[0]} - {parts[1]} = {result}")
                else:
                    print(f"{bot_name}: Use: minus 10 3 or minus 10 and 3")
            except Exception:
                print(f"{bot_name}: Numbers only. Try: minus 10 and 3")
            continue

        if user_input.startswith("mul "):
            parts = user_input.split()
            if len(parts) == 3:
                try:
                    result = float(parts[1]) * float(parts[2])
                    print(f"{bot_name}: {parts[1]} * {parts[2]} = {result}")
                except Exception:
                    print(f"{bot_name}: Use: mul 3 4")
            else:
                print(f"{bot_name}: Use: mul 3 4")
            continue

        if user_input.startswith("div "):
            parts = user_input.split()
            if len(parts) == 3:
                try:
                    result = float(parts[1]) / float(parts[2])
                    print(f"{bot_name}: {parts[1]} / {parts[2]} = {result}")
                except Exception:
                    print(f"{bot_name}: Use: div 20 4")
            else:
                print(f"{bot_name}: Use: div 20 4")
            continue

        if re.match(r'^\s*\d+.*[\+\-\*/].*\d+\s*$', user_input):
            try:
                expr = user_input.replace('\\', '/')
                result = eval(expr, {})
                print(f"{bot_name}: The result of {expr} = {result}")
            except Exception:
                print(f"{bot_name}: That doesn't look like a valid math expression. Try again.")
            continue

        # fallback replies
        handle_responses(user_input)

# === START THE BOT ===
if __name__ == "__main__":
    # Get username first
    print(f"{bot_name}: Hello! I'm {bot_name}, your friendly AI portfolio assistant. What's your name?")
    while len(username) < 2:
        raw_input = input("You: ").strip()
        username = clean_name(raw_input)

        if len(username) < 2:
            print(f"{bot_name}: That doesn't look like a name. Try again")
        elif len(username) > 20:
            print(f"{bot_name}: Woah😲, that's too long for a name. Try again.")
            username = ""
        elif any(char.isdigit() for char in username):
            print(f"{bot_name}: Names can't contain numbers. Try again.")
            username = ""
        elif any(char in "!@#$%^&*()_+=[]{}|\\;:'\"<>,.?/" for char in username):
            print(f"{bot_name}: Names can't contain special characters. Try again.")
            username = ""
        elif len(username.split()) > 2:
            print(f"{bot_name}: Just give me your first name, not your whole life story!😅")
            username = ""
        else:
            register_visitor(username)
            print(f"{bot_name}: Nice to meet you, {username}!")

    main_loop()
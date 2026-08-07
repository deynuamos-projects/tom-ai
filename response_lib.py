"""Response library for the TOM AI bot.

This module centralizes all canned replies and provides a single
function `get_response(user_input: str, username: str) -> str` that
returns the appropriate response string.  It is used by both the
CLI version (main.py) and the Streamlit version (main_streamlit.py).
"""

import random

# -----------------------------------------------------------------
# 1.  Fixed response lists (unchanged from the original code)
# -----------------------------------------------------------------
bot_name = "TOM AI"

ai_identity = ["I'm an INTELLIGENT AI of course😊!", "Why do you ask", "Just code and vibes"]
confirm = ["sure", "👌", "👍", "Yes"]
thanks = ["Thank you", "Thanks", "I'm blushing😁","👍","🔥"]
ok_replies = ["ok", "Cool cool", "Gotcha 👍", "Alright!", "Nice","active","active active"]
ah_replies = ["see you oo 😏", "What's up?", "You good?","you ok?"]
insults_mild = ["you don't know anything", "you are a jerk", "shameless user", "shame on you", "you be clown"]
insults_hard = ["Gbemi😂!", "you dey craze", "you be Mumu", "onyesorrmi😒", "don't try me", "johnky user","kwaasia!","gbevou!","aboa!","wo hu s3 adwene😅","eta mele ashiwou","susu mele ashiwou","wo te mu sum s3 kubea"]

# -----------------------------------------------------------------
# 2.  Fixed messages that need special formatting
# -----------------------------------------------------------------
WOW_MESSAGE = "glad you like it😎"
THANK_MESSAGE = "You are welcome!, {username}"

# -----------------------------------------------------------------
# 3.  Shared response lists used in data‑driven rules
# -----------------------------------------------------------------
insult_reply = [
    "no, I'm just responding to your insults",
    "I'm just reflecting your words back to you"
]

# -----------------------------------------------------------------
# 4.  Core response dispatcher
# -----------------------------------------------------------------
def get_response(user_input: str, username: str) -> str:
    """
    Return the appropriate response for *user_input*.
    The function mirrors the original `handle_responses` logic but
    returns a string instead of printing directly, making it usable
    from both CLI and Streamlit contexts.
    """
    # Normalise input for case‑insensitive matching
    user_input = user_input.lower().strip()

    # -----------------------------------------------------------------
    # Data‑driven rule set – ordered to preserve original precedence
    # -----------------------------------------------------------------
    RESPONSE_RULES = [
        # Identity & introduction
        (["what kind of ai are you", "who are you", "are you intelligent"], ai_identity),
        # Confirmation / certainty
        (["are you sure", "is it true", "are you real", "are you a real ai", "are you a real person",
          "are you a real human", "are you a real bot", "are you a real machine", "are you a real computer"],
         confirm),
        # Appreciation / feelings
        (["the feeling is mutual","same here","you too","mutual feelings", "i like you", "i love you",
          "i care about you", "i appreciate you"], thanks),
        # Nice work / congratulations (uses the same `thanks` list)
        (["nice work", "great", "good", "nice", "well done", "wel'done", "👍", "👋", "bravo", "wow", "thanks",
          "great work", "nice work", "keep it up", "keep on", "keep going","nice work","big work","congratulations"],
         thanks),
        # Simple acknowledgements
        (["ok", "okay", "k", "kk", "alright"], ok_replies),
        (["ah", "oh", "erh", "hmm", "erhn"], ah_replies),
        # Mild insults
        (["you are dumb", "you are useless", "you are a waste of time", "you are a piece of garbage",
          "you are an idiot", "you don't know anything"], insults_mild),
        # Insult‑reply handling (both short and extended triggers)
        (["are you insulting me", "are you calling me names", "are you calling me an idiot"], insult_reply),
        (["you are not responding to my insults", "why aren't you responding to my insults",
          "why are you ignoring my insults"], insult_reply),
        # Fixed‑text responses
        (["wow", "oh wow", "whoa", "omg","impressive"], WOW_MESSAGE),
        (["thank you"], THANK_MESSAGE),
        # Harder insults
        (["idiot", "stupid ai", "you are foolish", "foolish ai", "you are mad"], insults_hard),
    ]

    # -----------------------------------------------------------------
    # Find the first matching rule and emit the appropriate reply
    # -----------------------------------------------------------------
    for triggers, response in RESPONSE_RULES:
        if user_input in triggers:
            # Fixed‑message cases (need formatting or are literal strings)
            if isinstance(response, str):
                if response == WOW_MESSAGE:
                    return f"{bot_name}: {response}"
                elif response == THANK_MESSAGE:
                    return f"{bot_name}: {response.format(username=username)}"
                # No other fixed‑message types are defined
            else:
                # Normal list of possible responses – pick one at random
                return f"{bot_name}: {random.choice(response)}"
            # Once a matching rule has been handled we stop processing
                return

    # -----------------------------------------------------------------
    # Fallback – original `dont_know` behaviour
    # -----------------------------------------------------------------
    dont_know = ["I don't have a response for that yet, but I'm learning every day!😎",
                 "ooops, I don't understand 😅",
                 "Huh? 😕 try something else"]
    return f"{bot_name}: {random.choice(dont_know)}"

# -----------------------------------------------------------------
# 5.  Extra context‑specific replies that were originally embedded
#    in the Streamlit version.  They are placed here so that the
#    CLI and Streamlit versions can share the same logic.
# -----------------------------------------------------------------
def get_extra_response(user_input: str, username: str) -> str:
    """
    Handles the extra branches that were originally inside
    `handle_responses` in `main_streamlit.py`.  This function is
    called from the Streamlit version when the generic dispatcher
    does not match any of the standard rules.
    """
    user_input_lower = user_input.lower().strip()

    # Creator‑related keywords – share Amos Deynu’s story
    creator_keywords = [
        "amos", "deynu", "creator", "builder", "owner",
        "built you", "made you", "created you",
        "who is amos", "who is deynu", "who is your creator",
        "who is your builder", "who is your owner"
    ]
    if any(word in user_input_lower for word in creator_keywords):
        return (f"{bot_name}: I was built by Amos Deynu, a brilliant developer and born ideator "
                f"from Accra, Ghana 🇬🇭. I am his first product for his portfolio. He built me while "
                f"learning Python by himself, which shows his discipline and self‑taught skills 💪. "
                f"Amos specializes in Python, AI chatbots, and turning ideas into smart tools that "
                f"solve real problems. He's available for partnership, freelance projects, and "
                f"building anything from scratch. Clean code + big ideas = Amos Deynu!😁")

    # Hire / contact / portfolio branches
    if "hire" in user_input_lower or "contact" in user_input_lower or "book" in user_input_lower \
            or "work with" in user_input_lower or "reach" in user_input_lower:
        return (f"{bot_name}: Want to hire Amos Deynu? Smart move 👌\n"
                f"He's a brilliant developer + born ideator from Accra, Ghana 🇬🇭\n"
                f"Skills: Python, AI chatbots, web apps, automation, solving real problems\n"
                f"I was his first portfolio project and he built me while teaching himself Python 💪\n"
                f"He's available for partnership, freelance, and full projects.\n"
                f"📧 Email: [deynuamos@gmail.com](mailto:deynuamos@gmail.com)\n"
                f"📱 WhatsApp/Call: [+233507630485](tel:+233507630485)")

    if any(keyword in user_input_lower for keyword in [
    "portfolio",
    "projects",
    "current projects",
    "my projects",
    "show projects",
    "show portfolio",
    "what have you built",
    "current project"
]):

     return f"""{bot_name}: 🚀 Amos Deynu's Portfolio

1️⃣ TOM AI
🤖 AI Portfolio Assistant
Status: ✅ Completed

Description:
A conversational AI assistant built with Python to showcase Amos Deynu's portfolio, skills, and projects.

━━━━━━━━━━━━━━━━━━━━

2️⃣ DEKA AI
🇬🇭 Ghana Knowledge AI
Status: 🟡 In Development

Description:
An AI platform focused on Ghana's culture, history, regions, education, tourism, and local knowledge using FastAPI and Semantic Search.

━━━━━━━━━━━━━━━━━━━━

3️⃣ FootballGame Master
⚽ Football Simulation Game
Status: 🟡 In Development

Description:
A football management and simulation game featuring match engine, career mode, AI opponents, and multiplayer.

━━━━━━━━━━━━━━━━━━━━

4️⃣ Python Calculator
🧮 Status: ✅ Completed

━━━━━━━━━━━━━━━━━━━━

5️⃣ Python Guess Game
🎮 Status: ✅ Completed

━━━━━━━━━━━━━━━━━━━━

6️⃣ THE IDEATOR'S HUB
🌍 AI • Web3 • Innovation Community

Mission:
Helping people turn their ideas into reality through AI, Python, Web3, and innovative solutions.

Type:
• deka
• football
• skills
• contact
• hire amos

to learn more.
"""

    # Thank‑you handling (fallback to generic thank‑you if not caught earlier)
    if user_input_lower == "thank you":
        return f"{bot_name}: You are welcome!, {username}"

    # Hard insults (fallback)
    if user_input_lower in ["idiot", "stupid ai", "you are foolish", "foolish ai", "you are mad"]:
        return f"{bot_name}: {random.choice(insults_hard)}"

    # If nothing matched, fall back to the generic dispatcher
    return get_response(user_input, username)
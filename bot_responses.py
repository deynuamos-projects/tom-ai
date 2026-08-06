import random

# Bot identity and response lists
bot_name = "TOM AI"
ai_identity = ["I'm an INTELLIGENT AI of course😊!", "Why do you ask", "Just code and vibes"]
confirm = ["sure", "👌", "👍", "Yes"]
thanks = ["Thank you", "Thanks", "I'm blushing😁","👍","🔥"]
ok_replies = ["ok", "Cool cool", "Gotcha 👍", "Alright!", "Nice","active","active active"]
ah_replies = ["see you oo 😏", "What's up?", "You good?","you ok?"]
insults_mild = ["you don't know anything", "you are a jerk", "shameless user", "shame on you", "you be clown"]
insults_hard = ["Gbemi😂!", "you dey craze", "you be Mumu", "onyesorrmi😒", "don't try me", "johnky user","kwaasia!","gbevou!","aboa!","wo hu s3 adwene😅","eta mele ashiwou","susu mele ashiwou","wo te mu sum s3 kubea"]

# Fixed messages that need special formatting
WOW_MESSAGE = "glad you like it😎"
THANK_MESSAGE = "You are welcome!, {username}"

# Response lists used in the data‑driven rules
insult_reply = [
    "no, I'm just responding to your insults",
    "I'm just reflecting your words back to you"
]

def handle_responses(user_input: str, username: str) -> None:
    """
    Dispatches canned replies based on the user's input.
    The logic is now data‑driven: each rule maps a set of triggers to
    either a list of possible responses or a fixed message.
    All original behaviour is preserved.
    """
    # Convert to lower case once for case‑insensitive matching
    user_input = user_input.lower().strip()

    # -----------------------------------------------------------------
    # Data‑driven response rules (ordered to match the original sequence)
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
                    print(f"{bot_name}: {response}")
                elif response == THANK_MESSAGE:
                    print(f"{bot_name}: {response.format(username=username)}")
                # No other fixed‑message types are defined
            else:
                # Normal list of possible responses – pick one at random
                print(f"{bot_name}: {random.choice(response)}")
            # Once a matching rule has been handled we stop processing
            return

    # -----------------------------------------------------------------
    # Fallback – this mirrors the original `dont_know` behaviour
    # -----------------------------------------------------------------
    dont_know = ["I don't have a response for that yet, but I'm learning every day!😎",
                 "ooops, I don't understand 😅",
                 "Huh? 😕 try something else"]
    print(f"{bot_name}: {random.choice(dont_know)}")
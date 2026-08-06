import time
import random

def type_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # new line at end

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
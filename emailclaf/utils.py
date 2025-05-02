import re

def mask_email(text):
    return re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[email]", text)

def mask_phone(text):
    return re.sub(r"\b\d{10}\b", "[phone_number]", text)

def mask_text(text):
    text = mask_email(text)
    text = mask_phone(text)
    return text



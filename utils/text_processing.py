# utils/text_processing.py
# Can contain functions for cleaning/preprocessing text from the reviews.

import re
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()
    return text



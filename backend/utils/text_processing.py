# # utils/text_processing.py
import os
import re
import string
import pickle
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


import nltk.data
punkt_path = nltk.data.find("tokenizers/punkt/english.pickle")

with open(punkt_path, "rb") as f:
    punkt_tokenizer = pickle.load(f)


def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

def clean_markdown(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[[^\]]]*]\([^)]*\)', '', text)
    text = re.sub(r'[*_`#>|-]', '', text)
    return text

def clean_text(text):
    text = clean_html(text)
    text = clean_markdown(text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    sentences = punkt_tokenizer.tokenize(text)
    tokens = []
    for sent in sentences:
        tokens.extend(word_tokenize(sent, language='english', preserve_line=True))


    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalpha()]
    return ' '.join(tokens)

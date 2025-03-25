# utils/text_processing.py

import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# 首次运行的话要下载这些：
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

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
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation

    # Tokenize, lemmatize, remove stopwords
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalpha()]
    return ' '.join(tokens)

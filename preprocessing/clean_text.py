import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load("fr_core_news_sm")
stop_words = set(stopwords.words('french'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    tokens = word_tokenize(text, language='french')
    return [word for word in tokens if word not in stop_words]

def lemmatize(tokens):
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

"""FAQ matching engine: NLTK preprocessing + TF-IDF + cosine similarity."""
import json
import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

for pkg, path in [("punkt", "tokenizers/punkt"), ("punkt_tab", "tokenizers/punkt_tab"),
                  ("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

_STOP = set(stopwords.words("english"))
_LEM = WordNetLemmatizer()

GREETINGS = {"hi", "hello", "hey", "good morning", "good evening"}
FALLBACK = "Sorry, I couldn't find an answer to that. Please try rephrasing or contact support@example.com."


# Simple synonym normalisation so paraphrases map to the same words as the FAQs
PHRASES = {"money back": "refund", "get my money": "refund", "send back": "return"}
SYNONYMS = {"package": "order", "parcel": "order", "abroad": "international", "overseas": "international",
            "ship": "shipping", "delivery": "shipping", "deliver": "shipping", "pay": "payment",
            "cost": "price", "charge": "price", "helpline": "support", "reach": "contact",
            "guarantee": "warranty", "voucher": "coupon", "promo": "coupon", "login": "password"}


def preprocess(text: str) -> str:
    """Lowercase -> strip punctuation -> synonyms -> tokenize -> remove stopwords -> lemmatize."""
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    for phrase, repl in PHRASES.items():
        text = text.replace(phrase, repl)
    tokens = [_LEM.lemmatize(t) for t in word_tokenize(text) if t not in _STOP]
    return " ".join(SYNONYMS.get(t, t) for t in tokens)


class FAQBot:
    def __init__(self, faq_path="data/faqs.json", threshold=0.2):
        self.faqs = json.loads(Path(faq_path).read_text(encoding="utf-8"))
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        corpus = [preprocess(f["question"] + " " + f["answer"]) for f in self.faqs]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def get_answer(self, user_input: str):
        """Return (answer, matched_question, score)."""
        if user_input.strip().lower() in GREETINGS:
            return "Hello! 👋 Ask me anything about shipping, returns, payments or your account.", None, 1.0
        cleaned = preprocess(user_input)
        if not cleaned:
            return FALLBACK, None, 0.0
        scores = cosine_similarity(self.vectorizer.transform([cleaned]), self.matrix)[0]
        best = int(scores.argmax())
        if scores[best] < self.threshold:
            return FALLBACK, None, float(scores[best])
        return self.faqs[best]["answer"], self.faqs[best]["question"], float(scores[best])

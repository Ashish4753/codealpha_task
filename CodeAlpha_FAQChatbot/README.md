# 🤖 FAQ Chatbot — CodeAlpha AI Internship (Task 2)

A chatbot that answers customer FAQs by finding the most similar stored question.

## How it works
1. FAQs are stored in `data/faqs.json`.
2. Text is preprocessed with **NLTK** (lowercase, tokenize, stop-word removal, lemmatization).
3. Questions are converted to **TF-IDF** vectors (unigrams + bigrams).
4. The user's message is compared to every FAQ using **cosine similarity**.
5. The best match is returned; if the score is below a threshold, a fallback reply is shown.

## Features
- Streamlit chat UI + terminal version (`cli.py`)
- Greeting handling and fallback answer
- Easy to customise: just edit `data/faqs.json`

## Run Locally
```bash
git clone https://github.com/<your-username>/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
pip install -r requirements.txt
streamlit run app.py      # web UI
python cli.py             # terminal
```

## Author
Your Name · [LinkedIn](https://linkedin.com/in/your-profile)

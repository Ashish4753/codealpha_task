"""Terminal version of the chatbot."""
from chatbot import FAQBot

bot = FAQBot("data/faqs.json")
print("FAQ Bot (type 'quit' to exit)")
while (q := input("You: ").strip()).lower() not in {"quit", "exit"}:
    print("Bot:", bot.get_answer(q)[0])

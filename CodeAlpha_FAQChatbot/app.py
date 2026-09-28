"""CodeAlpha Task 2 - FAQ Chatbot UI (Streamlit)."""
import streamlit as st
from chatbot import FAQBot

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖")
st.title("🤖 FAQ Chatbot")
st.caption("CodeAlpha AI Internship - Task 2")


@st.cache_resource
def load_bot():
    return FAQBot("data/faqs.json")


bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me about shipping, returns, payments or support."}
    ]

with st.sidebar:
    st.header("Sample questions")
    for f in bot.faqs[:6]:
        st.write("•", f["question"])
    if st.button("Clear chat"):
        st.session_state.pop("messages")
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    answer, matched, score = bot.get_answer(prompt)
    with st.chat_message("assistant"):
        st.write(answer)
        if matched:
            st.caption(f"Matched: “{matched}” (similarity {score:.2f})")
    st.session_state.messages.append({"role": "assistant", "content": answer})

"""CodeAlpha Task 1 - Language Translation Tool (Streamlit + deep-translator).

Full-screen colourful UI, 130+ languages, multi-language output, swap, TTS, history.
"""
import html
import io

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from gtts.lang import tts_langs

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="wide")

# ---------- styling ----------
st.markdown(
    """
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background: linear-gradient(135deg,#4facfe 0%,#7f5af0 45%,#ff6ec7 100%); background-attachment: fixed;}
.block-container {max-width: 100% !important; padding: 1.5rem 3rem 3rem 3rem;}
.hero {background: linear-gradient(90deg,#ff512f,#dd2476); color:#fff; padding: 1.6rem 2rem;
       border-radius: 22px; margin-bottom: 1.2rem; box-shadow: 0 10px 30px rgba(0,0,0,.25);}
.hero h1 {margin:0; font-size: 2.4rem; color:#fff;}
.hero p {margin:.3rem 0 0; opacity:.95; font-size:1.05rem;}
.panel {background: rgba(255,255,255,.95); border-radius: 20px; padding: 1.2rem 1.5rem 1rem; margin-bottom:1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,.18);}
.panel h3 {margin:0 0 .5rem; color:#4c1d95;}
div.stButton > button {border-radius: 14px; font-weight: 600; border: none; padding:.55rem 1.4rem;
       background: linear-gradient(90deg,#00c6ff,#0072ff); color:#fff;}
div.stButton > button:hover {filter: brightness(1.1); color:#fff;}
div.stButton > button[kind="primary"] {background: linear-gradient(90deg,#f7971e,#ff512f); font-size:1.1rem;}
.stTextArea textarea {border-radius: 14px; font-size: 1.1rem; background:#fff7ed;}
.chip {display:inline-block; color:#fff; padding:.25rem .9rem; border-radius:999px; font-weight:600; margin-bottom:.4rem;}
.stat {color:#fff; font-weight:600; text-shadow: 0 1px 3px rgba(0,0,0,.4);}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>🌐 Language Translation Tool</h1>'
    "<p>Translate text into 130+ languages instantly · CodeAlpha AI Internship – Task 1</p></div>",
    unsafe_allow_html=True,
)

# ---------- data ----------
LANGS = GoogleTranslator().get_supported_languages(as_dict=True)  # {'english': 'en', ...}
NAMES = sorted(LANGS)
TTS = tts_langs()
COLORS = ["#ff512f", "#11998e", "#7f00ff", "#f7971e", "#00b4db", "#e91e63", "#43a047", "#5c6bc0"]
label = lambda n: n.title()

st.session_state.setdefault("src", "auto detect")
st.session_state.setdefault("tgt", "hindi")
st.session_state.setdefault("history", [])


def swap():
    if st.session_state.src != "auto detect":
        st.session_state.src, st.session_state.tgt = st.session_state.tgt, st.session_state.src


def translate(text, src, tgt):
    return GoogleTranslator(source=src, target=tgt).translate(text)


# ---------- controls ----------
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="panel"><h3>✍️ Your text</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([5, 1, 5])
    c1.selectbox("From", ["auto detect"] + NAMES, key="src", format_func=label)
    c2.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
    c2.button("⇄", on_click=swap, help="Swap languages")
    c3.selectbox("To", NAMES, key="tgt", format_func=label)
    extra = st.multiselect("➕ Also translate into (optional, pick as many as you like)", NAMES,
                           format_func=label)
    text = st.text_area("Enter text", height=220, max_chars=5000,
                        placeholder="Type or paste text here...", label_visibility="collapsed")
    st.markdown(f"<span style='color:#6b7280'>{len(text)} / 5000 characters</span></div>",
                unsafe_allow_html=True)
    go = st.button("🚀 Translate", type="primary", use_container_width=True)

with right:
    st.markdown('<div class="panel"><h3>🌍 Languages available</h3>', unsafe_allow_html=True)
    st.markdown(f"**{len(NAMES)}** languages supported · **{len(TTS)}** with voice playback")
    st.caption("Tip: choose several languages in “Also translate into” to get every result at once.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>🕘 Recent translations</h3>', unsafe_allow_html=True)
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f"<small><b>{html.escape(h[0])}</b> → {html.escape(h[1][:60])}</small>",
                        unsafe_allow_html=True)
    else:
        st.caption("Nothing yet. Your translations will show up here.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- translate ----------
if go:
    if not text.strip():
        st.warning("Enter some text to translate.")
    else:
        src = "auto" if st.session_state.src == "auto detect" else LANGS[st.session_state.src]
        targets = [st.session_state.tgt] + [t for t in extra if t != st.session_state.tgt]
        results = {}
        with st.spinner("Translating..."):
            for t in targets:
                try:
                    results[t] = translate(text, src, LANGS[t])
                except Exception as e:
                    results[t] = f"⚠️ Translation failed: {e}"
        st.session_state["results"] = results
        st.session_state.history.append((label(st.session_state.tgt), results[targets[0]]))

# ---------- output ----------
results = st.session_state.get("results")
if results:
    st.markdown(f"<p class='stat'>✅ {len(results)} translation(s)</p>", unsafe_allow_html=True)
    cols = st.columns(2 if len(results) > 1 else 1, gap="large")
    for i, (lang, out) in enumerate(results.items()):
        with cols[i % len(cols)]:
            color = COLORS[i % len(COLORS)]
            st.markdown(
                f'<div class="panel" style="border-top:8px solid {color}">'
                f'<span class="chip" style="background:{color}">{label(lang)}</span>',
                unsafe_allow_html=True,
            )
            st.code(out, language=None, wrap_lines=True)  # hover -> copy icon
            code = LANGS[lang]
            if code in TTS and not out.startswith("⚠️"):
                if st.button("🔊 Listen", key=f"tts_{lang}"):
                    try:
                        buf = io.BytesIO()
                        gTTS(out, lang=code).write_to_fp(buf)
                        st.audio(buf.getvalue(), format="audio/mp3")
                    except Exception as e:
                        st.info(f"Voice playback failed: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

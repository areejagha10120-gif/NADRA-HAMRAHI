# -*- coding: utf-8 -*-
"""
NADRA HAMRAHI: Streamlit PROTOTYPE.

This file is only for previewing how the product looks and works. The real
app is planned in Next.js + Supabase + Groq (see README.md).

How it is organised
  content.py  all text and data (English + Urdu)
  ai.py       privacy masking, snippet search, Groq streaming
  styles.py   the visual design (CSS)
  app.py      pages, navigation and the single chat page  <-- you are here

Key idea: every card on every page leads to ONE assistant page. The topic and
the card's question are stored in session_state, and the assistant page sends
that question automatically.
"""
import html
import os
import re
import time

import streamlit as st

from ai import (DEFAULT_MODEL, FALLBACK_MODEL, build_messages, collect_sources,
                mask_ids, retrieve, stream_answer, transcribe_audio)
from content import (ABOUT, CNIC_OPTIONS, CONTACT, GREETING, HOW_STEPS, KB,
                     POPULAR, PROBLEMS, SERVICE_GROUPS, SERVICES, TICKER, TOPICS, UI)
from styles import HERO_SVG, build_css

try:  # optional: only needed for the voice-input button
    from streamlit_mic_recorder import mic_recorder
    HAS_MIC = True
except ImportError:
    HAS_MIC = False

st.set_page_config(
    page_title="NADRA HAMRAHI",
    page_icon="favicon.png" if os.path.exists("favicon.png") else None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

MAX_AI_PER_SESSION = 15  # protects the free Groq quota during the prototype
NAV_KEYS = ["home", "cnic", "services", "assistant", "how", "about"]
NAV_LABEL_KEYS = {
    "home": "nav_home", "cnic": "nav_cnic", "services": "nav_services",
    "assistant": "nav_assistant", "how": "nav_how", "about": "nav_about",
}

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
for _key, _value in {
    "nav": "home",            # current page (bound to the top navigation)
    "lang": "en",             # website language (bound to the EN | اردو toggle)
    "messages": [],           # chat history: {"role", "content", "sources"}
    "topic": None,            # slug of the current topic, or None
    "pending": None,          # question waiting to be sent automatically
    "pending_kind": "free",   # "curated" = pre-written answer, "free" = AI
    "ai_count": 0,
}.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value


def cur_lang():
    return st.session_state.get("lang", "en")


def t(key):
    return UI[cur_lang()][key]


# ---------------------------------------------------------------------------
# Settings (Groq key comes from Streamlit secrets or an environment variable)
# ---------------------------------------------------------------------------
def get_secret(name, default=None):
    try:
        value = st.secrets[name]
    except Exception:
        value = os.environ.get(name)
    return value or default


def get_models():
    primary = get_secret("GROQ_MODEL", DEFAULT_MODEL)
    return [primary] if primary == FALLBACK_MODEL else [primary, FALLBACK_MODEL]


# ---------------------------------------------------------------------------
# Callbacks: they run BEFORE the page redraws, so they can change the page
# ---------------------------------------------------------------------------
def go_to_assistant():
    """Hero's primary button: open the chat with no fixed topic."""
    st.session_state.topic = None
    st.session_state.messages = []
    st.session_state.nav = "assistant"


def go_to_how():
    st.session_state.nav = "how"


def open_topic(slug):
    """A card was clicked: start a fresh chat on this topic."""
    topic = TOPICS[slug]
    question = topic.get("question")
    st.session_state.topic = slug
    st.session_state.messages = []
    st.session_state.pending = question[cur_lang()] if question else None
    st.session_state.pending_kind = "curated" if topic.get("answer") else "free"
    st.session_state.nav = "assistant"


def ask_free(text, topic=None):
    text = (text or "").strip()
    if not text:
        return
    st.session_state.topic = topic
    st.session_state.messages = []
    st.session_state.pending = text
    st.session_state.pending_kind = "free"
    st.session_state.nav = "assistant"


def ask_from_hero():
    ask_free(st.session_state.get("hero_q", ""))


def ask_about_service(key):
    service = next(s for s in SERVICES if s["key"] == key)
    ask_free(service["question"][cur_lang()], service.get("topic"))


def ask_chip(text):
    st.session_state.pending = text
    st.session_state.pending_kind = "free"


def clear_topic():
    st.session_state.topic = None


# ---------------------------------------------------------------------------
# Small HTML helpers
# ---------------------------------------------------------------------------
def sec_title(title, sub=None, align="center"):
    out = '<div class="sec-wrap {}"><div class="sec-title">{}</div>'.format(
        "" if align == "center" else "left", html.escape(title)
    )
    if sub:
        out += '<div class="sec-sub">{}</div>'.format(html.escape(sub))
    out += "</div>"
    st.markdown(out, unsafe_allow_html=True)


def sources_html(sources):
    if not sources:
        return ""
    kind_label = {"official": t("src_official"), "news": t("src_news"), "web": t("src_web")}
    parts = []
    for label, url, kind in sources:
        parts.append(
            '<a href="{u}" target="_blank" rel="noopener noreferrer">{l}</a>'
            '<span class="tag {k}">{n}</span>'.format(
                u=html.escape(url, quote=True), l=html.escape(label), k=kind, n=kind_label[kind]
            )
        )
    return '<div class="src"><b>{}:</b> {}</div>'.format(t("src_title"), "".join(parts))


def fake_stream(text):
    """Types a pre-written answer word by word, like the AI would."""
    for token in re.split(r"(\s+)", text):
        yield token
        if token.strip():
            time.sleep(0.012)


# ---------------------------------------------------------------------------
# Page frame: top bar and footer
# ---------------------------------------------------------------------------
BRAND_MARK = (
    '<div class="brand-mark"><div class="brand-badge">'
    '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4 12l5 5L20 6" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg></div><span class="brand-text">{}</span></div>'
)


def render_topbar():
    with st.container(key="topbar"):
        c_brand, c_nav, c_lang = st.columns([2.3, 6.2, 1.9], vertical_alignment="center")
        with c_brand:
            st.markdown(BRAND_MARK.format(html.escape(t("brand"))), unsafe_allow_html=True)
        with c_nav:
            st.radio(
                "Navigation", NAV_KEYS, key="nav", horizontal=True,
                format_func=lambda k: UI[cur_lang()][NAV_LABEL_KEYS[k]],
                label_visibility="collapsed",
            )
        with c_lang:
            st.radio(
                "Language", ["en", "ur"], key="lang", horizontal=True,
                format_func=lambda k: {"en": "English", "ur": "اردو"}[k],
                label_visibility="collapsed",
            )


def render_footer():
    items = [
        (t("contact_mobile"), CONTACT["mobile"]),
        (t("contact_landline"), CONTACT["landline"]),
        (t("contact_email"), CONTACT["email"]),
        (t("contact_web"), CONTACT["web"]),
    ]
    grid = "".join(
        '<div class="foot-item"><small>{}</small><strong dir="ltr">{}</strong></div>'.format(
            html.escape(label), html.escape(value)
        )
        for label, value in items
    )
    st.markdown(
        '<div class="foot"><div class="foot-title">{}</div><div class="foot-grid">{}</div>'
        '<div class="foot-note">{}</div></div>'.format(t("contact_title"), grid, t("disclaimer")),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def hero_title_html(title):
    """Split the headline so the last word becomes the green accent line,
    the same treatment nadra.gov.pk uses ('Empowerment through / Identity')."""
    words = title.rsplit(" ", 1)
    if len(words) == 2:
        return "{}<span class=\"accent\">{}</span>".format(html.escape(words[0] + " "), html.escape(words[1]))
    return "<span class=\"accent\">{}</span>".format(html.escape(title))


def page_home():
    lang = cur_lang()
    with st.container(key="hero"):
        c_text, c_art = st.columns([1.15, 0.85], vertical_alignment="center")
        with c_text:
            st.markdown(
                '<h1 class="hero-title">{}</h1><p class="hero-sub">{}</p>'.format(
                    hero_title_html(t("hero_title")), html.escape(t("hero_sub"))
                ),
                unsafe_allow_html=True,
            )
            with st.container(key="hero_form"):
                with st.form("hero_form_inner", clear_on_submit=True):
                    c_input, c_btn = st.columns([5, 1.4])
                    with c_input:
                        st.text_input("Question", key="hero_q", placeholder=t("ask_ph"),
                                      label_visibility="collapsed")
                    with c_btn:
                        st.form_submit_button(t("ask_btn"), on_click=ask_from_hero)
            with st.container(key="hero_pills"):
                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    st.button(t("nav_assistant"), key="hero_ask", on_click=go_to_assistant)
                with c_p2:
                    st.button(t("nav_how"), key="hero_how", on_click=go_to_how)
        with c_art:
            st.markdown('<div class="hero-art">{}</div>'.format(HERO_SVG), unsafe_allow_html=True)

    with st.container(key="ticker"):
        spans = "".join("<span>{}</span>".format(html.escape(item)) for item in TICKER[lang] * 2)
        st.markdown(
            '<div class="ticker-wrap"><div class="ticker-track">{}</div></div>'.format(spans),
            unsafe_allow_html=True,
        )

    sec_title(t("popular_title"), t("popular_sub"))
    with st.container(key="popular"):
        cols = st.columns(2)
        for i, (slug, label) in enumerate(POPULAR):
            with cols[i % 2]:
                st.button(label[lang], key="pop_" + slug, on_click=open_topic, args=(slug,))

    sec_title(t("problems_title"), t("problems_sub"))
    with st.container(key="tiles-problems"):
        cols = st.columns(3)
        for i, (slug, label, icon) in enumerate(PROBLEMS):
            with cols[i % 3]:
                st.button(label[lang], key="prob_" + slug, icon=icon,
                          on_click=open_topic, args=(slug,))


def page_cnic():
    lang = cur_lang()
    sec_title(t("cnic_title"), t("cnic_sub"))
    with st.container(key="tiles-cnic"):
        cols = st.columns(3)
        for i, (slug, label, icon) in enumerate(CNIC_OPTIONS):
            with cols[i % 3]:
                st.button(label[lang], key="cnic_" + slug, icon=icon,
                          on_click=open_topic, args=(slug,))


def page_services():
    lang = cur_lang()
    sec_title(t("services_title"), t("services_sub"))
    for group_key, group_name in SERVICE_GROUPS.items():
        items = [s for s in SERVICES if s["group"] == group_key]
        if not items:
            continue
        st.markdown('<div class="follow-title">{}</div>'.format(html.escape(group_name[lang])),
                    unsafe_allow_html=True)
        cols = st.columns(2)
        for i, service in enumerate(items):
            with cols[i % 2]:
                with st.container(key="svc-" + service["key"]):
                    st.markdown(
                        '<div class="svc-name">{}</div><div class="svc-blurb">{}</div>'.format(
                            html.escape(service["name"][lang]), html.escape(service["blurb"][lang])
                        ),
                        unsafe_allow_html=True,
                    )
                    st.button(t("ask_about"), key="ask_" + service["key"],
                              on_click=ask_about_service, args=(service["key"],))


def render_message(message):
    with st.chat_message(message["role"]):  # "user"/"assistant" get Streamlit's built-in icons
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown(sources_html(message["sources"]), unsafe_allow_html=True)


def ai_answer(question, lang):
    """Free-text question: find snippets, then ask Groq (or show the best snippet in demo mode)."""
    slug = st.session_state.topic
    topic = TOPICS.get(slug) if slug else None
    hits = retrieve(question, slug, KB, k=3)
    sources = collect_sources(hits)
    api_key = get_secret("GROQ_API_KEY")

    if not api_key:  # demo mode: no AI, show the closest saved information
        st.caption(t("demo_notice"))
        if hits:
            best = hits[0]["text"]
            text = best.get(lang) or best["en"]
        else:
            text, sources = t("no_info"), []
        st.markdown(text)
        return text, sources

    if st.session_state.ai_count >= MAX_AI_PER_SESSION:
        st.markdown(t("limit_msg"))
        return t("limit_msg"), []

    st.session_state.ai_count += 1
    messages = build_messages(
        st.session_state.messages, hits, topic["title"]["en"] if topic else None, lang
    )
    try:
        text = st.write_stream(stream_answer(api_key, get_models(), messages))
    except Exception:
        text = ""
    if not text or not str(text).strip():
        text, sources = t("busy_msg"), []
        st.markdown(text)
    return str(text), sources


def answer_pending():
    """Send the waiting question (card click, chip, or typed text) and show the answer."""
    question = st.session_state.pending
    if not question:
        return
    st.session_state.pending = None  # clear first so a rerun can never send it twice
    kind = st.session_state.pending_kind
    lang = cur_lang()

    clean, removed = mask_ids(question)
    st.session_state.messages.append({"role": "user", "content": clean})
    with st.chat_message("user"):
        st.markdown(clean)

    topic = TOPICS.get(st.session_state.topic) if st.session_state.topic else None
    with st.chat_message("assistant"):
        if removed:
            st.warning(t("id_removed"))
        if kind == "curated" and topic and topic.get("answer"):
            text = st.write_stream(fake_stream(topic["answer"][lang]))
            sources = topic["sources"]
        else:
            text, sources = ai_answer(clean, lang)
        if sources:
            st.markdown(sources_html(sources), unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": text, "sources": sources})


def render_composer():
    """An explicit, always-visible box to type a question, with a Send button
    and an optional voice-recording button that converts speech to text."""
    with st.container(key="composer"):
        with st.form("composer_form", clear_on_submit=True):
            c_text, c_send = st.columns([8, 1.6])
            with c_text:
                typed = st.text_area(
                    "Question", key="composer_text", height=68,
                    placeholder=t("chat_ph"), label_visibility="collapsed",
                )
            with c_send:
                sent = st.form_submit_button(t("send_btn"), use_container_width=True)
        if sent and typed and typed.strip():
            st.session_state.pending = typed.strip()
            st.session_state.pending_kind = "free"

        if HAS_MIC:
            audio = mic_recorder(
                start_prompt=t("record_btn"), stop_prompt=t("stop_btn"),
                just_once=True, format="wav", key="mic_rec",
            )
            if audio and audio.get("bytes"):
                api_key = get_secret("GROQ_API_KEY")
                if not api_key:
                    st.caption(t("voice_note_need_key"))
                else:
                    with st.spinner(t("voice_transcribing")):
                        try:
                            text = transcribe_audio(api_key, audio["bytes"])
                        except Exception:
                            text = ""
                    if text:
                        st.session_state.pending = text
                        st.session_state.pending_kind = "free"
        else:
            st.markdown('<p class="voice-note">{}</p>'.format(html.escape(t("voice_note_missing_pkg"))),
                        unsafe_allow_html=True)


def page_assistant():
    lang = cur_lang()
    slug = st.session_state.topic
    topic = TOPICS.get(slug) if slug else None

    sec_title(t("assistant_title"), align="left")
    if topic:
        c_pill, c_clear, _ = st.columns([4, 2, 3], vertical_alignment="center")
        c_pill.markdown(
            '<span class="topic-pill"><span>{}</span>{}</span>'.format(
                html.escape(t("topic")), html.escape(topic["title"][lang])
            ),
            unsafe_allow_html=True,
        )
        with c_clear:
            st.button(t("clear_topic"), key="clear_topic", on_click=clear_topic)

    # Language message: shown in both languages, always. There is no language setting for the chat.
    st.markdown(
        '<div class="greet">{}<br>{}</div><div class="note">{}</div>'.format(
            GREETING["en"], GREETING["ur"], html.escape(t("disclaimer"))
        ),
        unsafe_allow_html=True,
    )

    render_composer()

    for message in st.session_state.messages:
        render_message(message)
    answer_pending()

    # Follow-up chips: tap instead of typing
    if topic and topic.get("chips"):
        chips = topic["chips"][lang]
    else:
        chips = [label[lang] for _, label in POPULAR[:3]]
    if chips:
        heading = t("follow_title") if st.session_state.messages else t("start_hint")
        st.markdown('<div class="follow-title">{}</div>'.format(html.escape(heading)),
                    unsafe_allow_html=True)
        with st.container(key="chips"):
            for i, chip in enumerate(chips):
                st.button(chip, key="chip_{}_{}".format(len(st.session_state.messages), i),
                          on_click=ask_chip, args=(chip,))


def page_how():
    lang = cur_lang()
    sec_title(t("how_title"))
    items = "".join(
        "<li><div><h3>{}</h3><p>{}</p></div></li>".format(
            html.escape(step["title"][lang]), html.escape(step["text"][lang])
        )
        for step in HOW_STEPS
    )
    st.markdown('<ol class="steps">{}</ol>'.format(items), unsafe_allow_html=True)
    st.markdown(
        '<div class="closing"><b>{}</b>{}</div>'.format(
            html.escape(t("how_closing")), html.escape(t("how_closing_sub"))
        ),
        unsafe_allow_html=True,
    )


def page_about():
    sec_title(t("about_title"))
    st.markdown(ABOUT[cur_lang()])


PAGES = {
    "home": page_home, "cnic": page_cnic, "services": page_services,
    "assistant": page_assistant, "how": page_how, "about": page_about,
}

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
_font_html, _css_html = build_css(cur_lang())
st.markdown(_font_html, unsafe_allow_html=True)
st.markdown(_css_html, unsafe_allow_html=True)

render_topbar()
PAGES[st.session_state.nav]()
render_footer()

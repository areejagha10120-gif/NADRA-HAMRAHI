# -*- coding: utf-8 -*-
"""
Visual design for NADRA HAMRAHI, modelled on nadra.gov.pk's own visual
language (as shown in the reference screenshots), adapted to a chat product:

  - white page, thin nav bar, small green wordmark
  - hero: soft green gradient wash (not a solid block), big two-line
    headline with the second line in green, two pill buttons, a graphic
    on the right, a thin scrolling notice strip underneath
  - every card grid (services, popular questions, problems, CNIC options)
    uses the same pattern seen on nadra.gov.pk: a plain white card with a
    thin green line under it and a small "More detail"-style link
  - no emoji anywhere; icons are plain line icons (Streamlit's Material
    Symbols) and the one hero graphic is a flat, non-photographic SVG

Palette (brand brief)
  brand  #006600   primary
  deep   #01411C   darkest cluster green (nav text, headings on dark)
  mid    #146125   cluster green
  bright #037E1C   cluster green (links, accents)
  leaf   #00B152   cluster green (focus rings, small highlights)
"""

FONT_IMPORT = (
    "<style>@import url('https://fonts.googleapis.com/css2?"
    "family=Manrope:wght@500..800"
    "&family=Noto+Nastaliq+Urdu:wght@400..700"
    "&family=Public+Sans:wght@400..700&display=swap');</style>"
)

BASE_CSS = """
:root {
  --brand: #006600;
  --deep: #01411C;
  --mid: #146125;
  --bright: #037E1C;
  --leaf: #00B152;
  --ink: #17241A;
  --muted: #5C6B5E;
  --paper: #FFFFFF;
  --tint: #EEF4EE;
  --line: #DDE6DD;
  --head: "Manrope", "Noto Nastaliq Urdu", system-ui, sans-serif;
  --body: "Public Sans", "Noto Nastaliq Urdu", system-ui, sans-serif;
  --wrap: 1180px;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--paper);
  color: var(--ink);
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button {
  font-family: var(--body);
}
[data-testid="stIconMaterial"] { font-family: "Material Symbols Rounded" !important; }
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stSidebar"],
[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] {
  display: none !important;
}
[data-testid="stMainBlockContainer"], .block-container {
  max-width: var(--wrap);
  padding: 0 1.4rem 4.5rem;
}
/* the style/font blocks we inject take no visible space */
[data-testid="stElementContainer"]:has(> style), .element-container:has(> style) { display: none; }
a { color: var(--bright); }
button:focus-visible, input:focus-visible, textarea:focus-visible {
  outline: 3px solid var(--leaf) !important; outline-offset: 2px;
}

/* ---- nav bar ----------------------------------------------------------- */
.st-key-topbar { padding: 1.1rem 0 1rem; border-bottom: 1px solid var(--line); margin-bottom: 0; }
.brand-mark { display: flex; align-items: center; gap: .6rem; }
.brand-badge {
  width: 2.3rem; height: 2.3rem; border-radius: 9px; background: var(--deep);
  display: flex; align-items: center; justify-content: center; flex: none;
}
.brand-badge svg { width: 1.3rem; height: 1.3rem; }
.brand-text { font-family: var(--head); font-weight: 800; font-size: 1.24rem; color: var(--deep); line-height: 1.15; }

.st-key-nav [data-testid="stRadio"] > div[role="radiogroup"] { gap: .1rem; flex-wrap: wrap; justify-content: flex-end; }
.st-key-lang [data-testid="stRadio"] > div[role="radiogroup"] { justify-content: flex-end; }
.st-key-nav label[data-baseweb="radio"], .st-key-lang label[data-baseweb="radio"] {
  margin: 0; padding: .5rem .8rem; border-radius: 8px; cursor: pointer; transition: background .15s;
}
.st-key-nav label[data-baseweb="radio"] > div:first-child,
.st-key-lang label[data-baseweb="radio"] > div:first-child { display: none; }
.st-key-nav label[data-baseweb="radio"] p { font-weight: 600; font-size: .95rem; color: var(--ink); }
.st-key-lang label[data-baseweb="radio"] p { font-weight: 700; font-size: .92rem; color: var(--mid); }
.st-key-nav label[data-baseweb="radio"]:hover { background: var(--tint); }
.st-key-nav label[data-baseweb="radio"]:has(input:checked) p { color: var(--brand); }
.st-key-nav label[data-baseweb="radio"]:has(input:checked) { box-shadow: inset 0 -2px 0 var(--brand); border-radius: 4px; }
.st-key-lang label[data-baseweb="radio"]:has(input:checked) { background: var(--tint); }

/* ---- hero --------------------------------------------------------------*/
.st-key-hero {
  position: relative; overflow: hidden;
  background:
    radial-gradient(60% 90% at 100% -10%, rgba(0,177,82,.16), transparent 60%),
    radial-gradient(70% 80% at -10% 110%, rgba(1,65,28,.10), transparent 60%),
    var(--paper);
  padding: 3.4rem 0 2.2rem;
}
.hero-grid { display: grid; grid-template-columns: 1.15fr .85fr; gap: 2.5rem; align-items: center; }
.hero-title {
  font-family: var(--head); font-weight: 800; letter-spacing: -.02em;
  font-size: clamp(2.5rem, 4.6vw, 3.7rem); line-height: 1.08; color: var(--ink); margin: 0 0 1.1rem;
}
.hero-title .accent { display: block; color: var(--brand); }
.hero-sub { font-size: 1.14rem; line-height: 1.6; color: var(--muted); max-width: 46ch; margin: 0 0 1.7rem; }
.hero-art { display: flex; justify-content: center; }
.hero-art svg { width: 100%; max-width: 340px; height: auto; }

.st-key-hero_form [data-testid="stForm"] { border: 0; padding: 0; background: transparent; }
.st-key-hero_form [data-baseweb="input"], .st-key-hero_form [data-baseweb="base-input"] {
  background: #fff; border: 1.5px solid var(--line); border-radius: 11px;
}
.st-key-hero_form input { color: var(--ink); font-size: 1.02rem; padding: .95rem 1.05rem; }
.st-key-hero_form button {
  background: var(--brand); color: #fff; border: 0; border-radius: 11px;
  font-weight: 700; min-height: 3.15rem; width: 100%;
}
.st-key-hero_form button p { color: #fff; font-weight: 700; }
.st-key-hero_form button:hover { background: var(--deep); }

.st-key-hero_pills { margin-top: 1rem; }
.st-key-hero_pills .stButton > button { border-radius: 999px; min-height: 3rem; font-weight: 700; }
.st-key-hero_ask .stButton > button, .st-key-hero_ask > button { background: var(--brand); color: #fff; border: 0; }
.st-key-hero_ask .stButton > button p { color: #fff; }
.st-key-hero_ask .stButton > button:hover { background: var(--deep); }
.st-key-hero_how .stButton > button { background: transparent; border: 1.6px solid var(--brand); }
.st-key-hero_how .stButton > button p { color: var(--brand); }
.st-key-hero_how .stButton > button:hover { background: var(--tint); }

/* ---- scrolling notice strip ---------------------------------------------*/
.ticker-wrap {
  background: var(--deep); overflow: hidden; white-space: nowrap; padding: .6rem 0;
}
.ticker-track { display: inline-block; animation: ticker 32s linear infinite; }
.ticker-track span { color: #DDEFDF; font-size: .88rem; font-weight: 600; margin: 0 2.4rem; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .ticker-track { animation: none; } }

/* ---- section titles -------------------------------------------------- */
.sec-wrap { padding: 2.6rem 0 .4rem; text-align: center; }
.sec-title { font-family: var(--head); font-weight: 800; font-size: 1.9rem; letter-spacing: -.015em; color: var(--ink); margin: 0 0 .5rem; }
.sec-sub { color: var(--muted); font-size: 1rem; max-width: 62ch; margin: 0 auto; line-height: 1.6; }
.sec-wrap.left { text-align: start; }
.sec-wrap.left .sec-sub { margin: 0; }

/* ---- card grid (shared: popular / problems / cnic / services) --------- */
.stButton, .stButton > button { width: 100%; }
[class*="st-key-tiles"] .stButton > button, .st-key-popular .stButton > button {
  background: #fff; border: 1px solid var(--line); border-bottom: 3px solid var(--bright);
  border-radius: 10px; padding: 1.15rem 1.2rem 1rem; min-height: 5.6rem;
  justify-content: flex-start; text-align: start; gap: .65rem; transition: border-color .15s, transform .1s;
}
[class*="st-key-tiles"] .stButton > button p, .st-key-popular .stButton > button p {
  font-weight: 700; font-size: 1rem; color: var(--ink); text-align: start; line-height: 1.4;
}
[class*="st-key-tiles"] .stButton > button span, .st-key-popular .stButton > button span { color: var(--brand); }
[class*="st-key-tiles"] .stButton > button:hover, .st-key-popular .stButton > button:hover {
  border-bottom-color: var(--deep); transform: translateY(-1px);
}

/* follow-up chips: small pill buttons, not full cards */
.st-key-chips { display: flex; flex-direction: row; flex-wrap: wrap; gap: .55rem; }
.st-key-chips > div { width: auto !important; flex: 0 0 auto; }
.st-key-chips .stButton, .st-key-chips .stButton > button { width: auto; }
.st-key-chips .stButton > button {
  background: #fff; border: 1px solid var(--bright); border-radius: 999px; padding: .4rem 1.05rem; min-height: 2.4rem;
}
.st-key-chips .stButton > button p { color: var(--mid); font-weight: 600; font-size: .93rem; }
.st-key-chips .stButton > button:hover { background: var(--brand); border-color: var(--brand); }
.st-key-chips .stButton > button:hover p { color: #fff; }

.st-key-clear_topic .stButton > button { background: transparent; border: 1px solid var(--line); border-radius: 999px; min-height: 2.2rem; }
.st-key-clear_topic .stButton > button p { color: var(--muted); font-size: .88rem; }

/* ---- services cards ---------------------------------------------------*/
.svc-group { font-family: var(--head); font-weight: 700; font-size: 1.15rem; color: var(--deep); margin: 1.6rem 0 .8rem; }
[class*="st-key-svc"] {
  background: #fff; border: 1px solid var(--line); border-bottom: 3px solid var(--bright);
  border-radius: 10px; padding: 1.25rem 1.3rem 1.1rem; margin-bottom: .95rem;
}
.svc-name { font-family: var(--head); font-weight: 700; font-size: 1.14rem; color: var(--ink); margin: 0 0 .3rem; }
.svc-blurb { color: var(--muted); font-size: .96rem; margin: 0 0 .9rem; line-height: 1.55; }
[class*="st-key-svc"] .stButton > button { background: transparent; border: 0; padding: 0; min-height: unset; width: auto; }
[class*="st-key-svc"] .stButton > button p { color: var(--bright); font-weight: 700; font-size: .92rem; }
[class*="st-key-svc"] .stButton > button:hover p { color: var(--deep); text-decoration: underline; }

/* ---- assistant page -----------------------------------------------------*/
.topic-pill { display: inline-block; background: var(--deep); color: #fff; border-radius: 999px; padding: .35rem 1.05rem; font-weight: 700; font-size: .93rem; }
.topic-pill span { color: #A9DDB7; font-weight: 500; margin-inline-end: .35rem; }
.greet {
  background: var(--tint); border-radius: 12px; padding: .9rem 1.15rem; margin: .9rem 0 .5rem;
  line-height: 1.9; font-weight: 600; color: var(--deep);
}
.note { color: var(--muted); font-size: .87rem; margin: 0 0 1.3rem; line-height: 1.6; }

[data-testid="stChatMessage"] { background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.15rem; margin-bottom: .7rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: var(--tint); border-color: var(--tint); }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { line-height: 1.95; unicode-bidi: plaintext; text-align: start; }

.src { margin-top: .7rem; padding-top: .6rem; border-top: 1px dashed var(--line); font-size: .84rem; color: var(--muted); line-height: 1.9; }
.src a { color: var(--brand); text-decoration: underline; text-underline-offset: 2px; }
.tag { display: inline-block; padding: 0 .5rem; margin-inline: .35rem .9rem; border-radius: 999px; font-size: .72rem; font-weight: 600; background: var(--tint); color: var(--deep); }
.tag.news, .tag.web { background: #F6EBC9; color: #5B4300; }
.follow-title { font-weight: 700; color: var(--deep); margin: 1.1rem 0 .55rem; font-size: .96rem; }

/* composer: an explicit, always-visible type box (not the floating chat_input) */
.st-key-composer {
  background: #fff; border: 1.6px solid var(--line); border-radius: 14px;
  padding: .6rem .6rem .6rem 1.1rem; margin: .9rem 0 1.3rem;
}
.st-key-composer [data-testid="stForm"] { border: 0; padding: 0; }
.st-key-composer [data-baseweb="base-input"], .st-key-composer [data-baseweb="textarea"] { background: transparent; border: 0; }
.st-key-composer textarea { font-size: 1.02rem; line-height: 1.6; }
.st-key-composer .stButton > button {
  background: var(--brand); color: #fff; border: 0; border-radius: 10px; min-height: 2.7rem; font-weight: 700;
}
.st-key-composer .stButton > button p { color: #fff; }
.st-key-composer .stButton > button:hover { background: var(--deep); }
.voice-note { color: var(--muted); font-size: .82rem; margin: .3rem 0 1rem; }
/* note: the voice recorder is a sandboxed component (its own iframe), so
   page CSS cannot restyle it; only the surrounding .composer box is ours */

/* ---- how it works ---------------------------------------------------- */
.steps { list-style: none; margin: 1.2rem 0 0; padding: 0; counter-reset: step; }
.steps li { counter-increment: step; display: flex; gap: 1.2rem; align-items: flex-start; padding: 1.1rem 0; border-bottom: 1px solid var(--line); }
.steps li::before {
  content: counter(step); flex: 0 0 2.5rem; height: 2.5rem; border-radius: 8px; background: var(--tint); color: var(--brand);
  font-family: var(--head); font-weight: 800; display: flex; align-items: center; justify-content: center; margin-top: .1rem; font-size: 1.05rem;
}
.steps h3 { font-family: var(--head); font-size: 1.16rem; margin: 0 0 .2rem; color: var(--ink); }
.steps p { margin: 0; color: var(--muted); line-height: 1.6; }
.closing { margin-top: 2.2rem; padding: 1.8rem; border-radius: 16px; background: var(--tint); }
.closing b { font-family: var(--head); font-size: 1.4rem; display: block; margin-bottom: .35rem; color: var(--deep); }
.closing p { color: var(--muted); margin: 0; }

/* ---- footer ------------------------------------------------------------*/
.foot { margin-top: 3rem; padding: 1.6rem 1.8rem; border-radius: 16px; background: var(--deep); color: #E3F2E5; }
.foot-title { font-family: var(--head); font-weight: 700; font-size: 1.05rem; color: #fff; margin-bottom: .9rem; }
.foot-grid { display: flex; flex-wrap: wrap; gap: 1.2rem 2.6rem; }
.foot-item small { display: block; color: #A9DDB7; font-size: .8rem; }
.foot-item strong { color: #fff; font-size: 1.05rem; font-weight: 700; }
.foot-note { margin-top: 1.1rem; font-size: .84rem; color: #BFE3C8; line-height: 1.6; }

@media (max-width: 900px) {
  .hero-grid { grid-template-columns: 1fr; }
  .hero-art { order: -1; max-width: 220px; margin: 0 auto 1.2rem; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""

URDU_CSS = """
[data-testid="stAppViewContainer"] { direction: rtl; }
.stApp { font-size: 1.05rem; }
.stApp p, .stApp li, .stApp label { line-height: 2.05; }
.hero-title, .sec-title, .svc-name, .steps h3, .brand-text { line-height: 1.85; letter-spacing: 0; }
.hero-title { font-weight: 700; }
.stButton > button, textarea { direction: rtl; }
.stButton > button p { line-height: 2; padding-block: .1rem; }
.ticker-track span { font-family: "Noto Nastaliq Urdu", sans-serif; }
"""

# A flat, non-photographic hero graphic: a stylised ID card with a badge
# check-mark, plus a fingerprint motif in the background. No real or
# realistic-looking people, so nothing here can be mistaken for a photo.
HERO_SVG = """
<svg viewBox="0 0 340 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">
  <circle cx="170" cy="170" r="160" fill="#EEF4EE"/>
  <g opacity="0.55" stroke="#00B152" stroke-width="3" fill="none">
    <path d="M170 235a65 65 0 1 1 0-130"/>
    <path d="M170 218a48 48 0 1 1 0-96"/>
    <path d="M170 201a31 31 0 1 1 0-62"/>
  </g>
  <rect x="70" y="118" width="200" height="128" rx="16" fill="#01411C"/>
  <rect x="70" y="118" width="200" height="30" rx="16" fill="#037E1C"/>
  <circle cx="112" cy="182" r="22" fill="#FFFFFF" opacity="0.92"/>
  <rect x="146" y="168" width="96" height="9" rx="4.5" fill="#FFFFFF" opacity="0.85"/>
  <rect x="146" y="188" width="72" height="7" rx="3.5" fill="#A9DDB7"/>
  <rect x="90" y="216" width="160" height="7" rx="3.5" fill="#146125"/>
  <circle cx="255" cy="95" r="30" fill="#006600"/>
  <path d="M242 96l9 9 18-19" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def build_css(lang):
    """Return (font_html, css_html). They are injected with two separate st.markdown calls."""
    css = BASE_CSS + (URDU_CSS if lang == "ur" else "")
    return FONT_IMPORT, "<style>\n" + css + "\n</style>"

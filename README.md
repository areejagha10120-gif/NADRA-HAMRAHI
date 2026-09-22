# NADRA HAMRAHI: Streamlit prototype

A quick, clickable preview of the NADRA HAMRAHI idea. It is **only for seeing how the
product looks and works**. The real app is planned in Next.js + Supabase + Groq.

##   Live Demo

  **Try the application here:**

  [Nadra Hamrahi] (https://nadra-ahmrahi-20-wd47iuoz5zvrrparhxkq6q.streamlit.app/#ask-about-anything-nadra)

## Design concept

The look is modelled on nadra.gov.pk itself: a white page, a slim nav bar with a small green
wordmark, a hero with a soft green gradient wash and a big two-line headline (second line in
green), two pill buttons, and — the pattern repeated everywhere — plain white cards with a thin
green line underneath, the same way nadra.gov.pk presents its "Identity Services" cards.

The reference site uses a family photo in its hero. This app uses a small flat icon-style
graphic (an ID card and a badge) instead, since it isn't appropriate to reuse a real photo or
generate a realistic-looking one. No emoji are used anywhere; icons are plain line icons
(Streamlit's Material Symbols).

## What you can try

- **English | اردو toggle** in the top bar: switches every reading page (buttons, cards, services,
  How it works, About) and flips the layout right-to-left for Urdu.
- **Home:** a hero with two pill buttons, a scrolling notice strip, 6 popular questions, 6 common
  problems.
- **CNIC:** 7 options.
- **Services:** short English/Urdu introductions, each with a "More detail"-style link.
- **Ask AI:** the ONE chat page. Every card lands here and its question is sent automatically.
  Topic label, follow-up chips, sources under each answer, and the English/Urdu greeting.
- **A visible type box with a Send button**, plus an optional **voice button**: press it, speak,
  and your words are converted to text and asked automatically (English, Urdu or Roman Urdu — the
  speech model detects the language on its own).
- The chat answers in the language you type or speak. It has no language setting.

## Two modes

| Mode | What happens |
|---|---|
| **Demo (no key)** | Card clicks show the pre-written answers. Typed or spoken questions show the closest saved information. Voice recording still works, but shows a note that it needs a key to convert speech to text. |
| **Live (with a Groq key)** | Typed and spoken questions are answered by `openai/gpt-oss-120b`, using only the saved NADRA information as context. Falls back to `openai/gpt-oss-20b` if the first model is busy. Voice recordings are converted to text by Groq's Whisper model, using the same key. |

Card clicks never use AI, so they cost nothing against the free Groq limits.
Each browser session is capped at 15 AI answers to protect the free quota.

## Put it online (free)

### 1. Get a Groq key (optional but recommended)
Go to console.groq.com, sign up, open **API Keys**, and create a key (it starts with `gsk_`).

### 2. Upload to GitHub
1. Create a new repository, for example `nadra-hamrahi`.
2. **Add file → Upload files**, then drag in: `app.py`, `content.py`, `ai.py`, `styles.py`,
   `requirements.txt`, `README.md`, `.gitignore`.
3. Optional theme file: **Add file → Create new file**, type the name `.streamlit/config.toml`
   (typing the `/` creates the folder) and paste the contents of the `config.toml` from this folder.
   The app works without it.
4. Never upload a file called `secrets.toml`.

### 3. Deploy on Streamlit Community Cloud
1. Go to share.streamlit.io and sign in with GitHub.
2. **Create app**, pick your repository, branch `main`, main file `app.py`.
3. Open **Advanced settings → Secrets** and paste:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. Click **Deploy**.

### Run it on your own computer instead
```
pip install -r requirements.txt
streamlit run app.py
```
For live answers, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste your key.

## How the files fit together

| File | Job |
|---|---|
| `app.py` | Pages, navigation and the single chat page |
| `content.py` | ALL text: interface, topics, pre-written answers, saved knowledge (English + Urdu) |
| `ai.py` | Hides ID numbers, finds relevant snippets, calls Groq, handles fallback |
| `styles.py` | The green design system (colours, fonts, cards, right-to-left) |

**Add a topic:** add one entry to `TOPICS` in `content.py`, then add its slug to `POPULAR`, `PROBLEMS`
or `CNIC_OPTIONS`. No new page is needed.

## About the voice button

It uses the `streamlit-mic-recorder` package, already listed in `requirements.txt`, so Streamlit
Community Cloud installs it automatically. If you run the app locally without installing
requirements, the button quietly disappears and a small note explains why, instead of the app
crashing. Recording happens in your browser; the audio is sent to Groq only to convert it to
text, then discarded.

## Prototype shortcuts (the real app fixes these)

- Snippet search is simple keyword matching. The real app uses Supabase pgvector with a multilingual embedding model.
- The saved knowledge is a small hand-written set. The real app loads official NADRA pages with source and date.
- No database, no accounts, nothing stored between visits.
- Some sources are news reports and community websites. They are labelled as such in the app.

## Before showing this to other people

1. **Proofread the Urdu** in `content.py`.
2. **Re-check every answer against nadra.gov.pk.** NADRA rules, the pensioner Proof of Life process and
   face verification are all changing quickly.
3. Fees are intentionally not quoted anywhere. Keep it that way.
4. The contact details in the footer come from NADRA's contact page. Re-verify them before launch.

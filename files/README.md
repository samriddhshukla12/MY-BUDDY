# Second Brain + Story Engine — Setup Guide

A beginner-friendly walkthrough to get this running on your own computer.

## What you're building

A local web app with 4 modes:
- **Add a Note** — save thoughts/journal entries
- **Ask Anything** — plain AI Q&A, no memory
- **Ask My Notes** — AI answers using only your saved notes
- **Recall** — "what was I thinking about X" style memory search
- **Story Mode** — turns your own notes into a short story

---

## Step 1: Install Python

If you don't have Python yet:
1. Go to https://www.python.org/downloads/
2. Download and install the latest version
3. **Important (Windows only):** during install, check the box that says "Add Python to PATH"

To check it worked, open a terminal (Command Prompt / Terminal app) and type:
```
python --version
```
You should see something like `Python 3.11.x`.

---

## Step 2: Get the project files

Save all these files into one folder, e.g. `second_brain_app`:
- `app.py`
- `database.py`
- `memory.py`
- `ai.py`
- `requirements.txt`
- `.env.example`

(If you got these from Claude, they should already be organized this way.)

---

## Step 3: Open a terminal in that folder

- **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, press Enter
- **Mac:** right-click the folder → "New Terminal at Folder" (or open Terminal and `cd` into it)

---

## Step 4: Create a virtual environment (keeps things clean)

This step is optional but recommended — it keeps this project's packages separate from everything else on your computer.

```
python -m venv venv
```

Then activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

You'll know it worked because your terminal line will now start with `(venv)`.

---

## Step 5: Install the required packages

```
pip install -r requirements.txt
```

This installs Streamlit, the Claude SDK, the free embedding model library, and a couple of helpers. It may take a few minutes the first time.

---

## Step 6: Get your Claude API key

1. Go to https://console.anthropic.com
2. Sign up / log in
3. Go to "API Keys" and create a new key
4. Copy it

**Note:** the API is pay-as-you-go (separate from a claude.ai subscription). You'll need to add billing details, but usage for a personal project like this is typically very cheap (fractions of a cent per request for short answers).

---

## Step 7: Add your API key to the project

1. In your project folder, make a copy of `.env.example` and rename the copy to `.env`
2. Open `.env` in any text editor
3. Replace `your-api-key-here` with the key you copied:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxx
```
4. Save the file

**Never share this file or upload it anywhere public (like GitHub) — it's basically your password for the API.**

---

## Step 8: Run the app

Back in your terminal (make sure you're still in the project folder):

```
streamlit run app.py
```

A browser tab should open automatically at `http://localhost:8501`. If it doesn't, copy that URL into your browser manually.

---

## Step 9: Use it

1. Start with **Add a Note** — write a few notes/thoughts to give the app something to work with
2. Try **Ask Anything** — general questions, no memory needed
3. Try **Ask My Notes** or **Recall** — ask something related to what you just wrote
4. Try **Story Mode** — generate a short story built from your notes

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Try `python3` instead of `python` |
| `command not found: streamlit` | Make sure your virtual environment is activated (Step 4), then re-run Step 5 |
| API errors when asking questions | Double-check your `.env` file has the correct key and no extra spaces |
| First run is slow | Normal — it's downloading the free embedding model (~80MB) once |
| Notes not showing up | Check that `notes.db` was created in your project folder — it's created automatically the first time you add a note |

---

## What each file does (quick reference)

- `app.py` — the web page you interact with (Streamlit UI)
- `database.py` — saves/loads your notes (SQLite, a file-based database)
- `memory.py` — converts text into searchable "meaning" and finds relevant notes
- `ai.py` — sends prompts to Claude for each mode
- `requirements.txt` — list of packages to install
- `.env` — your private API key (you create this from `.env.example`)

---

## Next steps once this works

- Add a delete/edit button for notes
- Add file upload (so you can import old journal `.txt` files in bulk)
- Add tags/categories to notes
- Deploy it online (e.g. Streamlit Community Cloud) so you can use it from your phone

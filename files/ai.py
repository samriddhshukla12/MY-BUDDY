"""
ai.py
-----
This file handles all calls to Google's Gemini API (FREE tier).
Each function here is one "mode" of the app.

You need a free API key from Google AI Studio (aistudio.google.com/apikey).
No credit card required for the free tier.
We load it from a .env file so you never paste your key directly into code.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and loads GOOGLE_API_KEY into the environment

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-3.5-flash"  # fast, and included in the free tier


def _generate(prompt: str, max_tokens: int = 1000) -> str:
    """Shared helper: sends a prompt to Gemini and returns the text response."""
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens)
    )
    return response.text


def ask_anything(question: str) -> str:
    """Mode 1: Plain Q&A, no memory involved. Just clears a doubt on any topic."""
    return _generate(question, max_tokens=1000)


def ask_my_notes(question: str, relevant_notes: list) -> str:
    """Mode 2: Answers using ONLY the user's own notes as context."""
    if not relevant_notes:
        return "I couldn't find anything in your notes related to that."

    context = "\n\n".join([f"- {n['content']}" for n in relevant_notes])

    prompt = f"""Here are some of the user's personal notes:

{context}

Based only on these notes, answer this question: {question}

If the notes don't contain a real answer, say so honestly instead of guessing."""

    return _generate(prompt, max_tokens=1000)


def recall_summary(relevant_notes: list) -> str:
    """Mode 3: Summarizes what was found, framed as a memory recall (e.g. 'what was I thinking about X')."""
    if not relevant_notes:
        return "I couldn't find any notes related to that."

    context = "\n\n".join([f"- ({n['created_at'][:10]}) {n['content']}" for n in relevant_notes])

    prompt = f"""Here are notes the user wrote in the past, related to their question:

{context}

Write a short, natural summary (like a friend reminding them) of what they
were thinking about, referencing the general timeframes if useful."""

    return _generate(prompt, max_tokens=800)


def generate_story(relevant_notes: list, word_count: int, tone: str) -> str:
    """Mode 4: Extracts constraints from notes, then writes a short story built from them."""
    if not relevant_notes:
        return "No notes found to build a story from. Try adding some notes first."

    context = "\n\n".join([f"- {n['content']}" for n in relevant_notes])

    prompt = f"""Here are some of the user's personal notes and ideas:

{context}

Step 1: Pick ONE recurring theme, ONE object or idea, and ONE mood from these notes.
Step 2: Treat those three things as hard constraints for a short story.
Step 3: Write a short story (~{word_count} words) in a {tone} tone that
must include all three constraints.

First, briefly list the 3 constraints you extracted. Then write the story."""

    return _generate(prompt, max_tokens=2000)
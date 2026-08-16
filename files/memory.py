"""
memory.py
---------
This file is the "search brain" of the app.

When you save a note, we convert its text into a list of numbers
(called an "embedding") that captures its meaning. When you search later,
we convert your question into numbers too, and find the notes whose
numbers are most "similar" — this is how the app finds relevant notes
even if you don't use the exact same words.

We use a free, local model (sentence-transformers) so you don't need
an API key just for search — only for the actual AI answers later.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# This downloads a small free model the first time you run the app
# (about 80MB). After that, it's cached locally and loads instantly.
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> list:
    """Converts a piece of text into a list of numbers (embedding)."""
    model = get_model()
    vector = model.encode(text)
    return vector.tolist()


def cosine_similarity(vec_a, vec_b) -> float:
    """
    Measures how similar two embeddings are.
    Returns a number between -1 and 1 (1 = identical meaning).
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_notes(query: str, notes: list, top_k: int = 5) -> list:
    """
    Finds the notes most relevant to the query.
    - query: what the user typed (e.g. "what was I thinking about marketing?")
    - notes: the full list of notes from the database
    - top_k: how many matching notes to return

    Returns the notes sorted by relevance (most relevant first),
    each with a 'score' added.
    """
    if not notes:
        return []

    query_embedding = embed_text(query)

    scored_notes = []
    for note in notes:
        score = cosine_similarity(query_embedding, note["embedding"])
        scored_notes.append({**note, "score": score})

    scored_notes.sort(key=lambda n: n["score"], reverse=True)
    return scored_notes[:top_k]

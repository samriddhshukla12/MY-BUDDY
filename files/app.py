"""
app.py
------
This is the main file you run. It creates a web page (using Streamlit)
with a sidebar to switch between modes, and a main area to interact
with each mode.

Run this with:  streamlit run app.py
"""

import streamlit as st
from database import init_db, add_note, get_all_notes
from memory import embed_text, search_notes
from ai import ask_anything, ask_my_notes, recall_summary, generate_story

# --- Setup ---
st.set_page_config(page_title="Second Brain + Story Engine", page_icon="🧠")
init_db()  # make sure the database file/table exists

st.title("🧠MY BUDDY")

# --- Sidebar: mode selector ---
mode = st.sidebar.radio(
    "Choose a mode:",
    ["➕ Add a Note", "💬 Ask Anything", "📓 Ask My Notes", "🔍 Recall", "✍️ Story Mode"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Notes saved: {len(get_all_notes())}")


# ---------------- MODE: Add a Note ----------------
if mode == "➕ Add a Note":
    st.header("Add a Note")
    st.write("Save a thought, idea, or journal entry. This becomes searchable memory.")

    note_text = st.text_area("What's on your mind?", height=150)

    if st.button("Save Note"):
        if note_text.strip():
            with st.spinner("Saving..."):
                embedding = embed_text(note_text)
                add_note(note_text, embedding, note_type="note")
            st.success("Note saved!")
        else:
            st.warning("Write something before saving.")


# ---------------- MODE: Ask Anything ----------------
elif mode == "💬 Ask Anything":
    st.header("Ask Anything")
    st.write("General questions — no memory involved. Just a normal AI Q&A.")

    question = st.text_input("What do you want to know?")

    if st.button("Ask"):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_anything(question)
            st.markdown(answer)
        else:
            st.warning("Type a question first.")


# ---------------- MODE: Ask My Notes ----------------
elif mode == "📓 Ask My Notes":
    st.header("Ask My Notes")
    st.write("Ask a question — the AI will answer using only what you've written before.")

    question = st.text_input("Ask something about your own notes:")

    if st.button("Search & Answer"):
        if question.strip():
            notes = get_all_notes()
            with st.spinner("Searching your notes..."):
                relevant = search_notes(question, notes, top_k=5)
                answer = ask_my_notes(question, relevant)
            st.markdown(answer)

            with st.expander("See which notes were used"):
                for n in relevant:
                    st.write(f"- ({n['created_at'][:10]}) {n['content']}  \n  *relevance: {n['score']:.2f}*")
        else:
            st.warning("Type a question first.")


# ---------------- MODE: Recall ----------------
elif mode == "🔍 Recall":
    st.header("Recall")
    st.write('Example: "what was I thinking about six months ago regarding my career?"')

    query = st.text_input("What do you want to recall?")

    if st.button("Recall"):
        if query.strip():
            notes = get_all_notes()
            with st.spinner("Digging through your memory..."):
                relevant = search_notes(query, notes, top_k=5)
                summary = recall_summary(relevant)
            st.markdown(summary)
        else:
            st.warning("Type something to recall first.")


# ---------------- MODE: Story Mode ----------------
elif mode == "✍️ Story Mode":
    st.header("Story Mode")
    st.write("Turns your own past notes into constraints for a short story.")

    topic_hint = st.text_input("Optional: a topic to pull notes from (leave blank to use your most recent notes)")
    word_count = st.slider("Approximate word count", 100, 1000, 300, step=50)
    tone = st.selectbox("Tone", ["mysterious", "hopeful", "melancholic", "comedic", "dramatic", "whimsical"])

    if st.button("Generate Story"):
        notes = get_all_notes()
        with st.spinner("Extracting constraints and writing..."):
            if topic_hint.strip():
                relevant = search_notes(topic_hint, notes, top_k=5)
            else:
                relevant = notes[:5]  # most recent notes
            story = generate_story(relevant, word_count, tone)

        st.markdown(story)

        if st.button("💾 Save this story as a note"):
            embedding = embed_text(story)
            add_note(story, embedding, note_type="story")
            st.success("Story saved to your notes!")

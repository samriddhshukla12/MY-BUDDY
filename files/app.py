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
# --- Matrix rain background ---
# --- Matrix rain background (with real characters) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #000000 !important;
    background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22220%22%20height%3D%22330%22%3E%3Ctext%20x%3D%228%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%83%8A%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%AA%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%83%8D%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EX%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%A6%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E2%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AA%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%A8%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EZ%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EF%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EB%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%A8%3C%2Ftext%3E%3Ctext%20x%3D%228%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%A6%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%83%86%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%B3%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EB%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EA%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AD%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%83%8D%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EA%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EB%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E6%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EO%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E4%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%83%8D%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%BF%3C%2Ftext%3E%3Ctext%20x%3D%2230%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EJ%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E8%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EV%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EL%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%83%86%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%AF%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%B5%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%B3%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EH%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EN%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%83%8B%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3ED%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EC%3C%2Ftext%3E%3Ctext%20x%3D%2252%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%AA%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EZ%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%A8%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EG%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%83%86%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EV%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%A4%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%83%8C%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E6%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%BB%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%B1%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EX%3C%2Ftext%3E%3Ctext%20x%3D%2274%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E3%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EA%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EV%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3ER%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EU%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EK%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%83%8C%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%BD%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%B3%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EH%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%A2%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3ES%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%83%81%3C%2Ftext%3E%3Ctext%20x%3D%2296%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%A2%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E1%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EZ%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EJ%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E4%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E0%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%A8%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AA%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E3%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%AF%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3ED%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%AD%3C%2Ftext%3E%3Ctext%20x%3D%22118%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EB%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E9%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EZ%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AA%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%B3%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%83%8C%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%AF%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E4%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%AD%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EM%3C%2Ftext%3E%3Ctext%20x%3D%22140%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E8%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%BB%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%B3%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EN%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EG%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EJ%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E8%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EX%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%83%8C%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E9%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EF%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EQ%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3ER%3C%2Ftext%3E%3Ctext%20x%3D%22162%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EM%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%B9%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%83%8C%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%A4%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%B9%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E3%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%83%8D%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3E%E3%82%BD%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%BD%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E%E3%82%B9%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%BB%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EQ%3C%2Ftext%3E%3Ctext%20x%3D%22184%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3ES%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%2216%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EX%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%2238%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EP%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%2260%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E5%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%2282%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3E2%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22104%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E%E3%82%AB%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22126%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3E4%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22148%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.25%22%3EM%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22170%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EL%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22192%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%B5%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22214%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%A4%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22236%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EC%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22258%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3EQ%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22280%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.9%22%3EE%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22302%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.65%22%3EH%3C%2Ftext%3E%3Ctext%20x%3D%22206%22%20y%3D%22324%22%20font-family%3D%22monospace%22%20font-size%3D%2216%22%20fill%3D%22%2300FF41%22%20opacity%3D%220.45%22%3E%E3%82%B3%3C%2Ftext%3E%3C%2Fsvg%3E");
    background-repeat: repeat;
    animation: matrix-fall-bg 6s linear infinite;
}
@keyframes matrix-fall-bg {
    from { background-position: 0 0; }
    to { background-position: 0 330px; }
}

.my-buddy-header {
    background: rgba(0, 0, 0, 0.8);
    padding: 32px 20px 40px;
    text-align: center;
    border-bottom: 3px solid #00FF41;
    border-radius: 8px;
    margin-bottom: 24px;
    box-shadow: 0 0 30px rgba(0,255,65,0.3);
}
.my-buddy-title {
    font-size: 34px;
    font-weight: 700;
    color: #00FF41;
    margin: 0;
    text-shadow: 0 0 10px #00FF41;
}
.my-buddy-signature {
    font-family: 'Great Vibes', cursive;
    font-size: 26px;
    color: #00FF41;
    margin-top: 2px;
    display: inline-block;
    transform: rotate(-4deg);
}
p, label, .stMarkdown, [data-testid="stMarkdownContainer"] {
    color: #E0FFE9 !important;
}
</style>

<div class="my-buddy-header">
    <p class="my-buddy-title">🧠 My Buddy</p>
    <p class="my-buddy-signature">Samriddh's helping hand</p>
</div>
""", unsafe_allow_html=True)
# --- End Matrix background + header ---


# --- End custom header ---
init_db()  # make sure the database file/table exists

st.title("🧠MY BUDDY by Samriddh Shukla ")

# --- Sidebar: mode selector ---
# --- Quick Start Guide (sidebar) ---
with st.sidebar.expander("📖 Quick Start Guide", expanded=False):
    st.markdown("""
    **Welcome to My Buddy!** Here's how to use each mode:

    **➕ Add a Note**
    Save a thought, idea, or journal entry. This is your memory bank — everything else pulls from what you save here.

    **💬 Ask Anything**
    General questions, no memory involved. Works like a normal AI assistant.

    **📓 Ask My Notes**
    Ask a question and get an answer based ONLY on your saved notes.

    **🔍 Recall**
    Jog your memory — e.g. "what was I thinking about last month?"

    **✍️ Story Mode**
    Turns your own notes into a short story, using a theme, object, and mood pulled from what you've written.

    ---
    *Tip: Start by adding a few notes, then try the other modes on them!*
    """)
# --- End Quick Start Guide ---
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

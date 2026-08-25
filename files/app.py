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
# --- Matrix rain background (realistic falling columns) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

/* Stop Streamlit's containers from trapping position:fixed */
[data-testid="stAppViewContainer"], [data-testid="stMain"], .main,
section.main, [data-testid="block-container"] {
    transform: none !important;
}

[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #000000 !important;
}

.matrix-rain-wrap {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    overflow: hidden;
    z-index: -2;
    background: #000000;
}
.matrix-col {
    position: absolute;
    top: -50%;
    font-family: monospace;
    font-size: 20px;
    line-height: 1.15;
    color: #00FF41;
    text-shadow: 0 0 6px #00FF41, 0 0 12px #00FF41;
    white-space: nowrap;
    animation-name: matrix-drop;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
.matrix-col::after {
    content: "";
}
@keyframes matrix-drop {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(300%); }
}

/* Fade mask so the top and bottom blend into black, like real digital rain */
.matrix-fade {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    background: linear-gradient(
        to bottom,
        #000000 0%,
        rgba(0,0,0,0) 15%,
        rgba(0,0,0,0) 70%,
        #000000 100%
    );
    pointer-events: none;
}

.my-buddy-header {
    background: rgba(0, 0, 0, 0.8);
    padding: 32px 20px 40px;
    text-align: center;
    border-bottom: 3px solid #00FF41;
    border-radius: 8px;
    margin-bottom: 24px;
    box-shadow: 0 0 30px rgba(0,255,65,0.35);
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

<div class="matrix-rain-wrap">
<div class="matrix-col" style="left:0.0%; animation-duration:7.2s; animation-delay:-3.4s;">ヘ<br>ム<br>9<br>ヨ<br>ス<br>シ<br>6<br>ム<br>マ<br>ル<br>リ<br>5<br>シ<br>キ<br>ヘ<br>ト<br>コ<br>カ<br>モ<br>6<br>ン<br>ル<br>ウ<br>ラ<br>ハ<br>ヘ<br>レ<br>2<br>リ<br></div><div class="matrix-col" style="left:2.22%; animation-duration:8.6s; animation-delay:-3.7s;">エ<br>ウ<br>ス<br>タ<br>ラ<br>イ<br>4<br>ホ<br>ナ<br>ヘ<br>ヨ<br>8<br>ス<br>メ<br>ソ<br>ル<br>テ<br></div><div class="matrix-col" style="left:4.44%; animation-duration:7.5s; animation-delay:-4.0s;">レ<br>ツ<br>ヒ<br>ヤ<br>8<br>カ<br>0<br>チ<br>ナ<br>3<br>ソ<br>ム<br>テ<br>イ<br>オ<br>ユ<br>4<br>キ<br>ハ<br>キ<br>9<br>テ<br>ノ<br>オ<br>イ<br>9<br>ワ<br>ア<br>セ<br></div><div class="matrix-col" style="left:6.67%; animation-duration:5.5s; animation-delay:-5.5s;">ノ<br>0<br>ハ<br>ヒ<br>オ<br>ユ<br>ル<br>ス<br>4<br>ワ<br>ツ<br>ニ<br>カ<br>ト<br>ニ<br>ア<br>ヒ<br>3<br>ク<br>ケ<br>タ<br>0<br>キ<br>ア<br>エ<br>ホ<br>6<br>ミ<br>シ<br>ワ<br></div><div class="matrix-col" style="left:8.89%; animation-duration:7.9s; animation-delay:-2.7s;">1<br>4<br>ケ<br>ヒ<br>レ<br>ノ<br>ク<br>ハ<br>ヒ<br>セ<br>ア<br>ツ<br>6<br>ヨ<br>ト<br>イ<br>セ<br>シ<br>ハ<br>9<br>ラ<br></div><div class="matrix-col" style="left:11.11%; animation-duration:8.5s; animation-delay:-0.6s;">セ<br>ヘ<br>チ<br>ア<br>4<br>リ<br>ニ<br>8<br>テ<br>ノ<br>オ<br>オ<br>カ<br>セ<br>ヨ<br>ル<br>タ<br>ア<br>ラ<br></div><div class="matrix-col" style="left:13.33%; animation-duration:6.6s; animation-delay:-3.7s;">ヨ<br>マ<br>8<br>ユ<br>ケ<br>ノ<br>シ<br>ル<br>コ<br>ト<br>ソ<br>7<br>リ<br>タ<br>1<br>ス<br>サ<br>2<br>ル<br></div><div class="matrix-col" style="left:15.56%; animation-duration:10.6s; animation-delay:-1.2s;">マ<br>ラ<br>カ<br>ヒ<br>エ<br>キ<br>キ<br>ウ<br>ム<br>チ<br>タ<br>2<br>0<br>ハ<br>チ<br>ヒ<br>7<br>ラ<br>ミ<br>テ<br>メ<br>シ<br>1<br>オ<br>ケ<br>ソ<br>マ<br></div><div class="matrix-col" style="left:17.78%; animation-duration:7.9s; animation-delay:-5.1s;">ツ<br>セ<br>セ<br>2<br>イ<br>オ<br>ツ<br>ヒ<br>ヘ<br>タ<br>エ<br>ウ<br>シ<br>テ<br>ネ<br>メ<br>ユ<br></div><div class="matrix-col" style="left:20.0%; animation-duration:10.8s; animation-delay:-0.6s;">ヘ<br>ニ<br>ロ<br>1<br>ン<br>メ<br>ヨ<br>ケ<br>ヨ<br>ウ<br>イ<br>マ<br>ヌ<br>ン<br>ト<br>ウ<br>イ<br>ラ<br>ル<br></div><div class="matrix-col" style="left:22.22%; animation-duration:4.5s; animation-delay:-0.4s;">ナ<br>ケ<br>オ<br>オ<br>ヘ<br>モ<br>ネ<br>2<br>ウ<br>2<br>2<br>0<br>ケ<br>5<br>ニ<br>ヌ<br>カ<br>ワ<br>マ<br>オ<br>9<br>ヒ<br>5<br>イ<br></div><div class="matrix-col" style="left:24.44%; animation-duration:10.0s; animation-delay:-3.4s;">ノ<br>ヨ<br>ア<br>ラ<br>オ<br>カ<br>カ<br>ル<br>ク<br>チ<br>ヒ<br>1<br>ニ<br>ノ<br>2<br>ン<br>ヨ<br>ホ<br>ヘ<br>ホ<br>8<br>モ<br>カ<br>メ<br>3<br>ム<br>イ<br></div><div class="matrix-col" style="left:26.67%; animation-duration:6.2s; animation-delay:-0.5s;">ソ<br>ン<br>ク<br>ミ<br>4<br>リ<br>ロ<br>ミ<br>チ<br>ア<br>ネ<br>ト<br>コ<br>ワ<br>リ<br></div><div class="matrix-col" style="left:28.89%; animation-duration:5.4s; animation-delay:-1.0s;">ロ<br>ヘ<br>ミ<br>タ<br>ナ<br>ハ<br>ロ<br>チ<br>ス<br>ル<br>フ<br>6<br>6<br>3<br>ス<br>セ<br>ノ<br>ソ<br>ヨ<br>ナ<br>セ<br>ケ<br>ケ<br>ミ<br>ヌ<br></div><div class="matrix-col" style="left:31.11%; animation-duration:9.9s; animation-delay:-5.1s;">ツ<br>7<br>サ<br>ク<br>ヘ<br>マ<br>ツ<br>セ<br>8<br>ヒ<br>ノ<br>ル<br>メ<br>ミ<br>ワ<br>ナ<br>0<br></div><div class="matrix-col" style="left:33.33%; animation-duration:9.9s; animation-delay:-5.9s;">ナ<br>オ<br>8<br>ウ<br>ツ<br>ラ<br>ウ<br>ワ<br>0<br>ツ<br>ユ<br>ヌ<br>ト<br>レ<br>5<br>ユ<br>イ<br>レ<br>ケ<br>ハ<br>ホ<br>ス<br>イ<br>4<br>8<br>ツ<br>タ<br>4<br>コ<br></div><div class="matrix-col" style="left:35.56%; animation-duration:9.6s; animation-delay:-5.9s;">ヘ<br>キ<br>ル<br>モ<br>レ<br>ル<br>6<br>ネ<br>オ<br>ワ<br>ス<br>ス<br>7<br>マ<br>チ<br>シ<br>0<br>ア<br></div><div class="matrix-col" style="left:37.78%; animation-duration:9.3s; animation-delay:-3.2s;">シ<br>ソ<br>ツ<br>4<br>ヌ<br>モ<br>ン<br>メ<br>ム<br>リ<br>3<br>サ<br>ハ<br>9<br>5<br>ン<br></div><div class="matrix-col" style="left:40.0%; animation-duration:10.3s; animation-delay:-0.5s;">ケ<br>ヘ<br>ホ<br>ス<br>ル<br>ア<br>ノ<br>ヤ<br>ユ<br>レ<br>ム<br>5<br>7<br>ニ<br>ホ<br>ナ<br>レ<br>セ<br>キ<br>1<br>7<br>6<br>レ<br>0<br>ク<br>セ<br>タ<br></div><div class="matrix-col" style="left:42.22%; animation-duration:10.3s; animation-delay:-5.9s;">モ<br>5<br>ナ<br>チ<br>0<br>9<br>イ<br>ヌ<br>ム<br>カ<br>ウ<br>ヘ<br>ニ<br>ヤ<br>ヒ<br>4<br>ツ<br>ミ<br>イ<br>セ<br>6<br>オ<br>フ<br>6<br></div><div class="matrix-col" style="left:44.44%; animation-duration:4.2s; animation-delay:-3.2s;">マ<br>コ<br>メ<br>1<br>メ<br>8<br>ワ<br>ン<br>ヘ<br>ミ<br>ヨ<br>ン<br>カ<br>3<br>ソ<br>ヘ<br>メ<br>ヤ<br>テ<br></div><div class="matrix-col" style="left:46.67%; animation-duration:9.8s; animation-delay:-3.4s;">メ<br>ム<br>8<br>ヤ<br>チ<br>ト<br>ロ<br>ノ<br>9<br>リ<br>セ<br>ト<br>9<br>コ<br>モ<br>メ<br>ツ<br>ユ<br>ミ<br>ス<br></div><div class="matrix-col" style="left:48.89%; animation-duration:6.9s; animation-delay:-0.7s;">ラ<br>ノ<br>イ<br>モ<br>ウ<br>メ<br>ハ<br>モ<br>6<br>ユ<br>ク<br>ミ<br>カ<br>ン<br>サ<br></div><div class="matrix-col" style="left:51.11%; animation-duration:4.5s; animation-delay:-3.2s;">6<br>ハ<br>ツ<br>タ<br>マ<br>ミ<br>ケ<br>ニ<br>フ<br>7<br>マ<br>メ<br>ナ<br>キ<br>ス<br>ヒ<br>リ<br>イ<br>チ<br>ケ<br>ン<br>4<br>イ<br>ウ<br>ス<br>コ<br>ソ<br>ア<br></div><div class="matrix-col" style="left:53.33%; animation-duration:8.8s; animation-delay:-1.9s;">タ<br>リ<br>ミ<br>キ<br>ミ<br>1<br>ヨ<br>ク<br>9<br>ム<br>リ<br>チ<br>0<br>ス<br>ン<br>メ<br>フ<br>イ<br>ノ<br>ル<br>ヒ<br>7<br>メ<br>リ<br>サ<br>モ<br></div><div class="matrix-col" style="left:55.56%; animation-duration:5.4s; animation-delay:-3.8s;">メ<br>セ<br>9<br>モ<br>リ<br>ヨ<br>9<br>ケ<br>ソ<br>2<br>ル<br>6<br>ヌ<br>シ<br>ナ<br>ラ<br>ナ<br>ス<br>セ<br>4<br>ス<br></div><div class="matrix-col" style="left:57.78%; animation-duration:10.2s; animation-delay:-0.8s;">ケ<br>1<br>カ<br>チ<br>ノ<br>キ<br>フ<br>8<br>ヒ<br>モ<br>5<br>0<br>ケ<br>ス<br>ハ<br>ル<br>ワ<br>6<br>イ<br>キ<br>ス<br>ユ<br></div><div class="matrix-col" style="left:60.0%; animation-duration:8.8s; animation-delay:-5.5s;">ク<br>0<br>ム<br>ル<br>3<br>ニ<br>ム<br>ワ<br>8<br>ス<br>6<br>オ<br>マ<br>キ<br>イ<br>ウ<br>3<br>ヤ<br>リ<br>ム<br>ユ<br>マ<br>コ<br>ス<br>シ<br>ク<br></div><div class="matrix-col" style="left:62.22%; animation-duration:5.4s; animation-delay:-5.0s;">ワ<br>キ<br>ヨ<br>エ<br>ケ<br>ワ<br>ホ<br>オ<br>3<br>キ<br>ナ<br>ハ<br>ホ<br>フ<br>ム<br>ヌ<br>フ<br>セ<br>ラ<br>ネ<br>ア<br>ル<br>ン<br>ウ<br></div><div class="matrix-col" style="left:64.44%; animation-duration:9.9s; animation-delay:-1.1s;">ネ<br>2<br>ネ<br>ハ<br>ス<br>ラ<br>サ<br>キ<br>ム<br>5<br>ア<br>ナ<br>カ<br>6<br>8<br>0<br>ル<br>ハ<br>ユ<br>ラ<br>ス<br>ム<br>ヨ<br>ニ<br>6<br>3<br>チ<br>ツ<br>ク<br></div><div class="matrix-col" style="left:66.67%; animation-duration:9.2s; animation-delay:-4.7s;">ケ<br>ニ<br>モ<br>ン<br>ネ<br>4<br>フ<br>3<br>シ<br>ハ<br>セ<br>1<br>シ<br>オ<br>6<br>ニ<br>ト<br>マ<br>キ<br>ア<br>ヌ<br>ル<br>リ<br>エ<br>ソ<br>ツ<br>ロ<br></div><div class="matrix-col" style="left:68.89%; animation-duration:6.1s; animation-delay:-1.3s;">ユ<br>シ<br>モ<br>オ<br>ノ<br>ム<br>ミ<br>レ<br>セ<br>ン<br>ク<br>3<br>ハ<br>ユ<br>イ<br>ク<br>リ<br>キ<br>2<br>タ<br>チ<br>ヘ<br>ハ<br>ム<br>エ<br>3<br>ス<br></div><div class="matrix-col" style="left:71.11%; animation-duration:8.5s; animation-delay:-0.1s;">チ<br>ツ<br>ニ<br>ヤ<br>モ<br>ム<br>ヒ<br>メ<br>ユ<br>9<br>キ<br>ル<br>ヘ<br>6<br>レ<br>オ<br>ヤ<br>ラ<br>ロ<br>3<br>ウ<br>ノ<br>サ<br></div><div class="matrix-col" style="left:73.33%; animation-duration:6.7s; animation-delay:-5.8s;">モ<br>リ<br>ラ<br>エ<br>フ<br>ミ<br>ヒ<br>テ<br>メ<br>ハ<br>ラ<br>ト<br>ネ<br>メ<br>テ<br>マ<br>レ<br>ツ<br>ヤ<br>テ<br>ロ<br>0<br>2<br>テ<br>イ<br>ア<br>4<br>タ<br>ヨ<br>ウ<br></div><div class="matrix-col" style="left:75.56%; animation-duration:8.4s; animation-delay:-2.5s;">エ<br>ナ<br>2<br>ハ<br>エ<br>ヨ<br>1<br>ナ<br>オ<br>6<br>ソ<br>フ<br>1<br>マ<br>チ<br>3<br>タ<br>ウ<br>メ<br>キ<br>6<br>1<br>ホ<br>コ<br>7<br>タ<br>ラ<br></div><div class="matrix-col" style="left:77.78%; animation-duration:8.9s; animation-delay:-0.3s;">ホ<br>ク<br>セ<br>エ<br>ヌ<br>メ<br>コ<br>ク<br>ネ<br>ヘ<br>ケ<br>ロ<br>ヒ<br>ホ<br>ラ<br>チ<br>ル<br>ヨ<br>ワ<br>ヒ<br>ネ<br>4<br>2<br>メ<br>7<br>ケ<br>テ<br>1<br></div><div class="matrix-col" style="left:80.0%; animation-duration:4.9s; animation-delay:-2.9s;">5<br>ム<br>リ<br>9<br>ヌ<br>ツ<br>ツ<br>リ<br>ワ<br>1<br>ユ<br>ン<br>ヨ<br>ス<br>ル<br>ツ<br>3<br>タ<br>ス<br>タ<br>ム<br>レ<br>ス<br>ワ<br></div><div class="matrix-col" style="left:82.22%; animation-duration:4.3s; animation-delay:-0.4s;">チ<br>フ<br>イ<br>リ<br>ウ<br>キ<br>ソ<br>モ<br>ツ<br>オ<br>3<br>カ<br>ワ<br>サ<br>ヤ<br>タ<br>ル<br>ネ<br>マ<br>マ<br>ヌ<br>セ<br>ニ<br></div><div class="matrix-col" style="left:84.44%; animation-duration:6.4s; animation-delay:-4.5s;">6<br>ク<br>ヘ<br>6<br>7<br>リ<br>8<br>4<br>4<br>セ<br>ヘ<br>フ<br>2<br>チ<br>ノ<br>6<br>コ<br></div><div class="matrix-col" style="left:86.67%; animation-duration:6.6s; animation-delay:-3.9s;">テ<br>ヤ<br>3<br>2<br>7<br>シ<br>フ<br>レ<br>ネ<br>ヨ<br>キ<br>ホ<br>ナ<br>カ<br>モ<br>カ<br>フ<br>ユ<br>ユ<br>ミ<br>7<br>ワ<br>ホ<br>ト<br>7<br></div><div class="matrix-col" style="left:88.89%; animation-duration:9.4s; animation-delay:-0.5s;">ロ<br>ラ<br>カ<br>ン<br>ト<br>ミ<br>1<br>3<br>ン<br>ナ<br>テ<br>コ<br>ソ<br>ヌ<br>ロ<br>1<br>ナ<br>ネ<br>ク<br>ナ<br>0<br></div><div class="matrix-col" style="left:91.11%; animation-duration:7.1s; animation-delay:-3.6s;">ヘ<br>メ<br>6<br>ト<br>ホ<br>ナ<br>ソ<br>ハ<br>1<br>メ<br>タ<br>カ<br>ネ<br>8<br>ネ<br>イ<br>ネ<br>ワ<br>ハ<br>ヨ<br>ノ<br>5<br>ス<br></div><div class="matrix-col" style="left:93.33%; animation-duration:9.2s; animation-delay:-2.2s;">モ<br>コ<br>8<br>ヨ<br>ユ<br>シ<br>シ<br>カ<br>3<br>ホ<br>9<br>テ<br>6<br>イ<br>ソ<br>メ<br>エ<br>モ<br>サ<br>ユ<br>テ<br>イ<br>レ<br>8<br>6<br>フ<br>オ<br></div><div class="matrix-col" style="left:95.56%; animation-duration:8.1s; animation-delay:-1.8s;">ニ<br>カ<br>ツ<br>2<br>キ<br>ナ<br>カ<br>イ<br>ル<br>レ<br>コ<br>キ<br>2<br>7<br>レ<br>フ<br>タ<br></div><div class="matrix-col" style="left:97.78%; animation-duration:9.0s; animation-delay:-2.9s;">3<br>ホ<br>ハ<br>ヌ<br>ニ<br>6<br>ニ<br>ワ<br>ケ<br>ミ<br>ミ<br>モ<br>6<br>1<br>オ<br>0<br>リ<br>ウ<br>ヒ<br>3<br>7<br>ロ<br>ヌ<br>9<br>ア<br></div>
</div>
<div class="matrix-fade"></div>

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

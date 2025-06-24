import streamlit as st
import pandas as pd
import random
from datetime import datetime

from src.logger import get_logger
from src.config import APP_CONFIG, DATA_CONFIG, UI_CONFIG, ALGORITHMS
from src.style import NETFLIX_CSS
from src.html import HEADER_HTML, FOOTER_HTML
from src.utils import load_data, safe_get, get_movies_by_ids, call_ai_service, init_session

logger = get_logger(__name__)

# Configuration
st.set_page_config(**APP_CONFIG)
logger.info("App started - Page configured")

# Netflix-style CSS
st.markdown(NETFLIX_CSS, unsafe_allow_html=True)

# Header
st.markdown(HEADER_HTML, unsafe_allow_html=True)

df = load_data(DATA_CONFIG['netflix_csv'])

# Initialize Session State
init_session(st, 'current_ids', random.sample(df['id'].tolist(), DATA_CONFIG['default_limit']))
init_session(st, 'algorithm_used', "TF-IDF")
init_session(st, 'last_recommended', None)
init_session(st, 'scores', None)
init_session(st, 'because_you_watched', [])

# Display Movies
movies = get_movies_by_ids(df, st.session_state.current_ids, st.session_state.scores)

# Because You Watched section
if st.session_state.because_you_watched:
    # Place this section immediately after the header
    st.markdown("""
    <div class="section-title">
        <h2>🎬 Because You Watched</h2>
    </div>
    """, unsafe_allow_html=True)

    last_watched = " | ".join(st.session_state.because_you_watched[:])
    with st.expander(f"{last_watched}", expanded=True):
        st.markdown(f"""
        <div class="because-you-watched-card">
            <div class="because-subtitle">Here are some similar titles you might enjoy</div>
        </div>
        """, unsafe_allow_html=True)

num_cols = UI_CONFIG['num_columns']
cols = st.columns(num_cols, gap="small")

#if st.session_state.last_recommended:
#    st.toast(f"🎯 Found movies similar to '{st.session_state.last_recommended}'!", icon="🎬")

for i, row in movies.iterrows():
    with cols[i % num_cols]:
        with st.form(f"form_{row['id']}"):
            genre = str(safe_get(row, 'genres'))
            genre_display = f"{genre[:35]}..." if len(genre) > 35 else genre

            description = safe_get(row, 'overview', 'No description available')
            description_display = description

            poster_path = safe_get(row, 'poster_path', '')
            # Create responsive poster image with proper sizing
            if poster_path:
                poster_html = f'<img src="{poster_path}" class="movie-poster" alt="{row["title"]}" style="width: 400px; height: 200px; object-fit: cover;">'
            else:
                poster_html = '<div class="no-poster" style="width: 100%; aspect-ratio: 2/3; display: flex; align-items: center; justify-content: center;">No Image</div>'

            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-poster-container">
                    {poster_html}
                </div>
                <div class="movie-title">{row['title']}</div>
                <div class="movie-description">{description_display}</div>
                <div class="movie-meta">
                    <div class="meta-row"><span class="meta-label">Imdb Rating:</span> {safe_get(row, 'imdb_rating')} | <span class="meta-label">Duration:</span> {safe_get(row, 'runtime')}</div>
                    <div class="meta-row"><span class="meta-label">Director:</span> {safe_get(row, 'director')}</div>
                    <div class="meta-row"><span class="meta-label">Genre:</span> {genre_display}</div>
                    <div class="meta-row"><span class="meta-label">Score:</span> {safe_get(row, 'score', 0)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("🎯 Get Recommendations", use_container_width=True, type="primary"):
                logger.info(f"User requested recommendations for: {row['title']} (ID: {row['id']})")
                st.session_state.last_recommended = row['title']
                st.session_state.current_ids, st.session_state.scores = call_ai_service(df, row['id'], st.session_state.algorithm_used, limit=DATA_CONFIG['default_limit'])
                st.session_state.because_you_watched.append(row['title'])
                st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Algorithm Selection")

    algorithm = st.selectbox(
        "Choose Algorithm:", ALGORITHMS,
        index=ALGORITHMS.index(st.session_state.algorithm_used)
    )

    if algorithm != st.session_state.algorithm_used:
        logger.info(f"Algorithm changed: {st.session_state.algorithm_used} -> {algorithm}")
        st.session_state.algorithm_used = algorithm

    with st.expander("📊 Algorithm Comparison"):
        st.markdown("""
        **TF-IDF:** Classical NLP, keyword-based, fast
        **Sentence Transformers:** Semantic understanding, context-aware
        **OpenAI GPT:** Advanced language model, human-like recommendations
        """)

    st.markdown("<hr><h3>🔄 Reset Session</h3>", unsafe_allow_html=True)
    if st.button("🔄 Reset", use_container_width=True, type="secondary"):
        logger.info("User reset session")
        st.session_state.current_ids = random.sample(df['id'].tolist(), DATA_CONFIG['default_limit'])
        st.session_state.scores = None
        st.session_state.algorithm_used = "TF-IDF"
        st.session_state.last_recommended = None
        st.toast("Session reset! 🎉", icon="🔄")
        st.rerun()

# Footer
st.markdown(FOOTER_HTML, unsafe_allow_html=True)

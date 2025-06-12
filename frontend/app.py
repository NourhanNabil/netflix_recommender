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


# Display Movies
movies = get_movies_by_ids(df, st.session_state.current_ids)

num_cols = UI_CONFIG['num_columns']
cols = st.columns(num_cols, gap="small")

if st.session_state.last_recommended:
    st.toast(f"🎯 Found movies similar to '{st.session_state.last_recommended}'!", icon="🎬")

for i, row in movies.iterrows():
    with cols[i % num_cols]:
        with st.form(f"form_{row['id']}"):
            genre = str(safe_get(row, 'listed_in'))
            genre_display = f"{genre[:35]}..." if len(genre) > 35 else genre

            description = safe_get(row, 'description', 'No description available')
            description_display = description

            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title">{row['title']}</div>
                <div class="movie-description">{description_display}</div>
                <div class="movie-meta">
                    <div class="meta-row"><span class="meta-label">Type:</span> {row['type']} | <span class="meta-label">Year:</span> {row['release_year']}</div>
                    <div class="meta-row"><span class="meta-label">Rating:</span> {safe_get(row, 'rating')} | <span class="meta-label">Duration:</span> {safe_get(row, 'duration')}</div>
                    <div class="meta-row"><span class="meta-label">Director:</span> {safe_get(row, 'director')}</div>
                    <div class="meta-row"><span class="meta-label">Country:</span> {safe_get(row, 'country')}</div>
                    <div class="meta-row"><span class="meta-label">Genre:</span> {genre_display}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("🎯 Get Recommendations", use_container_width=True, type="primary"):
                logger.info(f"User requested recommendations for: {row['title']} (ID: {row['id']})")
                st.session_state.last_recommended = row['title']
                st.session_state.current_ids = call_ai_service(df, row['id'], st.session_state.algorithm_used, limit=DATA_CONFIG['default_limit'])
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
        st.session_state.algorithm_used = "TF-IDF"
        st.session_state.last_recommended = None
        st.toast("Session reset! 🎉", icon="🔄")
        st.rerun()

# Footer
st.markdown(FOOTER_HTML, unsafe_allow_html=True)

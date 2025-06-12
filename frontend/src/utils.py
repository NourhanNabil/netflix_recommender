import streamlit as st
import pandas as pd
import random

from src.logger import get_logger


logger = get_logger(__name__)

def safe_get(row, column, default='N/A'):
    """Safely get column value with fallback"""
    value = row.get(column, default)
    return value if pd.notna(value) else default

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text with ellipsis if longer than max_length"""
    return f"{text[:max_length]}..." if len(text) > max_length else text

# Data Loading
@st.cache_data
def load_data(path):
    logger.info("Loading Netflix dataset")
    df = pd.read_csv(path)
    df['id'] = df.index
    logger.info(f"Dataset loaded: {len(df)} movies")
    return df

def get_movies_by_ids(df, movie_ids: list[int]) -> pd.DataFrame:
    return df[df['id'].isin(movie_ids)].reset_index(drop=True)

def call_ai_service(df, selected_id: int, algorithm: str, limit: int = 24) -> list[int]:
    """Mock AI service - replace with real implementation"""
    logger.info(f"Generating recommendations: algorithm={algorithm}, movie_id={selected_id}, limit={limit}")
    available_ids = [id for id in df['id'].tolist() if id != selected_id]
    recommendations = random.sample(available_ids, min(limit, len(available_ids)))
    logger.info(f"Generated {len(recommendations)} recommendations")
    return recommendations

def init_session(st, key, default_value):
    """Initialize session state with a default value if not already set."""
    if key not in st.session_state:
        st.session_state[key] = default_value
        logger.info(f"Session state initialized: {key} = {default_value}")

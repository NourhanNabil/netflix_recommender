import streamlit as st
import pandas as pd
import random

from src.logger import get_logger
import requests
from src.config import ALGORITHMS_MAP


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
    df['id'] = df["show_id"]
    logger.info(f"Dataset loaded: {len(df)} movies")
    return df

def get_movies_by_ids(df, movie_ids: list[str], scores: list[float] = None) -> pd.DataFrame:
    df_filtered = df[df['id'].isin(movie_ids)].reset_index(drop=True)
    if scores is not None:
        df_filtered['score'] = scores
    return df_filtered

def call_ai_service(df, selected_id: str, algorithm: str, limit: int = 24) -> tuple[list[str], list[float]]:
    """Call AI service for recommendations"""
    logger.info(f"Calling AI service: algorithm={algorithm}, movie_id={selected_id}, limit={limit}")

    assert algorithm in ALGORITHMS_MAP, f"Algorithm {algorithm} not supported"

    try:
        response = requests.post(
            'http://localhost:8080/recommendations',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json={
                'show_id': selected_id,
                'model_name': ALGORITHMS_MAP[algorithm]
            }
        )
        response.raise_for_status()

        recommendations = response.json() # List[dict]

        assert "recommendations" in recommendations, f"Error in AI service response: {recommendations}"

        recommendations = recommendations['recommendations']

        # select "show_id" from each recommendation
        recommendations_ids = [rec['show_id'] for rec in recommendations if 'show_id' in rec]
        scores = [round(rec['score'], 6) for rec in recommendations if 'score' in rec]

        logger.info(f"Received {len(recommendations_ids)} recommendations from AI service")
        return recommendations_ids[1:limit], scores[1:limit]  # Exclude the first one (the selected movie itself)

    except requests.exceptions.RequestException as e:
        logger.error(f"AI service request failed: {e}")
        raise

def init_session(st, key, default_value):
    """Initialize session state with a default value if not already set."""
    if key not in st.session_state:
        st.session_state[key] = default_value
        logger.info(f"Session state initialized: {key} = {default_value}")

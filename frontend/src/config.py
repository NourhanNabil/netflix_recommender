import logging

# App Configuration
APP_CONFIG = {
    "page_title": "Content-Based Movie Recommender | DS699",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

# Data Configuration
DATA_CONFIG = {
    "netflix_csv": "data/netflix_titles.csv",
    "default_limit": 9
}

# UI Configuration
UI_CONFIG = {
    "num_columns": 3,
    "description_max_length": 120,
    "genre_max_length": 35
}

# Available algorithms
ALGORITHMS = ["TF-IDF", "Sentence Transformers", "OpenAI GPT"]

ALGORITHMS_MAP = {
    "TF-IDF": "tfidf",
    "Sentence Transformers": "sbert",
    "OpenAI GPT": "openai"
}

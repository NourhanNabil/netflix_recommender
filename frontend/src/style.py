NETFLIX_CSS = """
<style>
    /* Global Netflix-style theme */
    .stApp {
        background-color: #141414;
        color: #ffffff;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #e50914 0%, #221f1f 100%);
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        text-align: center;
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 10px;
    }

    .main-header h3 {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }

    /* Movie card styling */
    .movie-card {
        background: linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid transparent;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        height: 380px;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #e50914;
        box-shadow: 0 15px 35px rgba(229, 9, 20, 0.3);
    }

    .movie-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
        min-height: 60px;
        display: flex;
        align-items: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }

    .movie-description {
        font-size: 0.9rem;
        color: #cccccc;
        line-height: 1.5;
        margin-bottom: 15px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        flex-grow: 1;
    }

    .movie-meta {
        font-size: 0.85rem;
        color: #999999;
        margin-bottom: 15px;
        padding: 10px 0;
        border-top: 1px solid #333333;
    }

    .meta-row {
        margin-bottom: 5px;
    }

    .meta-label {
        color: #e50914;
        font-weight: 600;
    }

    /* Button styling */
    .recommend-btn {
        background: linear-gradient(45deg, #e50914 0%, #f40612 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3);
    }

    .recommend-btn:hover {
        background: linear-gradient(45deg, #f40612 0%, #e50914 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }

    /* Toast notification styling */
    .stToast {
        background-color: #2a2a2a;
        border-left: 4px solid #e50914;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #2a2a2a;
    }

    ::-webkit-scrollbar-thumb {
        background: #e50914;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #f40612;
    }

    /* Form button override */
    .stFormSubmitButton > button {
        background: linear-gradient(45deg, #e50914 0%, #f40612 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stFormSubmitButton > button:hover {
        background: linear-gradient(45deg, #f40612 0%, #e50914 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5) !important;
    }

    /* Footer styling */
    .footer {
        background-color: #0a0a0a;
        padding: 30px;
        margin-top: 50px;
        border-top: 2px solid #333333;
        text-align: center;
        color: #999999;
    }
</style>
"""

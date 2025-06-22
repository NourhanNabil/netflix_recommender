from fastapi import APIRouter
import os
import pandas as pd
import numpy as np 
import openai
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from Definitions.RecommenderRequest import RecommendationRequest

recommender_router = APIRouter()

metadata = pd.read_csv("movie_metadata.csv")
metadata.set_index("show_id", inplace=True)
openai.api_key = os.getenv("OPENAI_API_KEY")


vectorizers = {}
faiss_indexes = {}
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

with open(f'embeddings/vectorizer_tfidf.pkl', 'rb') as f:
    vectorizers["tfidf"] = pickle.load(f)

for model_name in ["tfidf", "sbert","openai"]:
    faiss_indexes[model_name] = faiss.read_index(f"embeddings/faiss_{model_name}.index")

def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return np.array(response['data'][0]['embedding'], dtype=np.float32)
    except Exception as e:
        print(f"Error with text: {text[:30]}... | {e}")
        return None,None

@recommender_router.post("/recommendations")
def get_recommendations(req: RecommendationRequest):
    model_name = req.model_name.lower()
    if model_name not in faiss_indexes:
        return {"error": f"Model {model_name} not supported"}
    try:
        input_text = metadata.loc[req.show_id]["all_text_info"]        
    except:
        return {"error": "Invalid show ID provided"}

    if model_name == "tfidf":
        vec = vectorizers["tfidf"].transform([input_text]).toarray().astype('float32')
    elif model_name == "sbert":
        vec = sbert_model.encode([input_text]).astype('float32')
    elif model_name == "openai":
        vec = np.array([get_openai_embedding(input_text)])

    index = faiss_indexes[model_name]
    D, I = index.search(vec, k=10)
    recommendations = metadata.iloc[I[0]].reset_index()
    similarity_scores = 1 - D[0] / 2

    results = []
    for i, row in recommendations.iterrows():
        results.append({
            "show_id": row["show_id"],
            "all_text_info": row["all_text_info"],
            "score": round(float(similarity_scores[i]), 4)
        })

    return {"recommendations": results}
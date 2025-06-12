import pandas as pd
import faiss
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer


df = pd.read_csv("netflix_titles.csv")
df = df.fillna("")
# Use show_id as identifier
df["show_id"] = df["show_id"].astype(str)
df["all_text_info"] = df.drop(columns=["show_id"]).astype(str).apply(lambda row: ", ".join([f"{col}:{val}" for col, val in row.items()]), axis=1)

vectorizers = {
    "tfidf": TfidfVectorizer(stop_words='english', max_features=10000)
}

embeddings = {}

# TF-IDF model
tfidf_vectorizer = vectorizers["tfidf"]
tfidf_vec = tfidf_vectorizer.fit_transform(df["all_text_info"])
embeddings["tfidf"] = tfidf_vec.toarray().astype('float32')

index = faiss.IndexFlatL2(tfidf_vec.shape[1])
index.add(embeddings["tfidf"])
faiss.write_index(index, f"faiss_tfidf.index")
with open(f'vectorizer_tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)
    
    
# Sentence Transformer
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
sbert_vec = sbert_model.encode(df["all_text_info"].tolist(), show_progress_bar=True)
embeddings["sbert"] = sbert_vec.astype('float32')
index = faiss.IndexFlatL2(sbert_vec.shape[1])
index.add(embeddings["sbert"])
faiss.write_index(index, f"faiss_sbert.index")


# Save metadata
metadata = df[["show_id", "all_text_info"]]
metadata.to_csv("movie_metadata.csv", index=False)


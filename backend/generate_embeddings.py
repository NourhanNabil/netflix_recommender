import pandas as pd
import numpy as np
import faiss
import os 
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

df = pd.read_csv("netflix_titles.csv")
df = df.fillna("")
columns_to_be_dropped = ['show_id','vote_average','vote_count','status','imdb_id','popularity','tagline','imdb_rating','imdb_votes','poster_path']
# Use show_id as identifier
df["show_id"] = df["show_id"].astype(str)
df["all_text_info"] = df.drop(columns=columns_to_be_dropped).astype(str).apply(lambda row: ", ".join([f"{val}" for col, val in row.items()]), axis=1)

vectorizers = {
    "tfidf": TfidfVectorizer(analyzer='word', stop_words="english", token_pattern='(?u)\\b\\w\\w+\\b', ngram_range=(2, 4), max_features=1000)
}

embeddings = {}

# TF-IDF model
tfidf_vectorizer = vectorizers["tfidf"]
tfidf_vec = tfidf_vectorizer.fit_transform(df["all_text_info"])
embeddings["tfidf"] = tfidf_vec.toarray().astype('float32')

np.savez('tfidf_embeddings.npz', embeddings=embeddings["tfidf"])

# Load npz file
data = np.load('/kaggle/working/tfidf_embeddings.npz')
tfidf_embeddings = data['embeddings']

# Create and add to FAISS index
index = faiss.IndexFlatL2(tfidf_embeddings.shape[1])
index.add(tfidf_embeddings)

# Save index
faiss.write_index(index, 'faiss_tfidf.index')
    
# Sentence Transformer
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
sbert_vec = sbert_model.encode(df["all_text_info"].tolist(), show_progress_bar=True)
embeddings["sbert"] = sbert_vec.astype('float32')
index = faiss.IndexFlatL2(sbert_vec.shape[1])
index.add(embeddings["sbert"])
faiss.write_index(index, f"faiss_sbert.index")


def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return np.array(response['data'][0]['embedding'], dtype=np.float32)
    except Exception as e:
        print(f"Error with text: {text[:30]}... | {e}")
        return None,None




openai.api_key = os.environ['OPENAI_KEY']

EMBEDDING_DIM = 1536  # Expected OpenAI embedding size

def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return np.array(response['data'][0]['embedding'], dtype=np.float32)
    except Exception as e:
        print(f"Error with text: {text[:30]}... | {e}")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)  # Return zeros on failure

def generate_embeddings_with_tqdm(text_list, max_threads=8):
    embeddings = [None] * len(text_list)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(get_openai_embedding, text): idx for idx, text in enumerate(text_list)}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Embedding texts"):
            idx = futures[future]
            embedding = future.result()
            embeddings[idx] = embedding
    return np.vstack(embeddings)

openai_vecs = generate_embeddings_with_tqdm(df["all_text_info"], max_threads=8)

assert openai_vecs.shape[1] == EMBEDDING_DIM, f"Embedding size mismatch. Got {openai_vecs.shape[1]} instead of {EMBEDDING_DIM}"

# Save embeddings
np.save("openai_embeddings.npy", openai_vecs)

# Save FAISS index
index = faiss.IndexFlatL2(EMBEDDING_DIM)
index.add(openai_vecs)
faiss.write_index(index, "faiss_openai.index")


# Save metadata
metadata = df[["show_id", "all_text_info"]]
metadata.to_csv("movie_metadata.csv", index=False)


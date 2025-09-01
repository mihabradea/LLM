# retriever.py
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-large",
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("book_summaries", embedding_function=openai_ef)

def retrieve_candidates(query: str, k: int = 4):
    res = collection.query(query_texts=[query], n_results=k)
    docs   = res["documents"][0]
    metas  = res["metadatas"][0]
    titles = [m["title"] for m in metas]
    return [{"title": t, "short_summary": d} for t, d in zip(titles, docs)]

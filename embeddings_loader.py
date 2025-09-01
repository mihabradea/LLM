# embeddings_loader.py (varianta pentru ChromaDB >= 0.5)
import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from book_summaries import book_summaries

# 1) Cheia OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Lipsește OPENAI_API_KEY din .env")

# 2) Client Chroma nou (persistență pe disc)
client = chromadb.PersistentClient(path="./chroma_db")

# 3) Funcția de embedding (OpenAI)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-large",
)

# 4) Colecția (cu embedding function atașată)
collection = client.get_or_create_collection(
    name="book_summaries",
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"},  # opțional, dar util
)

# 5) Pregătim datele
ids = [f"book_{i}" for i in range(len(book_summaries))]
documents = [b["short_summary"] for b in book_summaries]
metadatas = [{"title": b["title"]} for b in book_summaries]

# 6) Curățăm intrările existente cu aceleași IDs (rulare repetată)
try:
    collection.delete(ids=ids)
except Exception:
    pass  # prima rulare nu are ce șterge

# 7) Adăugăm documentele (Chroma va calcula embeddings cu OpenAI)
print("🔄 Încarc datele și calculez embeddings cu OpenAI...")
collection.add(ids=ids, documents=documents, metadatas=metadatas)
print("✅ Datele au fost adăugate în colecția Chroma `book_summaries`.")

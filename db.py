### importing the libraries :
import chromadb 
from sentence_transformers import SentenceTransformer
import os 
# ------------------------------------------------------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
DATA_PATH = os.path.join(BASE_DIR, "data")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="my_docs")

documents = []
ids = []

for filename in os.listdir(DATA_PATH):
    if filename.endswith(".txt"):
        filepath = os.path.join(DATA_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            documents.append(content)
            ids.append(filename)

collection.add(
    documents=documents,
    ids=ids
)
print("database created successfully")
print("Total items in collection:", collection.count())
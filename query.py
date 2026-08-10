import chromadb 

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(name="my_docs")

query="Does this person have experience for machine learning and tensoflow"


results = collection.query(
    query_texts=[query],
    n_results=3
)


for i, (doc_id, doc, distance) in enumerate(zip(results['ids'][0], results['documents'][0], results['distances'][0])):
    print(f"\n--- Rank {i+1} ---")
    print(f"Resume: {doc_id}")
    print(f"Distance (lower = more similar): {distance:.4f}")
    print(f"Preview: {doc[:150]}...")
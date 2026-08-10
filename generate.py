import chromadb
import os 
import ollama

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="my_docs")

query = "Does this person have experience with machine learning and TensorFlow?"


results = collection.query(
    query_texts=query,
    n_results=1
)

retrieved_resume = results['documents'][0][0]
retrieved_id = results["ids"][0][0]


print(f"retrieved resume : {retrieved_id}\n")

prompt=f""" Based on the resume answer the questions : 
        Resume:
        {retrieved_resume}

        Question: {query}

        Give a clear reason why this document was chosen."""

response = ollama.chat(
    model= "llama3.2:3b",
    messages=[{"role" :"user" , "content":prompt}]
)

print("--- Answer ---")
print(response['message']['content'])
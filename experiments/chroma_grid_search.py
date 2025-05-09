import csv
import os
import chromadb
from chromadb.utils import embedding_functions
from sklearn.metrics import accuracy_score

import pandas as pd
df = pd.read_csv("input_questions.csv")

chunk_sizes = [1000, 3500, 7200]
overlaps = [0.1, 0.15, 0.2]
results = []

client = chromadb.Client()
embedding_fn = embedding_functions.DefaultEmbeddingFunction()


def grid_search():
    base_text = ""
    txt_folder = "txts"
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(txt_folder, filename), "r", encoding="utf-8") as f:
                base_text += f.read() + "\n"


    def chunk_text(text, chunk_size, overlap_ratio):
        overlap = int(chunk_size * overlap_ratio)
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks

    for chunk_size in chunk_sizes:
        for overlap_ratio in overlaps:
            chunks = chunk_text(base_text, chunk_size, overlap_ratio)

            collection_name = f"test_{chunk_size}_{int(overlap_ratio * 100)}"
            existing_collections = [col.name for col in client.list_collections()]
            if collection_name in existing_collections:
                client.delete_collection(collection_name)

            collection = client.create_collection(name=collection_name, embedding_function=embedding_fn)

            for i, chunk in enumerate(chunks):
                collection.add(documents=[chunk], ids=[str(i)])

            correct = 0
            for idx, row in df.iterrows():
                query = row['question']
                desired = row['desired answer']

                results_list = collection.query(query_texts=[query], n_results=1)
                retrieved = results_list['documents'][0][0]

                if desired.lower() in retrieved.lower():
                    correct += 1

            accuracy = correct / len(df)
            results.append({
                "Chunk_size": chunk_size,
                "Overlap": f"{int(overlap_ratio * 100)}%",
                "Accuracy": round(accuracy, 4)
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv("chroma_grid_search.csv", index=False)


def main():
    grid_search()

if __name__ == '__main__':
    main()

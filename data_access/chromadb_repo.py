import chromadb
from chromadb.utils import embedding_functions
import os
from transformers import AutoTokenizer
from tqdm import tqdm

chroma_client = chromadb.PersistentClient(path="/home/grundy/PycharmProjects/diplo/chroma_db/storage")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="HIT-TMG/KaLM-embedding-multilingual-mini-v1"
)
tokenizer = AutoTokenizer.from_pretrained("HIT-TMG/KaLM-embedding-multilingual-mini-v1")

def get_or_create_collection(name):
    try:
        collection = chroma_client.get_collection(name=name, embedding_function=embedding_function)
        print(f"Collection '{name}' already exists")
    except chromadb.errors.InvalidCollectionException:
        collection = chroma_client.create_collection(name=name, embedding_function=embedding_function)
        print(f"Collection '{name}' created successfully")
    return collection

def split_text(text, max_length=7200, overlap=0.15):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    
    if len(tokens) <= max_length:
        return [text]
    
    stride = int(max_length * (1 - overlap))
    chunks = []
    
    for i in range(0, len(tokens), stride):
        chunk = tokens[i:i + max_length]
        chunks.append(tokenizer.decode(chunk, skip_special_tokens=True))
    
    return chunks

def add_documents(path_to_folder):
    collection = get_or_create_collection("iee")
    documents = []
    ids = []
    metadatas = []

    for filename in os.listdir(path_to_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(path_to_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            chunks = split_text(text)
            
            if len(chunks) == 1:
                documents.append(chunks[0])
                ids.append(os.path.splitext(filename)[0])
                metadatas.append({"source": filename})
            else:
                for i, chunk in enumerate(chunks, 1):
                    documents.append(chunk)
                    ids.append(f"{os.path.splitext(filename)[0]}_{i:03d}")
                    metadatas.append({"source": filename, "chunk": i})

    if documents:
        collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Added {len(documents)} documents to the collection")
    else:
        print("No documents to add")

    print(f"Collection '{collection.name}' now contains {collection.count()} documents")


def get_similar_documents(query, n=1):
    collection = chroma_client.get_collection("iee", embedding_function=embedding_function)
    results = collection.query(
        query_texts=[query],
        n_results=n,
    )

    return results


if __name__ == '__main__':
    #add_documents('../data/txts')
    print(get_similar_documents('What is the Email of Mr. Goulianas?'))

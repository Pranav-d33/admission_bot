import json
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

class SentenceTransformerEmbeddings(Embeddings):
    """
    Wrapper class to make SentenceTransformer compatible with LangChain embeddings interface.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        :param model_name: Name of the SentenceTransformer model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        """
        Embed a list of documents.
        
        :param texts: List of text strings to embed
        :return: List of embeddings
        """
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text):
        """
        Embed a single query text.
        
        :param text: Text to embed
        :return: Embedding for the text
        """
        return self.model.encode(text).tolist()

def load_chunks(file_path):
    """
    Load chunks from a JSON file.
    
    :param file_path: Path to the JSON file containing chunks
    :return: List of chunks
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading chunks: {e}")
        return []

def embed_and_store_chunks(chunks, db_path="vector_db"):
    """
    Embed chunks and store them in a Chroma vector database.
    
    :param chunks: List of chunks to embed and store
    :param db_path: Path to store the vector database
    :return: Chroma vector store
    """
    # Check if chunks are empty
    if not chunks:
        print("No chunks to process.")
        return None

    # Create custom embeddings wrapper
    try:
        embeddings = SentenceTransformerEmbeddings()
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        return None

    # Convert chunks into LangChain Document objects
    documents = [
        Document(
            page_content=chunk.get("page_content", ""), 
            metadata=chunk.get("metadata", {})
        ) 
        for chunk in chunks
    ]

    # Initialize Chroma vector store
    try:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=db_path,
            collection_name="college_data"
        )
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

    print(f"Successfully embedded and stored {len(documents)} chunks.")
    return vector_store

def main():
    """
    Main function to orchestrate chunk loading and embedding.
    """
    # Load chunked data
    chunk_file_path = "chunks.json"
    chunks = load_chunks(chunk_file_path)

    # Embed and store chunks
    vector_db_path = "vector_db"
    vector_store = embed_and_store_chunks(chunks, db_path=vector_db_path)

    if vector_store:
        print(f"Chunks embedded and stored successfully in '{vector_db_path}'.")

if __name__ == "__main__":
    main()
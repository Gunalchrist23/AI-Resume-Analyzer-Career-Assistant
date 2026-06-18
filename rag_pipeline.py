import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Global vector store instance
_vector_store = None

def init_rag_pipeline(kb_path="career_knowledge_base.txt", persist_directory="./chroma_db"):
    """
    Initializes the RAG pipeline by loading the knowledge base,
    creating embeddings, and storing them in ChromaDB.
    """
    load_dotenv(override=True)
    global _vector_store

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("Please configure a valid GROQ_API_KEY in the .env file.")

    # Using standard local HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    marker_path = os.path.join(persist_directory, "hf_marker.txt")

    # If ChromaDB directory exists but doesn't have the HuggingFace marker,
    # delete it to prevent dimension mismatches.
    if os.path.exists(persist_directory):
        if not os.path.exists(marker_path):
            print("Detected old vector store. Resetting ChromaDB for HuggingFace embeddings...")
            import shutil
            try:
                shutil.rmtree(persist_directory)
            except Exception as e:
                print(f"Warning: Could not remove old ChromaDB directory: {e}")

    # If ChromaDB already has data, just load it
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("Loading existing ChromaDB...")
        _vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        return _vector_store

    print("Creating new ChromaDB from knowledge base...")
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base '{kb_path}' not found.")

    # 1. Load document
    loader = TextLoader(kb_path, encoding='utf-8')
    documents = loader.load()

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\nROLE:", "\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents)

    # 3. Create vector store — ChromaDB 0.4+ persists automatically; no .persist() needed
    _vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    # Write marker file to indicate it is a HuggingFace store
    try:
        os.makedirs(persist_directory, exist_ok=True)
        with open(marker_path, "w") as f:
            f.write("huggingface")
    except Exception as e:
        print(f"Warning: Could not write marker file: {e}")

    return _vector_store


def get_retriever():
    """Returns the retriever for the RAG pipeline."""
    global _vector_store
    if _vector_store is None:
        _vector_store = init_rag_pipeline()
    return _vector_store.as_retriever(search_kwargs={"k": 3})
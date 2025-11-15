from langchain.tools import tool
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun

from ..utils.main_functions import load_config
from dotenv import load_dotenv

import os

config = load_config("config.yaml")
load_dotenv()
PERSIST_DIR = config["data_paths"]["vector_store_path"]
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))



def load_vector_store(persist_dir):
    model_name = config["models"]["embedding"]["name"]

    # Get api key from .env
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY is missing. Please set it in your .env file.")
    
    embeddings = CohereEmbeddings(model=model_name, cohere_api_key=api_key)


    return FAISS.load_local(
            persist_dir,
            embeddings=embeddings,
            allow_dangerous_deserialization=True)


@tool("RAG", return_direct=False)
def RAG_tool(query: str, k: int = 2) -> str:
    """Retrieve relevant knowledge base entries using vector similarity search."""
    try:

        vector_store_path = os.path.join(base_dir, PERSIST_DIR)
        print(f"RAG Tool: Loading vector store from {vector_store_path}")
        vector_store = load_vector_store(vector_store_path)
        results = vector_store.similarity_search(query, k=k)
        context = "\n\n".join([res.page_content for res in results])
        return f"🔍 Retrieved context:\n{context}"
    except Exception as e:
        return f"[ERROR] Error performing RAG search: {e}"


search = DuckDuckGoSearchRun()

def get_all_tools():
    """Return a combined list of all tools for the agent."""
    return [RAG_tool, search]

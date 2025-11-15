import os
import pandas as pd
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from ..utils.main_functions import load_config


def load_and_sample_dataframe(csv_path, sample_size=10):
    print(f"[Loading DataFrame from: {csv_path}")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
        print(f" Sampled {sample_size} rows from the DataFrame.")
    else:
        print(f" Using all {len(df)} rows from the DataFrame (less than requested sample size).")
    
    return df


def create_movie_documents(df):
    print(f" Creating documents from {len(df)} movies...")
    documents = []
    
    for idx, row in df.iterrows():
        # Create rich document with all information
        content = f"""Title: {row['Title']}

Plot: {row['Plot_Clean'][:4000]}

Cast: {row['Cast']}

Director: {row['Director']}

Genre: {row['Genre']}"""
    
        doc = Document(page_content=content)
        documents.append(doc)
    
    print(f"Created {len(documents)} movie documents.")
    return documents


def create_cohere_embeddings(model_name):
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("[WARN] COHERE_API_KEY not found. Please check your .env file.")
    print(f" Creating Cohere embeddings (model: {model_name})...")
    return CohereEmbeddings(model=model_name, cohere_api_key=api_key)


def build_and_save_faiss_index(docs, embeddings, save_path):
    print("Building FAISS vector store...")
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(save_path)
    print(f"FAISS index saved to: {save_path}")


def build():
    load_dotenv()
    config = load_config()

    csv_path = config["data_paths"]["csv_path"]  
    vector_store_path = config["data_paths"]["vector_store_path"]
    model_name = config["models"]["embedding"]["name"]
    sample_size = config["models"]["embedding"]["sample_size"]
    # Load and sample the DataFrame
    df = load_and_sample_dataframe(csv_path, sample_size)
    
    # Create documents from DataFrame
    docs = create_movie_documents(df)
    
    # Create embeddings
    embeddings = create_cohere_embeddings(model_name)
    
    # Build and save FAISS index
    build_and_save_faiss_index(docs, embeddings, vector_store_path)











    
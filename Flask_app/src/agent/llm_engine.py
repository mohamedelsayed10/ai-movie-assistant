import os
from langchain_google_genai import ChatGoogleGenerativeAI
from ..utils.main_functions import load_config
from dotenv import load_dotenv



def get_llm(config_path="config.yaml"):
    config = load_config(config_path)
    load_dotenv()

    model_name = config["models"]["llm"]["name"]
    temperature = config["models"]["llm"].get("temperature", 0.1)

    google_api_key = os.getenv("GOOGLE_API_KEY") 

    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=google_api_key,
        temperature=temperature
    )

    return llm

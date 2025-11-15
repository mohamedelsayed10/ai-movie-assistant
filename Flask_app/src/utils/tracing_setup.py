import os
from dotenv import load_dotenv
from .main_functions import load_config

def setup_tracing():
    """
    Load LangSmith tracing configuration and set environment variables
    if tracing is enabled in the config.
    """
    # Load .env and config
    load_dotenv()
    config = load_config("config.yaml")

    tracing_config = config.get("tracing", {})

    # Check if tracing is enabled
    if tracing_config.get("enabled", False):
        print("[TRACE] Tracing is enabled. Setting environment variables...")

        # Get values from config and env
        endpoint = tracing_config.get("end_point")
        project = tracing_config.get("project_name")
        api_key = os.getenv("LANGSMITH_API_KEY")

        # Validate required values
        if not api_key:
            raise ValueError("[TRACE ERROR] LANGSMITH_API_KEY is missing in .env file")

        if not endpoint or not project:
            raise ValueError("[TRACE ERROR] Missing tracing config fields in config.yaml")

        # Export environment variables
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_ENDPOINT"] = endpoint
        os.environ["LANGSMITH_API_KEY"] = api_key
        os.environ["LANGSMITH_PROJECT"] = project

        print(f"[TRACE] LANGSMITH_ENDPOINT = {endpoint}")
        print(f"[TRACE] LANGSMITH_PROJECT  = {project}")
        print("[TRACE] Tracing setup completed successfully.\n")
    else:
        print("[TRACE] Tracing is disabled in config.yaml.\n")

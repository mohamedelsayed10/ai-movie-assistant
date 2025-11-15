import yaml
import os
import sqlite3
#-------------------
# Loading Functions 
#-------------------
def load_config(config_path="config.yaml"):
    """Load YAML configuration."""
    # If the config_path doesn't exist, try looking in the config directory
    if not os.path.exists(config_path):
        # Build path to config directory relative to this file
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(os.path.dirname(current_dir))
        full_config_path = os.path.join(project_root, "config", config_path)
        if os.path.exists(full_config_path):
            config_path = full_config_path
        else:
            raise FileNotFoundError(f"Config file not found: {config_path} or {full_config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)




# read prompt from file
def load_prompt(prompt_path):
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
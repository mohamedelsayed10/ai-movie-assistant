

#  API Key Setup Guide

This document explains how to obtain and securely use API keys for all required services: **ElevenLabs**, **Google Gemini**, **MailerSend**, **LangSmith**, and **Cohere**.

----------

## 1. 🎙️ ElevenLabs API (Text-to-Speech)

### Steps to get your API key

1.  Go to [ElevenLabs.io](https://elevenlabs.io/developers).
    
2.  Sign in or create an account.
    
3.  Open your **Dashboard → Settings → API Keys**.
    
4.  Click **Create API Key** and name it.
    
5.  Copy it once shown — it won’t appear again.
    


----------

## 2. Google Gemini API (Generative Language Model)

### Steps to get your API key

1.  Go to [Google AI Studio](https://aistudio.google.com/).
    
2.  Log in with your Google account.
    
3.  Create or select a project.
    
4.  Click **Get API Key** under the “API keys” section.
    
5.  Copy and store it    

----------



## 3.  LangSmith API (LangChain Observability)

### Steps to get your API key (from [LangSmith Docs](https://docs.langchain.com/langsmith/create-account-api-key))

1.  Sign up for a free account at [smith.langchain.com](https://smith.langchain.com/).
    
2.  Once logged in, go to **Settings → API Keys**.
    
3.  Choose the key type:
    
    -   **Service Key** (for apps)
        
    -   **Personal Access Token** (for users)
        
4.  Choose whether it’s scoped to a **workspace** or **organization**.
    
5.  (Optional) Set expiration and permissions.
    
6.  Click **Create API Key** and copy it immediately — it’s only shown once.
    
7.  Store in `.env`
    ```
    


----------

## 4.  Cohere API (Embeddings, Text Generation, NLP)

### Steps to get your API key

1.  Create an account at [Cohere Dashboard](https://dashboard.cohere.com/).
    
2.  Go to **API Keys**.
    
3.  Copy your default key or create a new one.
    
4.  Store it safely

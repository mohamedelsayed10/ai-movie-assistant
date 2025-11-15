
# **AI Movie Assistant System**

An intelligent AI-powered movie platform combining **natural language processing**, **machine learning**, and **retrieval-augmented generation (RAG)** to provide:

* **Genre Prediction:** Multi-label classification using fine-tuned DistilBERT
* **Plot Summarization:** Non-spoiler summaries using LLMs (Gemini & Gemma-3)
* **Conversational AI:** Interactive Q&A with reasoning and memory
* **Movie Search:** Semantic retrieval with FAISS vector database
* **Voice Interaction:** Speech-to-text and text-to-speech for a natural interface


---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data](#data)
- [Technical Components](#technical-components)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)

## Overview


The system consists of multiple interconnected components:

- **Preprocessing Pipeline** (`Preprocessing_EDA.ipynb`): Performs data cleaning, standardization, and exploratory data analysis on movie plot data
- **Genre Prediction Models** (`Genre_Models.ipynb`): Implements multiple approaches for multi-label genre classification including classical ML, embedding-based models, and fine-tuned transformers
-  **Plot Summarization – Open/Closed Models** (`Generate_Summaries_Open_Close_Source_Models.ipynb`): Generates concise summaries using open-source and closed-source LLMs
- **Plot Summarization – Fine-Tuning** (`finetuning_Summarization_model.ipynb`): Uses fine-tuned Gemma-3 model for domain-specific, non-spoiler summaries

- **RAG & Conversational AI Agent** (`RAG_Search_and_QA_Agent.ipynb`): AI agent with memory, internet search, and retrieval-augmented generation (RAG) for answering movie-related queries

- **Web Interface** (`flask_app/`): Flask-based application with voice interaction, genre prediction, and summarization features




## Project Structure

```
├── Preprocessing_EDA.ipynb     
├── Genre_Models.ipynb       
├── finetuning_Summarization_model.ipynb  
├── Generate_Summaries_Open_Close_Source_Models.ipynb
├── RAG_Search_and_QA_Agent.ipynb    
└── README.md 

├── data/                     
│   ├── clean_wiki_movies.csv     
│   ├── wiki_movie_plots_deduped.csv # Raw data 

├── flask_app/     
│   ├── app.py                   
│   ├── requirements.txt         
│   ├── config/                    
│   ├── data/                       
│   ├── models/                    
│   ├── src/            
│   ├── static/                 
│   └── templates/                  
│   └── templates/                            
```



## Technical Components

### Data & Preprocessing  `Preprocessing_EDA.ipynb`:
- Handling of missing values and duplicates
- Processed genres 
- Standardization of genre labels and consolidation of similar categories
- Cleaned movie plots 
- Complete preprocessing pipeline  
- visualized genre and actor/director trends and other EDA.

###  Genre Prediction Approaches `Genre_Models.ipynb`:

### 1. Prepration
- created multi-label targets
- Iterative stratified train-test split

#### 2. Classical ML + TF-IDF
- Multinomial Naive Bayes
- Random Forest

#### 3. Pretrained Embeddings + ML
- SentenceTransformer embeddings + XGBoost

#### Transformer Fine-Tuning
- DistilBERT 
- RoBERTa 

###  Plot Summarization
Implemented in `Generate_Summaries_Open_Close_Source_Models.ipynb`
- Generate concise, spoiler-free summaries from movie plots using
 Gemini AI & local vLLM 

and in `finetuning_Summarization_model.ipynb`
- Fine-tuned Gemma-3-270M → Domain-specific, non-spoiler

###  Search & Q&A- Agent `RAG_Search_and_QA_Agent`:
- FAISS Vector DB → Semantic movie search
- Vector database creation using FAISS and Hugging Face embeddings
- RAG Agent → Memory + internet search tools
- LangGraph-based conversational agent with RAG and web search tools
- Integration with DuckDuckGo search and Google Gemini

###  Web & App
The Flask application provides a user-friendly interface with:
- Flask-based AI Movie Assistant
- Conversational AI with voice interaction powered by ElevenLabs
- Plot summarization functionality
- Genre prediction tool with plot input
- Responsive design with multiple specialized pages
- API endpoints for backend functionality


###  Resources
- **Best Genre Classification Model**: [Download from Google Drive](https://drive.google.com/drive/folders/1dRT1fTKETS0n2jarb7BSdnE6j3z5K1Ka?usp=sharing) under `flask_app/models`
- **Fine-tuned Model**: [Download from Google Drive](https://drive.google.com/file/d/1PHqIuvrLILrGtOwjR-dwVIxHQ7OghDLn/view?usp=sharing)
- **Dataset**: [Clean Wiki Movies Dataset](https://drive.google.com/file/d/1JUnPKUh3AqoB-5qtwIZtaYhblq1usw7v/view?usp=sharing) under `data dir`


## Installation

Installation instructions are provided within each notebook and in the Flask application's setup files. Please refer to the individual components for specific installation requirements and setup procedures:

- Jupyter notebooks have required library installations at the top
- The Flask application has dependencies listed in `flask_app/requirements.txt`
- Environment variables are detailed in the Flask application's documentation
---
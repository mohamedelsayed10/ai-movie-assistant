# AI Movie Assistant Application

## Overview

The AI Movie Assistant Application is a  conversational AI system designed to provide movie-related assistance through natural language interactions. The system combines large language models with specialized tools to provide information through document search capabilities and offer AI-powered movie analysis features.

### Key Features

- **Voice Interaction**: Speech-to-text and text-to-speech capabilities powered by ElevenLabs
- **Conversational AI**: Advanced LLM-powered agent with reasoning and action capabilities
- **Document Search**: RAG functionality for searching DF documents with semantic understanding
- **Genre Prediction**: AI-powered movie genre classification using fine-tuned DistilBERT transformer
- **Plot Summarization**: Intelligent plot summarization using Google Gemini AI
- **Web Interface**: Responsive web-based interface with multiple specialized pages

## Project Structure

```
├── config/                 
│   └── config.yaml
├── data/                   
│   ├── MOVIES_PLOT.CSV/               # Documents for RAG
│   └── vector_store/       # FAISS vector store
│   API_setup.md 
│   Installation_Guide.md 
├── models/         
│   ├── distilbert_genre_classifier/ 
│   ├── mlb_encoder.pkl     
│   └── genre_info.json     
├── src/                    # Source code
│   ├── agent/              # Chatbot interface and speech processing
│   ├── builders/           # Database and vector store builders
│   │   └── build_vectorstore.py
│   ├── models/             ML model wrappers
│   │   ├── __init__.py
│   │   ├── genre_predictor.py    # Genre prediction model
│   │   └── plot_summarizer.py    # Plot summarization model
│   ├── tools/              # Document search tools
│   │   ├── __init__.py
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── agent_utils.py
│   │   ├── main_functions.py
│   │   ├── markdown_utils.py
│   │   └── tracing_setup.py
│   └── app.py              # Main application entry point
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/              # HTML templates
│   ├── home.html           # Landing page
│   ├── chat.html          # Chat interface
│   ├── genre_prediction.html   
│   └── plot_summarizer.html   
├── .env                    # Environment variables
├── README.md               # Main project documentation
├── requirements.txt.                # Python dependencies
```
m



## Getting Started

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (optional, for faster inference)
- Google API key (for plot summarization)
- ElevenLabs API key (for voice features)

### Installation

For complete installation instructions, see our [Installation Guide](Installation_Guide.md).

## How to Run

After completing the installation, follow these steps to run the application:

### Starting the Application

1. Ensure you have set up your environment variables and configuration
2. Activate your virtual environment:
```bash
# On Windows
myenv\Scripts\activate

# On macOS/Linux
source myenv/bin/activate
```

3. Run the main application:
```bash
python src/app.py
```

s

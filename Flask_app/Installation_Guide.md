# Installation Guide

This guide provides step-by-step instructions to set up and run the AI Chatbot Application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.9 or higher
- Git
- pip (Python package installer)
- Virtual environment tool (e.g., `venv` or `virtualenv`)



## Step-by-Step Installation


### Project Structure

#### Models
Place all models in the **models** folder inside the Drive link:

[Models Link](https://drive.google.com/drive/folders/1dRT1fTKETS0n2jarb7BSdnE6j3z5K1Ka?usp=sharing)

---

#### Data
Place the dataset file in the **data** folder:


[Data Link](https://drive.google.com/file/d/1JUnPKUh3AqoB-5qtwIZtaYhblq1usw7v/view?usp=sharing)



### 1. Create a Virtual Environment

```bash
# On Windows
python -m venv myenv
myenv\Scripts\activate

# On macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r recruitments.txt
```


### 4. Environment Configuration

1. Create an environment file:
```bash
.env
```

2. Update `.env` with your API keys:
```bash
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

GOOGLE_API_KEY=your_google_api_key_here  # Key for Google Generative AI

COHERE_API_KEY=your_cohere_api_key_here  # Key for embeddings


LANGCHAIN_API_KEY=your_langchain_api_key_here  # Key for LangSmith tracing (optional)
```

**see our API Key Setup Guide [API_Key_Setup_Guide](API_Key_Setup_Guide.md)**.


### 5. Application Configuration

The application uses `config/config.yaml` for speech and model configuration:







## Running the Application

### Development Mode

```bash
python src/app.py
```

The application will start server:
-  UI: http://localhost:8001

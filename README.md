# AI Career & Interview Assistant

An AI-powered career and technical interview assistant built as part of my Generative AI internship capstone project.

## Project Overview

The AI Career & Interview Assistant uses a Large Language Model (LLM) to help users with career guidance, Computer Science learning, programming questions, and technical interview preparation.

The project is being developed step by step to demonstrate practical Generative AI concepts including LLM APIs, prompt engineering, RAG, tools, and AI agents.

## Current Features

* AI-powered conversational assistant
* Hugging Face LLM API integration
* Prompt engineering using system instructions
* Conversation history
* Career guidance
* Programming and Computer Science assistance
* Technical interview preparation
* Gradio-based user interface
* Environment variable based API authentication

## Technology Stack

* Python
* Hugging Face Inference API
* Llama 3.1 8B Instruct
* Gradio
* python-dotenv

## Current Architecture

```text
User
  ↓
Gradio Interface
  ↓
Python Application
  ↓
System Prompt + Conversation History
  ↓
Hugging Face API
  ↓
Llama 3.1 8B Instruct
  ↓
AI Response
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-career-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv312
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv312\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the environment file

Create a `.env` file in the project directory:

```text
HF_TOKEN=your_hugging_face_token
```

Do not upload the `.env` file to GitHub.

### 6. Run the application

```bash
python app.py
```

The Gradio application will then be available locally.

## Project Status

### Day 26 — Core Application

* [x] LLM API integration
* [x] Hugging Face authentication
* [x] System prompt
* [x] Conversation history
* [x] Gradio interface
* [x] Local application testing

### Upcoming

* [ ] RAG
* [ ] Document processing
* [ ] Embeddings
* [ ] Vector database
* [ ] Tool integration

# 🤖 AI Career & Interview Assistant

An AI-powered Career and Interview Assistant built as a Generative AI capstone project.

The application combines a Large Language Model (LLM), prompt engineering, Retrieval-Augmented Generation (RAG), embeddings, a FAISS vector database, tools, and an agent-based routing workflow.

## 🚀 Features

* 💬 AI chatbot with conversation history
* 🤖 Hugging Face LLM integration
* 📄 PDF document upload
* 🔎 Retrieval-Augmented Generation (RAG)
* 🧠 Sentence-transformer embeddings
* 🗄️ FAISS vector database
* 🧮 Calculator tool
* 📚 Interview-topic generation tool
* 🧭 Rule-based agent/router
* 🎨 Gradio web interface
* ⚠️ Basic error handling
* 🔐 Environment-variable based API authentication

## 🏗️ Architecture
![AI Career & Interview Assistant Architecture](architecture.png)

```text
User
  │
  ▼
Gradio Interface
  │
  ▼
Agent / Router
  │
  ├──────────────► Calculator Tool
  │
  ├──────────────► Interview Topics Tool
  │
  ├──────────────► RAG Pipeline
  │                    │
  │                    ▼
  │                 PDF File
  │                    │
  │                    ▼
  │                Text Chunks
  │                    │
  │                    ▼
  │                Embeddings
  │                    │
  │                    ▼
  │                FAISS DB
  │                    │
  │                    ▼
  │             Relevant Context
  │
  └──────────────► LLM
                       │
                       ▼
                   AI Response
```

## 🧠 How RAG Works

The application allows users to upload a PDF and ask questions about its contents.

The RAG pipeline works as follows:

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Embeddings
 ↓
FAISS Vector Database
 ↓
Similarity Search
 ↓
Relevant Chunks
 ↓
LLM
 ↓
Answer
```

This allows the application to retrieve relevant information from the uploaded document before generating an answer.

## 🛠️ Technologies Used

* Python
* Hugging Face Inference API
* Llama 3.1 8B Instruct
* Gradio
* PyPDF
* Sentence Transformers
* FAISS
* NumPy
* python-dotenv

## 📁 Project Structure

```text
ai-career-assistant/
│
├── app.py
├── rag.py
├── tools.py
├── test_rag.py
├── requirements.txt
├── README.md
└── .gitignore
```

Private/local files:

```text
.env
resume.pdf
.venv312/
```

These files are excluded from the public repository.

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd ai-career-assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv312
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv312\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

Add your Hugging Face token:

```text
HF_TOKEN=your_huggingface_token
```

Do not upload the `.env` file to GitHub.

### 7. Run the application

```bash
python app.py
```

The Gradio application will open locally.

## 🧪 Example Queries

### General AI

```text
What is machine learning?
```

### Calculator Tool

```text
Calculate 9.05 * 10
```

### Interview Tool

```text
Give me Python interview topics
```

### RAG

Upload a resume or another PDF and ask:

```text
What projects are mentioned in my resume?
```

## 🎯 Purpose of the Project

This project was developed as a Generative AI capstone project to demonstrate practical understanding of:

* LLM APIs
* Prompt engineering
* Conversation history
* RAG
* Embeddings
* Vector databases
* Semantic search
* Tool integration
* Agent-based routing
* Generative AI application development

## 🔮 Future Improvements

Possible future improvements include:

* Support for multiple documents
* Better document chunking
* Improved retrieval techniques
* Source citations in answers
* More tools
* LLM-based tool selection
* Authentication
* Persistent vector databases
* Improved UI
* Cloud deployment

## 👨‍💻 Author

Syed Abdul Wasay

B.Tech in Artificial Intelligence and Machine Learning

Generative AI Capstone Project

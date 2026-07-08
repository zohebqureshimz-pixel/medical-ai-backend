# 🩺 AI Medical Assistant Backend

An AI-powered Retrieval-Augmented Generation (RAG) backend built with **FastAPI**, **Google Gemini**, **FAISS**, and **BM25**. The system processes medical PDF documents, retrieves the most relevant information using hybrid search, and generates context-aware answers through Google's Gemini API.

> **⚠️ Disclaimer:** This project is intended for educational and portfolio purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment.

---

# 🚀 Overview

This backend enables users to upload medical PDF documents and ask natural language questions. Instead of relying solely on a Large Language Model, it retrieves relevant information from the uploaded documents before generating an answer.

The retrieval pipeline combines:

* **Semantic Search (FAISS)** for contextual similarity
* **Keyword Search (BM25)** for exact term matching
* **Google Gemini API** for high-quality response generation

This hybrid RAG approach improves response relevance while reducing hallucinations compared to using an LLM alone.

---

# ✨ Features

* 📄 Medical PDF ingestion
* ✂️ Automatic document chunking
* 🧠 Sentence embedding generation
* 🔎 FAISS vector search
* 📚 BM25 keyword retrieval
* 🔀 Hybrid retrieval pipeline
* 🤖 Google Gemini API integration
* ⚡ FastAPI REST API
* 🐳 Docker support
* 🧩 Modular project architecture
* 📈 Easily extensible for additional document collections

---

# 🏗️ System Architecture

```text
                 Medical PDF
                      │
                      ▼
            PDF Text Extraction
                      │
                      ▼
              Document Chunking
                      │
                      ▼
        Sentence Transformer Embeddings
               │                  │
               ▼                  ▼
        FAISS Vector Index     BM25 Index
               │                  │
               └──────────┬───────┘
                          ▼
                 Hybrid Retrieval
                          ▼
            Context Construction
                          ▼
               Google Gemini API
                          ▼
                 Generated Answer
```

---

# 🛠️ Tech Stack

| Category            | Technology                               |
| ------------------- | ---------------------------------------- |
| Language            | Python                                   |
| API Framework       | FastAPI                                  |
| LLM                 | Google Gemini API                        |
| Vector Search       | FAISS                                    |
| Keyword Search      | BM25                                     |
| Embeddings          | Sentence Transformers (all-MiniLM-L6-v2) |
| Numerical Computing | NumPy                                    |
| Containerization    | Docker                                   |

---

# 📂 Project Structure

```text
.
├── app.py
├── ingestion.py
├── retriever.py
├── storage.py
├── models.py
├── requirements.txt
├── Dockerfile
├── chunks.pkl
├── bm25.pkl
└── .gitignore
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/zohebqureshimz-pixel/medical-ai-backend.git

cd medical-ai-backend
```

## Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Start the server

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 🐳 Running with Docker

Build the Docker image:

```bash
docker build -t medical-ai-backend .
```

Run the container:

```bash
docker run -p 8000:8000 medical-ai-backend
```

---

# 📡 API Endpoints

| Method | Endpoint  | Description                            |
| ------ | --------- | -------------------------------------- |
| POST   | `/upload` | Upload and process a medical PDF       |
| POST   | `/ask`    | Ask questions about uploaded documents |

---

# 🔄 Retrieval Pipeline

1. Upload a medical PDF.
2. Extract text from the document.
3. Split the content into manageable chunks.
4. Generate sentence embeddings.
5. Store embeddings in a FAISS index.
6. Build a BM25 keyword index.
7. Retrieve relevant context using hybrid search.
8. Send the retrieved context and user query to Google Gemini.
9. Return a context-aware response.

---

# 💡 Future Improvements

* Conversation memory
* User authentication
* Streaming AI responses
* Multi-document collections
* Source citation highlighting
* Evaluation metrics
* Role-based access
* Admin dashboard
* Cloud deployment
* CI/CD pipeline
* Unit and integration tests

---

# 📸 Screenshots

Add screenshots showing:

* FastAPI Swagger UI (`/docs`)
* PDF upload workflow
* AI-generated responses
* Docker deployment
* Retrieval pipeline (optional)

---

# 👨‍💻 Author

**Zoheb Qureshi**

GitHub: https://github.com/zohebqureshimz-pixel

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

# 🏥 AI Medical Assistant Backend (Multi-Tenant Hybrid RAG)

A production-oriented Retrieval-Augmented Generation (RAG) backend built with **FastAPI**, **Google Gemini 2.5 Flash**, **FAISS**, **BM25**, and **JWT Authentication**. 

The system enables secure, multi-tenant medical PDF ingestion, hybrid vector + keyword search retrieval, and grounded medical answer generation with exact page source citations.

> ⚠️ **Disclaimer:** This project is for educational and portfolio purposes only. It is not intended for clinical use or as a substitute for professional medical advice.

---

## ⚡ Key Features

* 🔐 **JWT Authentication & Security**: Password hashing via Bcrypt, OAuth2 bearer token authentication, and route protection.
* 🛡️ **Multi-Tenant User Isolation**: Per-user database record tracking (`User` & `Document` schemas) and isolated per-user FAISS/BM25 disk storage.
* 🔍 **Hybrid Retrieval Engine**:
  * **FAISS Vector Search**: Dense semantic search using `SentenceTransformer("all-MiniLM-L6-v2")` normalized L2 embeddings.
  * **BM25 Keyword Search**: Sparse exact keyword matching via `rank_bm25`.
* 🤖 **Gemini AI Generation**: Powered by `gemini-2.5-flash` with strict prompt engineering for zero hallucination context adherence.
* 📄 **Source Citations**: Returns exact document names, page numbers, and text snippet citations with every answer.
* 🐳 **Docker & Cloud Ready**: Fully containerized and optimized for 1-click deployment on **Render** or **Railway**.

---

## 🏗️ System Architecture

```text
                     +---------------------------+
                     |    Client Request (JWT)   |
                     +-------------+-------------+
                                   |
                                   v
                     +---------------------------+
                     |    FastAPI Auth Guard     |
                     +-------------+-------------+
                                   |
              +--------------------+--------------------+
              |                                         |
              v                                         v
   +--------------------+                    +--------------------+
   |  /upload PDF       |                    |  /ask Question     |
   +----------+---------+                    +----------+---------+
              |                                         |
              v                                         v
   +--------------------+                    +--------------------+
   | Overlapping Chunk  |                    | Hybrid Retrieval   |
   | & Sentence Embed   |                    | (FAISS + BM25)     |
   +----------+---------+                    +----------+---------+
              |                                         |
              v                                         v
   +--------------------+                    +--------------------+
   | Isolated Per-User  |                    | Gemini 2.5 Flash   |
   | Index Storage      |                    | Answer + Citations |
   +--------------------+                    +--------------------+
```

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework** | FastAPI, Uvicorn |
| **LLM & Embeddings** | Google Gemini (`google-genai`), SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Search Engines** | FAISS (`faiss-cpu`), BM25 (`rank-bm25`) |
| **Database & Auth** | SQLAlchemy, SQLite/PostgreSQL, Passlib (Bcrypt), PyJWT / Python-Jose |
| **PDF Ingestion** | PyMuPDF / PyPDF |
| **Deployment** | Docker, Render |

---

## 📂 Project Structure

```text
.
├── auth/
│   ├── database.py       # SQLAlchemy database session & engine
│   ├── models.py         # User and Document database tables
│   ├── dependencies.py   # JWT token authentication dependencies
│   ├── routes.py         # /auth/register and /auth/token routes
│   └── security.py       # Password hashing & JWT token creation
├── uploads/              # Isolated per-user uploaded PDFs
├── data/                 # Per-user FAISS index, BM25, and chunk storage
├── app.py                # Main FastAPI application & routes
├── ingestion.py          # PDF extraction & text chunking logic
├── retriever.py          # Hybrid RRF search implementation
├── storage.py            # Disk loader/saver for vector indices & metadata
├── models.py             # Pydantic request/response models
├── Dockerfile            # Container deployment specification
└── requirements.txt      # Python dependencies
```

---

## 📡 API Endpoints

| Method | Endpoint | Protection | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Public | Register a new user account |
| `POST` | `/auth/token` | Public | User login (returns JWT Bearer Token) |
| `GET` | `/profile` | 🔒 JWT | Fetch logged-in user details |
| `POST` | `/upload` | 🔒 JWT | Upload and index a medical PDF for current user |
| `GET` | `/documents` | 🔒 JWT | List all indexed documents for current user |
| `POST` | `/ask` | 🔒 JWT | Query user's indexed document via Hybrid RAG |

---

## 🚀 Local Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/zohebqureshimz-pixel/medical-ai-backend.git
cd medical-ai-backend
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_jwt_secret_key_here
```

### 4. Run Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Access Swagger API Docs at: `http://localhost:8000/docs`

---

## 🐳 Docker & Render Deployment

### Docker Setup
```bash
docker build -t medical-ai-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key medical-ai-backend
```

### Render Deployment
1. Connect repository to [Render Web Services](https://dashboard.render.com).
2. Set Environment to **Docker**.
3. Add Environment Variables (`GEMINI_API_KEY`, `SECRET_KEY`, `PORT=8000`).
4. Deploy!

---

## 👨‍💻 Author

**Zoheb Qureshi**  
GitHub: [@zohebqureshimz-pixel](https://github.com/zohebqureshimz-pixel)

from fastapi import FastAPI
from fastapi import UploadFile, File
import shutil
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
from rank_bm25 import BM25Okapi
from google import genai
from auth.routes import router as auth_router
from auth.dependencies import get_current_user
from auth.models import User , Document
from auth.database import SessionLocal
from fastapi import Depends

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2")
from ingestion import process_pdf
from models import QuestionRequest
from retriever import search
from storage import (
    load_index,
    save_index,
    load_chunks,
    save_chunks,
    load_bm25,
    save_bm25,
)

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" , "https://medical-ai-frontend-rho.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    index = load_index()
    chunks = load_chunks()
    bm25 = load_bm25()
    print("Existing index loaded.")
except:
    index = None
    chunks = []
    bm25 = None
    print("No previous index found.")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_BASE_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(
    UPLOAD_BASE_DIR,
    exist_ok=True
)

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    user_upload_dir = os.path.join(
    UPLOAD_BASE_DIR,
    f"user_{current_user.id}"
    )

    os.makedirs(
       user_upload_dir,
       exist_ok=True
    )

    pdf_path = os.path.join(
    user_upload_dir,
    file.filename
    )

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document_name = (file.filename)

    print("========== UPLOAD DEBUG ==========")
    print("FILE FILENAME:", repr(file.filename))
    print("DOCUMENT NAME:", repr(document_name))
    print("USER ID:", current_user.id)
    print("===================================")

    new_chunks = process_pdf(pdf_path)

    chunks = new_chunks


    embeddings = model.encode(
    [c["chunk"] for c in new_chunks],
    batch_size=32,
    show_progress_bar=False
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    faiss.normalize_L2(embeddings)

    
    index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

    index.add(
    embeddings
    )

    chunks = new_chunks

    tokenized_chunks = [
       chunk["chunk"].split()
       for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    save_index(
    index,
    current_user.id,
    document_name
    )

    save_chunks(
    chunks,
    current_user.id,
    document_name
    )

    save_bm25( 
    bm25,
    current_user.id,
    document_name
    )

    db = SessionLocal()

    document = Document(
        user_id=current_user.id,
        filename=file.filename,
        filepath=pdf_path
    )

    db.add(document)
    db.commit()
    db.close()

    return {
        "message": "PDF indexed successfully"
    }

client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/documents")
def get_documents(current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()

    db.close()

    return {
        "documents":[
            doc.filename
            for doc in documents
        ]
    }


@app.post("/ask")
def ask_question(
    data: QuestionRequest,
    current_user: User = Depends(get_current_user)
):

    index = load_index(
    current_user.id,
    data.document_name
    )

    chunks = load_chunks(
    current_user.id,
    data.document_name
    )

    bm25 = load_bm25(
    current_user.id,    
    data.document_name
    )


    if index is None:
        return {
        "answer": "Document not found"
    }


    results = search(
    data.question,
    index,
    chunks,
    bm25
    )

    context = "\n\n".join(
        chunk["chunk"]
        for chunk in results
    )

    prompt = f"""
You are a medical study assistant.

Answer ONLY using the provided context.

Format your response using proper Markdown.

Rules:
- Use headings (##) for sections when appropriate.
- Use '-' for bullet points (not •).
- Leave a blank line between headings and lists.
- Do NOT output plain text lists on a single line.
- Do not use outside knowledge.

If the answer is not in the context, reply exactly:

Information not found in retrieved context.

Context:
{context}

Question:
{data.question}
"""


    
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    )

    answer = response.text

    return {
        "question": data.question,
        "answer": answer,
        "sources": [
            {
                "document": chunk["document"],
                "page": chunk["page"],
                "text": chunk["chunk"]
            }
            for chunk in results
        ]
    }

@app.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email
    }
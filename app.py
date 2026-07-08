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

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global index  , chunks , bm25

    pdf_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    new_chunks = process_pdf(pdf_path)


    embeddings = model.encode(
        [c["chunk"] for c in new_chunks]
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    faiss.normalize_L2(embeddings)

    
    if index is None:
       index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    chunks.extend(new_chunks)

    tokenized_chunks = [
       chunk["chunk"].split()
       for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    save_index(index)
    save_chunks(chunks)
    save_bm25(bm25)

    return {
        "message": "PDF indexed successfully"
    }

client = genai.Client(api_key=GEMINI_API_KEY)


@app.post("/ask")
def ask_question(
    data: QuestionRequest
):

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


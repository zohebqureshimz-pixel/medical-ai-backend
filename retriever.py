from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import numpy as np
import faiss


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def search(query , index , chunks , bm25, k=5):
    embedding_query = model.encode([query])

    embedding_query = np.array(embedding_query).astype("float32")

    faiss.normalize_L2(embedding_query)

    faiss_k = 20
    bm25_k = 20
    final_k = 5
    
    distances, indices = index.search(
        embedding_query,
        faiss_k
    )
    query_tokens = query.lower().split()

    bm25_scores = bm25.get_scores(query_tokens)
    
    faiss_indices = indices[0]

    bm25_indices = np.argsort(
        bm25_scores
        )[::-1][:bm25_k]
    
    rrf = {}

    for rank , indx in enumerate(faiss_indices):
        rrf[indx] = (
            rrf.get(indx, 0)
        + 1 / (60 + rank)
    )
    
    for rank , indx in enumerate(bm25_indices):
        rrf[indx] = (
            rrf.get(indx , 0)
            + 1 / (60 + rank)
        )

    final_indices=sorted(
        rrf , key = rrf.get, reverse= True
    ) [:final_k]

    pairs = [
    (query, chunks[i]["chunk"])
    for i in final_indices
]
    score = reranker.predict(pairs)

    ranked = sorted(
    zip(final_indices, score),
    key=lambda x: x[1],
    reverse=True
)   
    
    top_indices = [
        indx for indx , score in ranked[:final_k]
    ]
    return [
        chunks[i]
        for i in top_indices
    ]    
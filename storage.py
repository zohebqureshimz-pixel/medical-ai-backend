import pickle
import faiss

def load_index():

    return faiss.read_index(
        "anatomy.index"
    )

def save_index(index):

    faiss.write_index(
        index,
        "anatomy.index"
    )

def load_chunks():

    with open(
        "chunks.pkl",
        "rb"
    ) as f:

        return pickle.load(f)
    
def save_chunks(chunks):

    with open(
        "chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )

def load_bm25():

    with open(
        "bm25.pkl",
        "rb"
    ) as f:

        return pickle.load(f)
    
def save_bm25(bm25):

    with open(
        "bm25.pkl",
        "wb"
    ) as f:

        pickle.dump(
            bm25,
            f
        )

            


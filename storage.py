import os
import pickle
import faiss


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
    )

def get_document_path(user_id , document_name) :

    return os.path.join(
        DATA_DIR,
        f"user_{user_id}",
        document_name
    )

def save_index(index, user_id, document_name):

    folder = os.path.join(
        DATA_DIR,
        f"user_{user_id}",
        document_name
    )

    print("========== SAVE INDEX DEBUG ==========")
    print("USER ID:", user_id)
    print("DOCUMENT NAME:", repr(document_name))
    print("FOLDER:", folder)
    print("======================================")

    os.makedirs(
        folder,
        exist_ok=True
    )


    path = os.path.join(
        folder,
        "index.faiss"
    )


    faiss.write_index(
        index,
        path
    )


def load_index(user_id, document_name):
    path = get_document_path(user_id, document_name)

    index_path = os.path.join(
        path,
        "index.faiss"
    )

    print("========== DEBUG ==========")
    print("USER ID:", user_id)
    print("DOCUMENT NAME:", repr(document_name))
    print("DOCUMENT PATH:", path)
    print("INDEX PATH:", index_path)
    print("INDEX EXISTS:", os.path.exists(index_path))
    print("============================")

    if os.path.exists(index_path):
        return faiss.read_index(index_path)

    return None



def save_chunks(chunks, user_id , document_name):

    folder = os.path.join(
        DATA_DIR,
        f"user_{user_id}",
        document_name
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    with open(
        os.path.join(folder,"chunks.pkl"),
        "wb"
    ) as f:
        pickle.dump(chunks,f)


def load_chunks(user_id, document_name):
    path = get_document_path(user_id, document_name)

    file_path = os.path.join(
        path,
        "chunks.pkl"
    )

    if os.path.exists(file_path):

        with open(file_path, "rb") as f:
            return pickle.load(f)

    return []



def save_bm25(bm25, user_id , document_name):

    folder = os.path.join(
        DATA_DIR,
        f"user_{user_id}",
        document_name
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    with open(
        os.path.join(folder,"bm25.pkl"),
        "wb"
    ) as f:
        pickle.dump(bm25,f)


def load_bm25(user_id, document_name):
    path = get_document_path(user_id, document_name)

    file_path = os.path.join(
        path,
        "bm25.pkl"
    )

    if os.path.exists(file_path):

        with open(file_path, "rb") as f:
            return pickle.load(f)

    return None
        


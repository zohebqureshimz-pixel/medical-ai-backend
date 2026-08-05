import os
import pickle
import faiss
from cloud_storage import upload_file_to_cloud, download_file_from_cloud

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


def get_document_path(user_id, document_name: str) -> str:
    return os.path.join(DATA_DIR, f"user_{user_id}", document_name)


def get_cloud_key(user_id, document_name: str, filename: str) -> str:
    return f"data/user_{user_id}/{document_name}/{filename}"


def save_index(index, user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    os.makedirs(folder, exist_ok=True)
    
    local_path = os.path.join(folder, "index.faiss")
    faiss.write_index(index, local_path)
    
    cloud_key = get_cloud_key(user_id, document_name, "index.faiss")
    upload_file_to_cloud(local_path, cloud_key)


def load_index(user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    index_path = os.path.join(folder, "index.faiss")
    
    if not os.path.exists(index_path):
        cloud_key = get_cloud_key(user_id, document_name, "index.faiss")
        download_file_from_cloud(cloud_key, index_path)

    if os.path.exists(index_path):
        return faiss.read_index(index_path)

    return None


def save_chunks(chunks, user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    os.makedirs(folder, exist_ok=True)
    
    local_path = os.path.join(folder, "chunks.pkl")
    with open(local_path, "wb") as f:
        pickle.dump(chunks, f)

    cloud_key = get_cloud_key(user_id, document_name, "chunks.pkl")
    upload_file_to_cloud(local_path, cloud_key)


def load_chunks(user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    file_path = os.path.join(folder, "chunks.pkl")

    if not os.path.exists(file_path):
        cloud_key = get_cloud_key(user_id, document_name, "chunks.pkl")
        download_file_from_cloud(cloud_key, file_path)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)

    return []


def save_bm25(bm25, user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    os.makedirs(folder, exist_ok=True)
    
    local_path = os.path.join(folder, "bm25.pkl")
    with open(local_path, "wb") as f:
        pickle.dump(bm25, f)

    cloud_key = get_cloud_key(user_id, document_name, "bm25.pkl")
    upload_file_to_cloud(local_path, cloud_key)


def load_bm25(user_id, document_name: str):
    folder = get_document_path(user_id, document_name)
    file_path = os.path.join(folder, "bm25.pkl")

    if not os.path.exists(file_path):
        cloud_key = get_cloud_key(user_id, document_name, "bm25.pkl")
        download_file_from_cloud(cloud_key, file_path)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)

    return None

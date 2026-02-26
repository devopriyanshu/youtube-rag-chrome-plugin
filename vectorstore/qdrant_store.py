from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from core.embeddings import get_embeddings
import os

COLLECTION_NAME = 'youtube_videos'
def get_vector_store():
    client = QdrantClient(url='http://localhost:6333')

    return Qdrant(
        client=client,
        collection_name="my_collection",
        embeddings=get_embeddings()
    )
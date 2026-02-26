from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from core.embeddings import get_embeddings
import os

COLLECTION_NAME = 'youtube_videos'

def get_vector_store():
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=qdrant_url)

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=3072, distance=models.Distance.COSINE),
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings()
    )

def check_video_exists(video_id: str) -> bool:
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=qdrant_url)
    try:
        res = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.video_id",
                        match=models.MatchValue(value=video_id)
                    )
                ]
            ),
            limit=1
        )
        return len(res[0]) > 0
    except Exception:
        return False
from vectorstore.qdrant_store import get_vector_store
from core.llm import get_llm
from dotenv import load_dotenv

load_dotenv()

def rewrite_query(query):
    llm = get_llm()
    prompt = f"Rewrite for better semantic retrieval: {query}" 
    return llm.invoke(prompt).content

def retrieve_context(video_id, query):
    improved_query  = rewrite_query(query)
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "filter": {
                "must": [
                    {
                        "key": "video_id",
                        "match": {"value": video_id}
                    }
                ]
            }
        }
    )
    return retriever.invoke(improved_query)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vectorstore.qdrant_store import get_vector_store


def index_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 300
    )

    chunks = splitter.split_documents(documents)

    vector_store = get_vector_store()
    
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vector_store.add_documents(batch)
        if i + batch_size < len(chunks):
            import time
            time.sleep(5) # Throttle to respect Gemini free-tier 100RPM embed limit

    return len(chunks)


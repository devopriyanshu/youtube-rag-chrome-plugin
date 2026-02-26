from langchain_text_splitters import RecursiveCharacterTextSplitter
from vectorstore.qdrant_store import get_vector_store


def index_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 150
    )

    chunks = splitter.split_documents(documents)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)


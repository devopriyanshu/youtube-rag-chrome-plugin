from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')
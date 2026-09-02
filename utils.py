from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(
    model = "text-embedding-3-small",
    api_key = API_KEY
)

def extract_cv_text(path: str) -> str:
    loader = PyPDFLoader(path)
    documents = loader.load() 
    return "\n".join(doc.page_content for doc in documents)

def get_embedding(text:str) -> list[float]:
    return embeddings_model.embed_query(text)
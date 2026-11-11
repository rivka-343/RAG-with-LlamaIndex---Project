import os
import certifi
import ssl
from google.genai import Client # הוסף את זה ב-imports למעלה

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
from dotenv import load_dotenv
import chromadb
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

# יבוא הפונקציה מהצעד הקודם
from rag.process_data import load_and_process_data

load_dotenv()

def build_rag_index():
    api_key = os.getenv("GEMINI_API_KEY")


    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

  
    # 2. טעינת הנתונים המעובדים מצעד 2
    print("⏳ טוען נתונים מהקובץ...")
    raw_docs = load_and_process_data(os.path.join("rag", "otzar_books.csv"))
    
    # המרה לפורמט של LlamaIndex
    documents = [
        Document(text=d['text'], metadata=d['metadata']) 
        for d in raw_docs
    ]

    # 3. הקמת ChromaDB (אחסון מקומי)
    print("📦 מקים מסד נתונים וקטורי...")
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("books_catalog")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. יצירת האינדקס (כאן קורה הקסם - שליחת הנתונים ל-API ליצירת וקטורים)
    print("🚀 יוצר אינדקס וקטורי (זה עשוי לקחת זמן בגלל כמות השורות)...")
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        show_progress=True
    )

    print("✅ האינדקס מוכן ונשמר בתיקייה ./chroma_db")
    return index

if __name__ == "__main__":
    build_rag_index()
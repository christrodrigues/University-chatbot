from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import warnings

warnings.filterwarnings("ignore")
os.environ['USER_AGENT'] = 'northeastern-chatbot/1.0'
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

load_dotenv()

try:
    # Load docs
    print("Loading documents...")

    urls = [
    "https://www.northeastern.edu/",
    "https://www.northeastern.edu/campuses/boston/",
    "https://graduate.northeastern.edu/admissions-aid/how-to-apply/",
    "https://www.northeastern.edu/academics/",
    "https://www.northeastern.edu/admissions/",
    "https://www.northeastern.edu/student-life/",
   
     ]
            
    loader = WebBaseLoader(urls)

    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    # Split into chunks
    print("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Larger chunks often work better
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    # Create vector store
    print("Creating vector store...")
    db = Chroma.from_documents(
        chunks, 
        OpenAIEmbeddings(), 
        persist_directory="db"
    )
    print("Vector store created and persisted!")

except Exception as e:
    print(f"Error: {e}")
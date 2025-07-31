from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# Load the database
db = Chroma(persist_directory="db", embedding_function=OpenAIEmbeddings())

# Get collection info
collection = db._collection
print(f"Total documents in database: {collection.count()}")

# Test a simple retrieval
query = "Northeastern University"
docs = db.similarity_search(query, k=3)

print(f"\nFound {len(docs)} similar documents for query: '{query}'")
print("\nFirst few results:")
for i, doc in enumerate(docs[:2]):
    print(f"\n--- Document {i+1} ---")
    print(f"Content preview: {doc.page_content[:200]}...")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
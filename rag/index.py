from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# Define the path to the PDF file
pdf_path = Path(__file__).parent / "springboot.pdf"

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

#Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)

#Vector embeddings for the chunks
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Create a vector store and add the chunks to it
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",  #Make sure Qdrant database is running at this URL
    collection_name="springboot_docs"
)

print("Document loaded, split into chunks, and added to the vector store successfully!")
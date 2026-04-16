from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = Path(__file__).parent / "springboot.pdf"

#Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

#Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)
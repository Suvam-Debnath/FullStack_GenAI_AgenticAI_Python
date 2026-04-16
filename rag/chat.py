from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

#Vector embeddings for the chunks
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Create a vector store and add the chunks to it
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333", #Make sure Qdrant database is running at this URL
    collection_name="springboot_docs"
)

# Taking user input and retrieving relevant chunks from the vector store
user_query = input("Enter your question about Spring Boot: ")

#Perform similarity search to find relevant chunks based on the user's query from the vector db
search_results = vector_db.similarity_search(query=user_query, k=3)

# Prepare the context for the system prompt by combining the retrieved chunks with their page numbers and file locations
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
 You are a helpfull AI Assistant who answeres user query based on the available context retrieved from a PDF file along with page_contents and page number.

 You should only ans the user based on the following context and navigate the user to open the right page number to know more.

 Context:
 {context}
"""

# Now we will send the user query along with the system prompt to the OpenAI API to get a response based on the retrieved context.
response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        { "role": "system", "content":SYSTEM_PROMPT  },
        { "role": "user", "content":user_query  },
    ]
)


print(f"🤖: {response.choices[0].message.content}")
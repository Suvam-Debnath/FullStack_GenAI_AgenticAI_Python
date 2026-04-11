from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Client will automatically pick GEMINI_API_KEY from environment
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain ai in few words"
)

print(response.text)
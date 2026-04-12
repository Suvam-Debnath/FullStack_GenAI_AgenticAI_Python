from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [GEMINI_API_KEY]

# Initialize OpenAI client and make a chat completion request
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Optional, default is OpenAI's API endpoint
)

# Make a chat completion request to Gemini model
response = client.chat.completions.create(
  model="gemini-2.5-flash",
    messages=[
      {"role": "user", "content": "what is the capital of France?"}
    ]
)

# Print the response from the model
print(response.choices[0].message.content)
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [OPENAI_API_KEY]

# Initialize OpenAI client and make a chat completion request
client = OpenAI()

# Make a chat completion request to GPT-4o-mini model
response = client.chat.completions.create(
  model="gpt-4o-mini",
    messages=[
      {"role": "user", "content": "What is the capital of France?"}
    ]
)
print(response.choices[0].message.content)
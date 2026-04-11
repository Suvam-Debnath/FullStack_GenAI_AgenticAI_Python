from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [OPENAI_API_KEY]
client = OpenAI()
response = client.chat.completions.create(
  model="gpt-4o-mini",
    messages=[
      {"role": "user", "content": "What is the capital of France?"}
    ]
)
print(response.choices[0].message.content)
#ZERO-SHOT PROMPTING EXAMPLE

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [GEMINI_API_KEY]

# Initialize OpenAI client and make a chat completion request
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Optional, default is OpenAI's API endpoint
)

# Zero-shot prompting: Directly giving the instruction to the model without any examples
SYSTEM_PROMPT = "You should only answer coding realted questioons. If the question is not coding related, respond with 'I can only answer coding related questions.'"

# Make a chat completion request to Gemini model
response = client.chat.completions.create(
  model="gemini-2.5-flash",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": "can  you help me to solve 1+5?"}
    ]
)

# Print the response from the model
print(response.choices[0].message.content)
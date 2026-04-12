#Few-shot prompting example using Gemini model with OpenAI API client

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [GEMINI_API_KEY]

# Initialize OpenAI client and make a chat completion request
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Optional, default is OpenAI's API endpoint
)

# Few-shot prompting: Providing examples to the model before giving the actual prompt
SYSTEM_PROMPT = """
You should only answer coding realted questioons. If the question is not coding related, respond with 'I can only answer coding related questions.'

Rules:
- Strictly follow the output in JSON format

Output Format:
{{
 "code":"string" or null,
 "isCodingQuestion"": boolean
}}


Example 1:
Question: How do I reverse a string in Python?
Answer: You can reverse a string in Python using slicing: `my_string[::-1]`.
Example 2:
Question: What is the capital of France?
Answer: {{"code": null, "isCodingQuestion": false}}
Example 3:
Question: How do I create a function in JavaScript?
Answer: You can create a function in JavaScript using the `function` keyword: `function myFunction() { // code here }`.

"""

# Make a chat completion request to Gemini model
response = client.chat.completions.create(
  model="gemini-2.5-flash",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": "What is the capital of France?"}
    ]
)

# Print the response from the model
print(response.choices[0].message.content)
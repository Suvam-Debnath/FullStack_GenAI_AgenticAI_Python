# Chain of Thought prompting example using Gemini model with OpenAI API client

from pyexpat.errors import messages
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file [GEMINI_API_KEY]

# Initialize OpenAI client and make a chat completion request
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Optional, default is OpenAI's API endpoint
)

SYSTEM_PROMPT = """
    Your are an experrt AI Assistant in resolving user queeries using chain of thought.
    Your work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has benn done, finally you can give the final answer in OUTPUT.

    Rules:
    - Strictly follow the output in JSON format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an intput), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    {{
        "step": "START" or "PLAN" or "OUTPUT",
        "message": "string"
    }}

    Example 1:
    START: Hey, can you solve 2+3*5/10
    PLAN: {
        "step": "PLAN",
        "message": "seems user is interested in math problem."
    }
    PLAN: {
        "step": "PLAN",
        "message": "looking at the problem, we should solve this using BODMAS method."
    }
    PLAN: {
        "step": "PLAN",
        "message": "I need to calculate the expression 2+3*5/10 following the order of operations."
    }
    PLAN: {
        "step": "PLAN",
        "message": "The expression 2+3*5/10 evaluates to 2+15/10, which is 2+1.5, resulting in 3.5."
    }
    OUTPUT: {
        "step": "OUTPUT",
        "message": "The result of the expression 2+3*5/10 is 3.5."
    }


"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("-->")
message_history.append({"role": "user", "content": user_query})


# Make a chat completion request to Gemini model
response = client.chat.completions.create(
  model="gemini-2.5-flash",
  response_format={"type": "json_object"},
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": "solve 2+3*5/10"},

      # Manually keep adding messages to history based on the response from the model until you get the final answer in OUTPUT step.
       {"role": "assistant", "content": json.dumps({
         "step": "START",
        "message": "User wants to solve the mathematical expression 2+3*5/10."})},
        {"role": "assistant", "content": json.dumps({
         "step": "PLAN", "message": "I need to calculate the expression 2+3*5/10 following the order of operations (BODMAS/PEMDAS)."
        })},
        {"role": "assistant", "content": json.dumps({
         "step": "PLAN", "message": "First, perform the multiplication: 3 * 5 = 15."
        })},
        {"role": "assistant", "content": json.dumps({
         "step": "PLAN", "message": "Next, perform the division: 15 / 10 = 1.5."
        })},
        {"role": "assistant", "content": json.dumps({
         "step": "PLAN", "message": "Finally, perform the addition: 2 + 1.5 = 3.5."
        })},
        {"role": "assistant", "content": json.dumps({
         "step": "OUTPUT", "message": "The result of the expression 2+3*5/10 is 3.5."
        })}
    ]
)

# Print the response from the model
print(response.choices[0].message.content)
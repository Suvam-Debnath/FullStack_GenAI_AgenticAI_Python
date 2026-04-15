# Chain Of Thought Prompting
from dotenv import load_dotenv
from ollama import Client   # ✅ CHANGED
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

load_dotenv()

client = Client(host="http://localhost:11434")   # ✅ CHANGED

def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}


SYSTEM_PROMPT = """ 
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    - get_weather(city: str)
    - run_command(cmd: str)
"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None)
    tool: Optional[str] = Field(None)
    input: Optional[str] = Field(None)

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👉🏻 ")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        # ✅ CHANGED: Ollama call
        response = client.chat(
            model="llama3",   # ✅ local model
            messages=message_history
        )

        raw_result = response['message']['content']
        message_history.append({"role": "assistant", "content": raw_result})

        # ✅ CHANGED: manual parsing instead of .parse()
        try:
            parsed_result = json.loads(raw_result)
        except:
            print("❌ Invalid JSON from model")
            break

        if parsed_result["step"] == "START":
            print("🔥", parsed_result.get("content"))
            continue

        if parsed_result["step"] == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")

            message_history.append({ 
                "role": "user",   # ✅ CHANGED from developer → user
                "content": json.dumps(
                    { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
                ) 
            })
            continue

        if parsed_result["step"] == "PLAN":
            print("🧠", parsed_result.get("content"))
            continue

        if parsed_result["step"] == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

print("\n\n\n")
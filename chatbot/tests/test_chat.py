import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools import esp_tools
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

config = types.GenerateContentConfig(
    tools=[esp_tools],
    temperature=0.7,
    system_instruction=(
        "You are ESPilot..."  # same system instruction as main.py
    )
)

def act(name, args):
    args = dict(args)
    print(f"[TEST] Would call '{name}' with params: {args}")
    return {"status": "success", "message": f"{name} executed (simulated)"}

chat = client.chats.create(model="gemini-2.5-flash", config=config)

while True:
    request = input("You: ")
    if request.lower() in ("quit", "exit"):
        break

    response = chat.send_message(request)

    while True:
        part = response.candidates[0].content.parts[0]
        if part.function_call:
            func_name = part.function_call.name
            func_args = part.function_call.args
            result = act(func_name, func_args)

            response = chat.send_message(
                types.Part.from_function_response(name=func_name, response=result)
            )
        else:
            break

    print("AI:", response.text)
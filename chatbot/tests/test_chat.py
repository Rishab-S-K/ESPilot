import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import requests
from tools import esp_tools
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


##Model Decleration
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    tools=[esp_tools],
    generation_config=genai.GenerationConfig(temperature=0.7),
    system_instruction=(
        "You are ESPilot, a chatbot that is able to control a ESP32-controlled breadboard. "
        "The breadboard has LEDS (red, yellow, blue, green, white), an RGB LED, temperature "
        "sensor, light sensor, passive buzzer, active buzzer, and a LCD display with 4 rows. "
        "Interpret user requests and call the appropriate tool to control the breadboard. "
        "Here are some of the features you may be asked(you must not be limited to these, be creative). "
        "-Generating your own song. "
        "-Playing a known song by transcribing the sheet music. Note that only 1 frequency can be played at one time due to there being only 1 passive buzzer. "
        "-Generating fun color themes for the LEDS, like if you are asked to make the breadboard 'spooky'. "
    )
)

##action function
def act(name, args):
    args = dict(args)
    print(f"[TEST] Would call '{name}' with params: {args}")
    return {"status": "success", "message": f"{name} executed (simulated)"}
    
chat = model.start_chat()

while True:
    request = input("You: ")
    if request.lower() in ("quit", "exit"): 
        break
    
    response = chat.send_message(request)

    while True:
        part = response.candidates[0].content.parts[0]

        if part.function_call.name:
            func_name = part.function_call.name
            func_args = part.function_call.args
            result = act(func_name, func_args)

            response = chat.send_message(
                genai.protos.Content(parts=[genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(name=func_name, response=result)
                )])
            )
        else:
            break
    print("AI:", response.text)


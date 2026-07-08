import os
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
    system_instruction=(
        "You are ESPilot, a chatbot that is able to control a ESP32-controlled breadboard."
        "The breadboard has LEDS(red, yellow, blue, green, white), an RGB LED, temperature"
        "sensor, light sensor, passive buzzer, active buzzer, and a LCD display with 4 rows."
        "Interpret user requests and call the appropriate tool to control the breadboard."
        "Additionally, the user pay ask you to generate a song, either known or to make your own."
        "The known song should be transcribed and played. The song that is asked to create should be played."
    )
)

##action function
def act(name, args):
    args = dict(args)
    payload = {"function": name, "params": args}

    try:
        response = requests.post(f"{ESP32_IP}/execute", json = payload, timeout = 10)
        return response.json()
    except requests.exceptions.Re as exception:
        return {"status": "error", "message": str(exception)}
    
chat = model.start_chat()

while True:
    request = input("You: ")
    if request.lower() in ("quit", "exit"): 
        break

    response = chat.send_message(request)
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
        print("AI:", response.text)
    else:
        print("AI:", response.text)


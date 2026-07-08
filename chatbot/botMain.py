import os
import requests
from tools import esp_tools
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
ESP32_IP = os.environ["ESP32_IP"]


##Model Decleration
config = types.GenerateContentConfig(
    tools=[esp_tools],
    temperature=0.7,
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
    #esp32 must get values as ints not floats so convert them prior
    for key, value in args.items():
        if isinstance(value, float) and value.is_integer():
            args[key] = int(value)
    #payload structure (what the chatbot sends out)
    payload = {"function": name, "params": args}

    try:
        response = requests.post(f"{ESP32_IP}/execute", json = payload, timeout = 10)
        return response.json()
    except requests.exceptions.RequestException as exception:
        return {"status": "error", "message": str(exception)}
    
chat = client.chats.create(model="gemini-2.5-flash", config=config)


##Chat Loop
while True:
    request = input("You: ")
    if request.lower() in ("quit", "exit"): #exit if asked
        break
    
    response = chat.send_message(request)

    #for multiple actions in one request, keep calling 'act' until there are no function calls remaining
    while True:
        part = response.candidates[0].content.parts[0]

        if part.function_call: #if its a function call, continue
            func_name = part.function_call.name
            func_args = part.function_call.args
            result = act(func_name, func_args)

            #get a reply back after executing what the user wanted
            response = chat.send_message(
                types.Part.from_function_response(name=func_name, response=result)
            )
        else: #otherwise stop
            break
    print("AI:", response.text)
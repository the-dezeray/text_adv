import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import content_types
from collections.abc import Iterable

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model
model_name = "gemini-2.0-flash"

# Define available functions
def enable_lights():
    print("LIGHTBOT: Lights enabled.")

def set_light_color(rgb_hex: str):
    print(f"LIGHTBOT: Lights set to {rgb_hex}.")

def stop_lights():
    print("LIGHTBOT: Lights turned off.")

# Register functions
light_controls = [enable_lights, set_light_color, stop_lights]

# System instructions
instruction = "You are part of a game engine a story builder. A user will  give you a story to make  an  you will try to make it "

# Initialize model with tools
model = genai.GenerativeModel(model_name, tools=light_controls, system_instruction=instruction)

# Function to configure tool usage
def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    return content_types.to_tool_config({"function_calling_config": {"mode": mode, "allowed_function_names": fns}})

# Enable automatic function calling
auto_chat = model.start_chat(enable_automatic_function_calling=True)

print("LIGHTBOT: Ready to assist! Type 'exit' to quit.")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("LIGHTBOT: Goodbye!")
        break

    # Send message with tool configuration
    tool_config = tool_config_from_mode("auto")
    response = auto_chat.send_message(user_input, tool_config=tool_config)


    # Print the regular message response (if present)
    if response.parts:
        print(f"LIGHTBOT: {response.parts[0]}")

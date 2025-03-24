import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import content_types
from collections.abc import Iterable
from pydantic import BaseModel, ConfigDict
from typing import Optional,List ,Dict




def get_schema():
    schema = ""
    with open("data/structure.txt","r") as content:
        schema = content.read()
    if schema == "":
        raise ValueError("Schema is empty")
# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model
model_name = "gemini-2.0-flash"

schema = get_schema()

def generate_plot_as_nodes(plot: str) -> str:
    """Calls a Gemini client to generate a string based on the plot and other rules which will be turned into dictionary of nodes
    Args:
        plot(str): The plot generated by another AI
    Returns: 
        A string convertable into a dict
    """
    print("\nGenerating plot as nodes")

    response_schema = {
    "type": "ARRAY",

    "items": {
        "type": "OBJECT",
        "properties": {
        "id": {"type": "STRING"},
        "location": {"type": "STRING", "nullable": True},
        "text": {"type": "STRING"},
        "choices": {
            "type": "ARRAY",
            "items": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING"},
                "next_node": {"type": "STRING"},
                "function": {"type": "STRING", "nullable": True}
            },
            "required": ["text", "next_node"]
            }
        }
        },
        "required": ["id", "text", "choices"]
    }
    }

    # Create a properly formatted prompt with the plot and schema
    prompt = f"""Generate a story based on this plot: {plot}. which you present in a form of nodes like this ones {schema}.JSON should include a maximum of 10 story nodes."""
    
    con = genai.GenerationConfig(response_mime_type= "application/json",response_schema=response_schema)
    
    # Use the configured client instead of creating a new one
    model = genai.GenerativeModel(model_name="gemini-2.0-flash",generation_config=con)
    response = model.generate_content(prompt)
    
    print(f"Response = {response.text}")
    return response.text

# Register functions
light_controls = [generate_plot_as_nodes]

# System instructions
instruction = "You are part of a game engine story builder. A user will give you a story idea, and you will generate a plot of no less than 15 words. Then use the generate_plot_as_nodes function to get a structured version of the story."

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
        print(f"LIGHTBOT: {response.parts[0].text}")
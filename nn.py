from google import genai


import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))




from pydantic import BaseModel

class Choice(BaseModel):
    text: str
    next_node: int
    function: str | None

class Node(BaseModel):
    id: int
    location: str
    text: str
    choices: list[Choice]

response = client.models._generate_content_stream(
    model="gemini-2.0-flash",
    contents="Create a story  adventure  game with some nodes and choices.",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Node],
    },
)
# Use the response as a JSON string.
for chunk in response:
    print(chunk.text, end="")

print(response.text)

# Use instantiated objects.
my_recipes: list[Recipe] = response.parsed
import os
from google import genai
from google.genai import types


from dotenv import load_dotenv
load_dotenv()


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
class AI:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.config = types.GenerateContentConfig(
            system_instruction="You are a story builder a world Crafter. You will be given a story idea and you will generate a story based on the idea. and validate the story",
            tools=[self.generate_story, self.validate_story]
        )
    def generate_story(self,idea: str) -> list[Node]:
        """Generate a story .
        
        Args:

            idea: The main concept or theme for the story
            
        Returns:
            A list of Node objects representing the story structure
        """
        # Implementation would go here
        # For now returning a simple example
        print("generating story")

        response = self.client.models._generate_content(
            model="gemini-2.0-flash",
            contents=f"Create a story  adventure  game with some nodes and choices based on the idea {idea}.",
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Node],
            },
        )
        # Use the response as a JSON string.

        print(response.text)    # Use instantiated objects.
        story: list[Node] = response.parsed
        return {"story": story}

    
    
    
    def validate_story(self,story: list[Node]) -> dict:
        """Validate the story checking if all nodes are there .
        
        Args:
            story: List of Node objects representing the story
            
        Returns:
            A dictionary containing validation status and any issues found
        """
        #TODO: implement validation logic
        # Implementation would go here
        print("done validating story")
        return {"status": "success", "issues": []}

    def main(self):


        chat = self.client.chats.create(model="gemini-2.0-flash",config=self.config)

        responce =chat.send_message("a story about a fallen hero")
        print(responce.text)

a = AI()    
a.main()
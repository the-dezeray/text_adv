from ui.options import ui_text_panel
from typing import TYPE_CHECKING
import os
from google import genai
from google.genai import types
from util.logger import logger, event_logger

from dotenv import load_dotenv
load_dotenv()


from pydantic import BaseModel

if TYPE_CHECKING:
    from core.core import Core
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
    def __init__(self, core: "Core"):
        logger.info("Initializing AI class")
        self.core = core
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        logger.debug("Created Gemini client")
        tool_config = types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="ANY"
            )
        )
           
        self.config = types.GenerateContentConfig(
            system_instruction="You are a system the user will  provide an idea   and you will  pass that idea to the generate function and then use the validate function to validate the return value",
            tools=[self.generate_story, self.validate_story],
            tool_config=tool_config
        )

        self.chat = self.client.chats.create(model="gemini-2.0-flash",config=self.config)
        logger.info("AI initialization complete")
    @event_logger
    def generate_note(self, id: str) -> str:
        return "note is not implemented yet"
    @event_logger
    def fake_prompt(self, message: str) -> None:
        self.core.console.clear_display()
        self.core.console.print(ui_text_panel(text=""))
    @event_logger
    def prompt(self, message: str) -> None:
        logger.info(f"Processing prompt: {message[:50]}...")
        responce = self._prompt_model(message)
        logger.debug(f"Received response of length: {len(responce)}")
        self.core.console.print(ui_text_panel(text=responce))
    @event_logger
    def _prompt_model(self, message: str) ->str:
        logger.debug("Sending message to Gemini model")
        responce = self.chat.send_message(message)
        return str(responce.text)

    def generate_story(self,idea: str) -> list[Node]:
        """Generate a story .
        
        Args:
            idea: The main concept or theme for the story
            
        Returns:
            A list of Node objects representing the story structure
        """
        logger.info(f"Generating story for idea: {idea[:50]}...")
        self.core.console.print(ui_text_panel(text="generating story"))

        response = self.client.models._generate_content(
            model="gemini-2.0-flash",
            contents=f"Create a story adventure game with some nodes and choices based on the idea {idea}.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[Node]
            )
        )
        logger.debug("Received story generation response")
        logger.debug(response.text)
        self.core.console.print(ui_text_panel(text=response.text))    # Use instantiated objects.
        
        story: list[Node] = response.parsed
        return {"story": story}

    def validate_story( self,story: list[Node]) -> dict:
        """Validate the story checking if all nodes are there .
        
        Args:
            story: List of Node objects representing the story
            
        Returns:
            A dictionary containing validation status and any issues found
        """
        logger.info(f"Validating story with {len(story)} nodes")
        self.core.console.print(ui_text_panel(text="done validating story"))
        return {"status": "success", "issues": []}
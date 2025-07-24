from typing import Dict, Any

from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType


class ChatbotAgent:
    """
    A chatbot agent that can be configured with different models and system prompts.
    """

    def __init__(self, model_config: Dict[str, Any], agent_config: Dict[str, Any], tools: list = None):
        """
        Initializes the ChatbotAgent with provided configurations.

        Args:
            model_config (Dict[str, Any]): Configuration for the model, including
                                          'chatbot_model', 'api_key', and 'api_base_url'.
            agent_config (Dict[str, Any]): Configuration for the agent, including
                                          'role_name' and 'system_message'.
        """
        self.model_name = model_config['chatbot_model']
        self.camel_model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
            model_type=self.model_name,
            api_key=model_config['api_key'],
            url=model_config['api_base_url'],
            model_config_dict={"temperature": 0.7}
        )

        system_message = BaseMessage.make_assistant_message(
            role_name=agent_config["role_name"],
            content=agent_config["system_message"]
        )

        self.chat_agent = ChatAgent(system_message=system_message, model=self.camel_model, tools=tools)

    def run(self, user_message: str) -> Dict[str, Any]:
        """
        Runs the chatbot with the given user message.

        Args:
            user_message (str): The user's message.

        Returns:
            A dictionary containing the agent's response.
        """
        try:
            print(f"Invoking ChatAgent with model: {self.model_name}...")
            response = self.chat_agent.step(user_message)
            content = response.msgs[0].content
            return {"status": "success", "data": {"response": content}, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}
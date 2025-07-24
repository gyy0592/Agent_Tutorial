import sys
from pathlib import Path
import yaml

# --- Path Setup ---
# Add the project root to the Python path to allow imports from 'backend'
# This script is in tests/agents/, so we need to go up two levels
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.agents.chatbot import ChatbotAgent

def main():
    """
    Initializes the ChatbotAgent and runs a test query.
    """
    print("--- Testing Refactored ChatbotAgent ---")
    try:
        # Load Configurations
        config_path = project_root / 'config' / 'config.yaml'
        agents_path = project_root / 'config' / 'agents.yaml'

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        with open(agents_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)

        # Determine model configuration based on mode
        mode = config.get('mode', 'api')
        if mode == 'local':
            model_config = config['local_model']
            print("--- Using LOCAL model mode ---")
        else:
            model_config = config['api']
            print("--- Using API model mode ---")

        # Get agent configuration
        agent_config = prompts.get('chatbot')
        if not agent_config:
            raise ValueError("Agent 'chatbot' not found in agents.yaml")

        # Initialize the agent
        chatbot = ChatbotAgent(model_config=model_config, agent_config=agent_config)
        print("ChatbotAgent initialized successfully.")

        # Define a user message
        user_message = "Hello, what can you do?"
        print(f"User Message: {user_message}")

        # Run the agent
        result = chatbot.run(user_message)

        # Print the result
        if result["status"] == "success":
            print(f"Agent Response: {result['data']['response']}")
        else:
            print(f"An error occurred: {result['error']}")
        
        print("--- Test Complete ---")

    except FileNotFoundError as e:
        print(f"ERROR: A configuration file was not found. Please ensure config.yaml and agents.yaml exist. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the test: {e}")

if __name__ == "__main__":
    main()
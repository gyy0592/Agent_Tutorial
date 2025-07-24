import sys
from pathlib import Path
import yaml
from typing import Dict, Any

# --- Path Setup ---
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.agents.chatbot import ChatbotAgent
from backend.tools.example_tool import greet_user_tool


def load_configurations(project_dir: Path) -> Dict[str, Any]:
    """
    Loads and returns the model and agent configurations.
    """
    print("Loading Configurations...")
    config_path = project_dir / 'config' / 'config.yaml'
    agents_path = project_dir / 'config' / 'agents.yaml'

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    with open(agents_path, 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)

    mode = config.get('mode', 'api')
    if mode == 'local':
        model_config = config['local_model']
        print("Using LOCAL model mode.")
    else:
        model_config = config['api']
        print("Using API model mode.")

    chatbot_agent_config = prompts.get('chatbot')
    if not chatbot_agent_config:
        raise ValueError("Agent 'chatbot' not found in agents.yaml")
    
    return {
        "model_config": model_config,
        "chatbot_agent_config": chatbot_agent_config
    }


def initialize_agents(
    model_config: Dict[str, Any],
    agent_config: Dict[str, Any]
) -> Dict[str, ChatbotAgent]:
    """
    Initializes and returns two ChatbotAgent instances: one with a tool, one without.
    """
    print("Initializing Agents...")
    # Agent 1 (Tool User) with the tool
    tool_user_agent = ChatbotAgent(
        model_config=model_config,
        agent_config=agent_config,
        tools=[greet_user_tool] # Pass the tool here
    )
    print("Agent 1 (Tool User) initialized with greet_user_tool.")

    # Agent 2 (Tool Output Processor) without tools
    tool_output_processor_agent = ChatbotAgent(
        model_config=model_config,
        agent_config=agent_config
    )
    print("Agent 2 (Tool Output Processor) initialized.")

    return {
        "tool_user_agent": tool_user_agent,
        "tool_output_processor_agent": tool_output_processor_agent
    }


def run_tool_user_interaction(tool_user_agent: ChatbotAgent) -> str:
    """
    Simulates the first agent's interaction, including tool calling.
    Returns the content of the tool's response or an error message.
    """
    print("\nRunning Agent 1 Interaction (Tool Calling)...")
    user_message_to_tool_agent = "Please greet John Doe."
    print(f"Input to Agent 1: {user_message_to_tool_agent}")

    tool_agent_result = tool_user_agent.run(user_message_to_tool_agent)

    if tool_agent_result["status"] == "success":
        tool_response_content = tool_agent_result['data']['response']
        print(f"Output from Agent 1: {tool_response_content}")
    else:
        tool_response_content = f"Error: {tool_agent_result['error']}"
        print(f"Error from Agent 1: {tool_response_content}")
    
    return tool_response_content


def run_output_processor_interaction(
    processor_agent: ChatbotAgent,
    tool_response_content: str
) -> str:
    """
    Simulates the second agent processing the first agent's output.
    Returns the final response from the second agent or an error message.
    """
    print("\nRunning Agent 2 Interaction (Processing Tool Output)...")
    processor_message = f"The previous agent received this response from a tool: '{tool_response_content}'. Please summarize this and provide a friendly closing remark."
    print(f"Input to Agent 2: {processor_message}")

    processor_agent_result = processor_agent.run(processor_message)

    if processor_agent_result["status"] == "success":
        final_response = processor_agent_result['data']['response']
        print(f"Output from Agent 2 (Final Response): {final_response}")
    else:
        final_response = f"Error: {processor_agent_result['error']}"
        print(f"Error from Agent 2: {final_response}")
    
    return final_response


def main():
    """
    Main function to orchestrate the direct demonstration of tool calling and agent interaction.
    """
    print("--- Starting Direct Tool and Agent Demonstration ---")
    try:
        project_dir = Path(__file__).parent.parent

        # Step 1: Load Configurations
        configs = load_configurations(project_dir)
        model_config = configs["model_config"]
        chatbot_agent_config = configs["chatbot_agent_config"]

        # Step 2: Initialize Agents
        agents = initialize_agents(model_config, chatbot_agent_config)
        tool_user_agent = agents["tool_user_agent"]
        tool_output_processor_agent = agents["tool_output_processor_agent"]

        # Step 3: Run Agent 1 Interaction (Tool Calling)
        tool_response = run_tool_user_interaction(tool_user_agent)

        # Step 4: Run Agent 2 Interaction (Processing Tool Output)
        final_output = run_output_processor_interaction(tool_output_processor_agent, tool_response)
        
        print("\n--- Demonstration Complete ---")

    except FileNotFoundError as e:
        print(f"ERROR: A configuration file was not found. Please ensure config.yaml and agents.yaml exist. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the demonstration: {e}")

if __name__ == "__main__":
    main()

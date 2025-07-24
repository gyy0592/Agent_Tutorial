# Minimum_LLm

This project provides a basic framework for interacting with language models, featuring a configurable chatbot agent.

## Getting Started

### Running the Chatbot

The core chatbot logic is encapsulated in `backend/agents/chatbot.py`.

*   To run a basic test of the chatbot's functionality without tools, execute:
    ```bash
    python tests/agents/test_chatbot.py
    ```
    This script initializes the `ChatbotAgent` and sends a predefined message, printing the agent's response.

*   To see an example of the chatbot using a custom tool, execute:
    ```bash
    python tests/tools/test_example_tool_usage.py
    ```
    This demonstrates how to integrate and utilize custom tools with the `ChatbotAgent`.

*   For a direct, step-by-step demonstration of two agents interacting with tool calling, execute:
    ```bash
    python workflow/direct_tool_agent_demo.py
    ```
    This script clearly illustrates the input, processing, and output at each stage of the interaction.

### Configuration

The behavior of the chatbot and the models it uses can be configured via YAML files located in the `config/` directory:

*   `config/config.yaml`: Defines the overall mode (local or API) and specific settings for the language models, including API keys, base URLs, and model names.
*   `config/agents.yaml`: Contains configurations for different agents, including their `role_name` and `system_message`. The `chatbot` agent's system message can be modified here to change its persona or instructions.

### Tool Calling

The `ChatbotAgent` supports tool calling, allowing it to interact with external functions.

*   **Defining Tools**: Custom tools can be defined in the `backend/tools/` directory. Each tool should be a Python function wrapped using `camel.toolkits.FunctionTool`. It is crucial to provide clear docstrings for the function and its parameters to ensure the language model can correctly understand and utilize the tool. An example is provided in `backend/tools/example_tool.py`.
*   **Using Tools**: To enable tool calling for the `ChatbotAgent`, pass a list of `FunctionTool` instances to the `tools` parameter when initializing `ChatbotAgent`. Refer to `tests/tools/test_example_tool_usage.py` for a practical example.

### Customization

You can modify the `config/config.yaml` and `config/agents.yaml` files to:
*   Switch between local and API models.
*   Change the specific language model used.
*   Update API keys and base URLs.
*   Adjust the chatbot's system message and role name to alter its responses and behavior.
*   Add new custom tools and integrate them with the `ChatbotAgent` for extended functionality.

### Model Storage Paths

By default, large language models and their associated files can consume significant disk space. You can customize their storage locations by setting environment variables:

*   **Hugging Face Models**: To change the default download location for Hugging Face models (used by many Python libraries), set the `HF_HOME` environment variable to your desired path. For example, on Windows, in PowerShell or Command Prompt (run as administrator for system-wide, or just user for user-specific):
    ```bash
    setx HF_HOME "D:\your_huggingface_models_path"
    ```

*   **Ollama Models**: To change where Ollama stores its models, set the `OLLAMA_MODELS` environment variable. For example, on Windows:
    ```bash
    setx OLLAMA_MODELS "D:\your_ollama_models_path"
    ```

After setting these environment variables, you must restart any open terminal windows and the respective applications (e.g., Ollama server) for the changes to take effect.

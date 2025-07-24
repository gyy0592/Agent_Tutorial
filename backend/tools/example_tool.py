from camel.toolkits import FunctionTool

def greet_user(name: str) -> str:
    """Greets the user by their name."

    Args:
        name (str): The name of the user to greet.
    """
    return f"Hello, {name}! Nice to meet you."

greet_user_tool = FunctionTool(greet_user)

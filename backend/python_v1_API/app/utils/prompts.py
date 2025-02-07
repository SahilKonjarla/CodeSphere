def get_optimize_prompt(code: str, goal:str) -> str:
    return f"""
        You are an expert software optimizer specializing in analyzing code for inefficiencies and providing improvements. 
    
        Analyze the following code:
        
        {code}
        
        Your task is to:
        1. Identify inefficiencies in the code (e.g., redundant operations, slow algorithms, or excessive memory usage).
        2. Suggest specific optimizations to improve performance, reduce memory usage, or achieve other stated goals.
        3. Provide a detailed explanation for your suggestions, including why they improve the code and any trade-offs.
        
        Optimization Goal: {goal}
        If no inefficiencies are found, confirm that the code is already optimized and explain why no changes are necessary.
        
        In your output please structure it as such:
        Inefficiencies: Your response will go here
        Suggestions: Your response will go here
        Explanation: Your response will go here
    """


def get_debug_prompt(code: str) -> str:
    return f"""
        You are an expert debugging assistant. Your job is to analyze code for errors and provide detailed explanations and solutions.

        Here is the code snippet that needs to be debugged:
        {code}
        
        Your task is to:
        1. Identify any syntax, logical, or runtime errors in the code. Be specific about the issues and indicate the line numbers if possible.
        2. Suggest corrections or improvements for each issue.
        3. Provide a detailed explanation for each issue, including why it occurs and how your suggested solution resolves it.
        
        If the code has no errors, confirm that it is valid and explain why the code works correctly.
        
        Return the output in the following structure:
        - Errors: A list of identified issues in the code.
        - Suggestions: A list of corrections or improvements.
        - Explanation: A detailed explanation of the errors and solutions.
    """


def get_docstring_prompt(code: str) -> str:
    return f"""
        You are an expert in programming. Generate comprehensive docstrings for the following code:
        
        {code}
        
        Include descriptions for parameters, return values, and exceptions if applicable.
        
        In your response please before you give your response include the word Docstring and then
        include your response after
        
    """


def get_comments_prompt(code: str) -> str:
    return f"""
        You are an expert in programming. Add inline comments to the following code to explain its logic:

        {code}
        
        IIn your response please before you give your response include the word Comments and then
        include your response after
        
    """


def get_overview_prompt(code: str) -> str:
    return f"""
        You are an expert in programming. Provide a high-level overview of the functionality of the following code:

        {code}
        
        In your response please before you give your response include the word Overview and then
        include your response after in a new line
        
    """


def get_readme_prompt(code: str) -> str:
    return f"""
        You are an expert technical writer. Generate a README.md file for the following code:

        {code}

        Include:
        - A title for the project.
        - The purpose of the code.
        - Usage instructions, including input and output details.
        - Dependencies or requirements.
        - Example usage.
        
        In your response please before you give your response include the word README and then
        include your response after
        
    """


def get_learner_prompt(parsed_logs: list) -> str:
    """
    Constructs a dynamic prompt for the Learner Agent based on parsed user logs.

    :param parsed_logs: A list of parsed logs containing details of user interactions.
    :return: A formatted prompt string for the Learner Agent.
    """
    if not parsed_logs:
        raise ValueError("Parsed logs cannot be empty.")

    # Build the introductory part of the prompt
    prompt = (
        "You are an advanced learning assistant that helps developers improve their coding practices "
        "and workflows. Analyze the following recent user interactions to detect trends, provide actionable "
        "recommendations, and suggest educational resources.\n\n"
        "### Developer Logs:\n"
    )

    # Add each log to the prompt
    for idx, log in enumerate(parsed_logs, start=1):
        prompt += f"{idx}. Agent: {log['agent']}\n"
        prompt += f"   - Code: {log.get('code', 'N/A')}\n"

        # Add agent-specific details
        if log['agent'] == "debugging":
            prompt += f"   - Errors: {', '.join(log.get('errors', [])) or 'None'}\n"
            prompt += f"   - Suggestions: {', '.join(log.get('suggestions', [])) or 'None'}\n"
            prompt += f"   - Explanation: {log.get('explanation', 'N/A')}\n"
        elif log['agent'] == "optimization":
            prompt += f"   - Inefficiencies: {', '.join(log.get('inefficiencies', [])) or 'None'}\n"
            prompt += f"   - Suggestions: {', '.join(log.get('suggestions', [])) or 'None'}\n"
            prompt += f"   - Explanation: {log.get('explanation', 'N/A')}\n"
        elif log['agent'] == "documentation":
            prompt += f"   - Documentation Type: {log.get('documentation_type', 'N/A')}\n"
            prompt += f"   - Docstring: {', '.join(log.get('docstring', [])) or 'None'}\n"
            prompt += f"   - Readme: {', '.join(log.get('readme', [])) or 'None'}\n"
            prompt += f"   - Overview: {', '.join(log.get('overview', [])) or 'None'}\n"
            prompt += f"   - Comments: {', '.join(log.get('comments', [])) or 'None'}\n"

        # Add timestamp
        prompt += f"   - Timestamp: {log.get('timestamp', 'N/A')}\n\n"

    # Add instructions for the LLM
    prompt += (
        "### Tasks:\n"
        "1. Identify trends in the user's coding behavior, such as recurring issues, preferred programming languages, "
        "or frequently requested tasks.\n"
        "2. Provide actionable recommendations, including tools, libraries, or workflows that could improve their development process.\n"
        "3. Suggest educational resources, such as articles, tutorials, or documentation, to help the user improve their skills.\n\n"
        "### Output Format:\n"
        "- **Trends**: Summarize patterns detected in the user's behavior.\n"
        "- **Recommendations**: List actionable suggestions, including tools, libraries, or workflows.\n"
        "- **Resources**: Provide links to relevant articles, tutorials, or tools."
    )

    return prompt


def get_orchestrator_sys_prompt() -> str:
    """
    Returns the custom prompt for the orchestrator agent.
    """
    return (
        "You are an Orchestrator Agent that manages multiple specialized tools to help developers debug, optimize, "
        "and document their code. Based on the input, identify the correct tool(s) to invoke and return the output "
        "in a structured format."
    )


def get_orchestrator_prompt(message, user_id) -> str:
    """
    Returns the starter prompt for the orchestrator agent.
    """
    return f"""
        ### Message:
        {message}
        
        ### User_id:
        {user_id}

        Based on the user message, determine what the code is and what the task is, and what would be the most suitable tool(s) to invoke and provide a clear and actionable response.
    """

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

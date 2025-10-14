def get_prompt(user_prompt: str) -> str:
    """Generate an optimized prompt based on user input."""
    common_instructions = """
You are an expert AI assistant. When responding:
- Be helpful and accurate
- Provide detailed explanations
- Use structured format when appropriate
- Consider edge cases
"""
    
    prompt1_template = f"""
Based on the user's request: "{user_prompt}"

Please provide a comprehensive response that includes:
1. Analysis of the request
2. Step-by-step solution
3. Code examples if applicable
4. Best practices and considerations

{common_instructions}
"""
    
    return prompt1_template
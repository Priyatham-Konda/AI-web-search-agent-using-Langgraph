from nodes.gemini_agent import gemini_generate
from nodes.tools import TOOL_REGISTRY

def tool_use_node(state: dict) -> dict:
    """
    ToolUse node: lets Gemini select from available tools and executes them.
    """
    available_tools = list(TOOL_REGISTRY.keys())
    processed_query = state.get('processed_query', '')
    prompt = (
        f"Given the query: '{processed_query}', which of these tools should I use? "
        f"Available tools: {', '.join(available_tools)}. "
        "Respond with a comma-separated list of tool names."
    )
    tools = gemini_generate(prompt)
    selected_tools = [t.strip() for t in tools.split(',') if t.strip() and t.strip() in available_tools]
    state['tools_needed'] = selected_tools
    # Execute selected tools and store results in state
    for tool_name in selected_tools:
        tool_func = TOOL_REGISTRY[tool_name]
        # For demo, pass processed_query or user_input as needed
        if tool_name == 'web_search':
            state = tool_func(processed_query, state)
        elif tool_name == 'calculator':
            state = tool_func(processed_query, state)
        # Add more tool logic as needed
    return state

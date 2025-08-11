def web_search_tool(query, state):
    # Use the web_search_node logic directly
    from nodes.web_search import web_search_node
    state['processed_query'] = query
    return web_search_node(state)

def calculator_tool(expression, state):
    # Simple calculator logic (safe eval for demo)
    try:
        result = str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        result = f"Calculator error: {e}"
    state['calculator_result'] = result
    return state

TOOL_REGISTRY = {
    "web_search": web_search_tool,
    "calculator": calculator_tool,
}

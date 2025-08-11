from nodes.gemini_agent import gemini_generate

def query_processor_node(state: dict) -> dict:
    """
    QueryProcessor node: uses Gemini to rephrase the user query for optimal search.
    """
    user_input = state.get('user_input', '')
    prompt = f"Rephrase the following user query for optimal web search: '{user_input}'"
    processed_query = gemini_generate(prompt)
    state['processed_query'] = processed_query.strip()
    return state

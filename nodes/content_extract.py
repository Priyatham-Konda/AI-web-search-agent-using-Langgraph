from nodes.gemini_agent import gemini_generate

def content_extract_node(state: dict) -> dict:
    """
    ContentExtract node: uses Gemini to extract relevant content from search results.
    """
    search_results = state.get('search_results', [])
    snippets = '\n'.join([r.get('snippet', '') for r in search_results])
    prompt = (
        f"Extract the most relevant facts or information from the following web search results for the query: '{state.get('processed_query', '')}'.\n"
        f"Results:\n{snippets}\nRespond with a bullet list."
    )
    extracted = gemini_generate(prompt)
    state['extracted_content'] = [line.strip('-• ') for line in extracted.split('\n') if line.strip()]
    return state

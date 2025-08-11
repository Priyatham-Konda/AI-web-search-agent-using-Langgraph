from nodes.gemini_agent import gemini_generate

def evaluator_node(state: dict) -> dict:
    """
    Evaluator node: uses Gemini to evaluate the quality of search results.
    """
    search_results = state.get('search_results', [])
    snippets = '\n'.join([r.get('snippet', '') for r in search_results])
    prompt = (
        f"Evaluate the following web search results for relevance and quality to the query: '{state.get('processed_query', '')}'.\n"
        f"Results:\n{snippets}\nRespond with 'good', 'average', or 'poor'."
    )
    evaluation = gemini_generate(prompt)
    state['evaluation_result'] = evaluation.strip().lower()
    return state

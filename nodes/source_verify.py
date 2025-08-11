from nodes.gemini_agent import gemini_generate

def source_verify_node(state: dict) -> dict:
    """
    SourceVerify node: uses Gemini to verify the credibility of sources from search results.
    """
    search_results = state.get('search_results', [])
    sources = [r.get('link', '') for r in search_results if r.get('link')]
    prompt = (
        "Given the following list of URLs, identify which are from reputable sources (e.g., .gov, .edu, major news, scientific journals):\n"
        + '\n'.join(sources) + "\nRespond with a comma-separated list of reputable URLs."
    )
    verified = gemini_generate(prompt)
    state['verified_sources'] = [url.strip() for url in verified.split(',') if url.strip()]
    return state

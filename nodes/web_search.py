import requests

def web_search_node(state: dict) -> dict:
    """
    WebSearch node: performs a real web search using SerpAPI and stores results.
    """
    query = state.get('processed_query', '')
    api_key = state.get('SERPAPI_KEY', 'YOUR_SERPAPI_KEY')  # Pass your key in state or set here
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        results = resp.json().get('organic_results', [])
        state['search_results'] = results
    except Exception as e:
        state['search_results'] = []
        state['web_search_error'] = str(e)
    return state

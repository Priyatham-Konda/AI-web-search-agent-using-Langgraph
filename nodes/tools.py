"""
Tool definitions using LangChain tools.
"""

import os
import requests
from typing import List
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

def web_search_function(query: str) -> str:
    """Perform web search using SerpAPI."""
    try:
        # Use SerpAPI if available
        api_key = os.getenv("SERPAPI_API_KEY")
        if api_key:
            search = SerpAPIWrapper(serpapi_api_key=api_key)
            results = search.run(query)
            return results
        else:
            # Fallback to a simple mock search
            return f"Mock search results for: {query}. Please set SERPAPI_API_KEY for real web search."
    except Exception as e:
        return f"Web search error: {str(e)}"

def calculator_function(expression: str) -> str:
    """Perform safe mathematical calculations."""
    try:
        # Remove any non-mathematical characters for safety
        allowed_chars = "0123456789+-*/.() "
        clean_expression = ''.join(c for c in expression if c in allowed_chars)
        
        if not clean_expression.strip():
            return "No valid mathematical expression found"
        
        # Safe evaluation
        result = eval(clean_expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def get_tools() -> List[Tool]:
    """Get all available tools."""
    tools = [
        Tool(
            name="web_search",
            description="Search the web for current information, news, facts, and answers to questions. Use this for any query that requires up-to-date information.",
            func=lambda query: web_search_function(query)
        ),
        Tool(
            name="calculator",
            description="Perform mathematical calculations. Can handle basic arithmetic, percentages, and simple mathematical expressions.",
            func=lambda expression: calculator_function(expression)
        )
    ]
    
    return tools
"""
Tool definitions using LangChain tools for ReAct agent.
Simplified and optimized for the ReAct pattern.
"""

import os
import requests
from typing import List
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

def web_search_function(query: str) -> str:
    """Perform web search using SerpAPI with better error handling."""
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if api_key:
            search = SerpAPIWrapper(serpapi_api_key=api_key)
            results = search.run(query)
            return results
        else:
            # Enhanced mock search for demo purposes
            return f"""Mock search results for: "{query}"

Top Results:
1. Recent information about {query} - This would contain current data from web search
2. Expert analysis on {query} - Detailed insights and explanations  
3. Latest developments in {query} - Up-to-date news and trends

Note: Set SERPAPI_API_KEY environment variable for real web search results."""
    except Exception as e:
        return f"Web search encountered an error: {str(e)}. Please try rephrasing your query."

def calculator_function(expression: str) -> str:
    """Perform safe mathematical calculations with enhanced capabilities."""
    try:
        # Clean the expression - allow mathematical operations
        import re
        
        # Extract mathematical expressions from natural language
        # Handle common patterns like "calculate X", "what is X", etc.
        expression = expression.lower()
        
        # Remove common words and extract mathematical parts
        math_patterns = [
            r'calculate\s+(.+)',
            r'what\s+is\s+(.+)',
            r'compute\s+(.+)',
            r'solve\s+(.+)',
            r'(\d+(?:\.\d+)?\s*[+\-*/]\s*\d+(?:\.\d+)?(?:\s*[+\-*/]\s*\d+(?:\.\d+)?)*)',
            r'(\d+(?:\.\d+)?(?:\s*%|\s+percent))',
        ]
        
        math_expression = None
        for pattern in math_patterns:
            match = re.search(pattern, expression)
            if match:
                math_expression = match.group(1).strip()
                break
        
        if not math_expression:
            math_expression = expression
        
        # Handle percentage calculations
        if '%' in math_expression or 'percent' in math_expression:
            # Extract numbers for percentage calculations
            numbers = re.findall(r'\d+(?:\.\d+)?', math_expression)
            if len(numbers) >= 2:
                base = float(numbers[0])
                percentage = float(numbers[1])
                result = (base * percentage) / 100
                return f"Result: {percentage}% of {base} = {result}"
        
        # Clean expression for safe evaluation
        allowed_chars = "0123456789+-*/.() "
        clean_expression = ''.join(c for c in math_expression if c in allowed_chars)
        
        if not clean_expression.strip():
            return "No valid mathematical expression found. Please provide a mathematical calculation."
        
        # Safe evaluation
        result = eval(clean_expression, {"__builtins__": {}})
        return f"Calculation: {clean_expression} = {result}"
        
    except Exception as e:
        return f"Calculation error: {str(e)}. Please check your mathematical expression."

def get_tools() -> List[Tool]:
    """Get all available tools for the ReAct agent."""
    tools = [
        Tool(
            name="web_search",
            description="""Search the web for current information, facts, news, and answers to questions. 
            Use this tool when you need:
            - Current events or recent news
            - Factual information or definitions
            - Research on any topic
            - Verification of claims or statements
            - Latest developments in any field
            Input should be a clear, specific search query.""",
            func=web_search_function
        ),
        Tool(
            name="calculator",
            description="""Perform mathematical calculations and solve math problems.
            Use this tool for:
            - Basic arithmetic (addition, subtraction, multiplication, division)
            - Percentage calculations
            - Mathematical expressions and equations
            - Number conversions
            - Statistical calculations
            Input can be a mathematical expression or word problem.""",
            func=calculator_function
        )
    ]
    
    return tools
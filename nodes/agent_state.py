"""
Define the agent state using LangGraph best practices.
"""

from typing import TypedDict, List, Dict, Any, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """State definition for the LangGraph agent."""
    user_input: str
    messages: Annotated[List[BaseMessage], operator.add]
    processed_query: str
    tools_to_use: List[str]
    tool_results: List[Dict[str, Any]]
    evaluation_result: str
    final_answer: str
    feedback: str
    memory_context: Dict[str, Any]
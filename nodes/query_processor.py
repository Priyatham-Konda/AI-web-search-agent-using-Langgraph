"""
Query Processor node using LangChain LLM integration.
"""

import os
from nodes.agent_state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def query_processor_node(state: AgentState) -> AgentState:
    """
    QueryProcessor node: uses LangChain ChatGoogleGenerativeAI to process queries.
    """
    user_input = state.get('user_input', '')
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Create messages for query processing
    messages = [
        SystemMessage(content="""You are a query optimization expert. 
        Rephrase user queries to be more effective for web search and information retrieval.
        Make the query specific, clear, and search-engine friendly.
        Return only the optimized query, nothing else."""),
        HumanMessage(content=f"Original query: {user_input}")
    ]
    
    try:
        response = llm.invoke(messages)
        processed_query = response.content.strip()
        state['processed_query'] = processed_query
        print(f"🔍 Query processed: '{processed_query}'")
    except Exception as e:
        print(f"❌ Query processing error: {e}")
        state['processed_query'] = user_input  # Fallback to original
    
    return state
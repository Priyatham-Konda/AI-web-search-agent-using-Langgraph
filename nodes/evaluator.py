"""
Evaluator node using LangChain for result evaluation.
"""

import os
from nodes.agent_state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def evaluator_node(state: AgentState) -> AgentState:
    """
    Evaluator node: evaluates the quality and relevance of tool results.
    """
    tool_results = state.get('tool_results', [])
    processed_query = state.get('processed_query', '')
    
    if not tool_results:
        state['evaluation_result'] = 'no_results'
        return state
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Prepare results summary for evaluation
    results_summary = []
    for result in tool_results:
        if result.get('success'):
            content = str(result.get('content', ''))[:500]  # Limit content length
            results_summary.append(f"Tool: {result.get('tool')}\nContent: {content}")
    
    results_text = "\n\n".join(results_summary)
    
    # Create messages for evaluation
    messages = [
        SystemMessage(content="""You are a result quality evaluator. 
        Evaluate how well the tool results answer the user's query.
        
        Rate the results as:
        - "excellent": Results directly and comprehensively answer the query
        - "good": Results are relevant and mostly answer the query
        - "fair": Results are somewhat relevant but incomplete
        - "poor": Results are not relevant or don't answer the query
        
        Return only the rating word, nothing else."""),
        HumanMessage(content=f"Query: {processed_query}\n\nResults:\n{results_text}")
    ]
    
    try:
        response = llm.invoke(messages)
        evaluation = response.content.strip().lower()
        state['evaluation_result'] = evaluation
        print(f"📊 Evaluation: {evaluation}")
        
    except Exception as e:
        print(f"❌ Evaluation error: {e}")
        state['evaluation_result'] = 'fair'  # Default fallback
    
    return state
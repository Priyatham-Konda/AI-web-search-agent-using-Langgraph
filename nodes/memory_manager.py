"""
Memory Manager node using LangGraph best practices.
"""

from nodes.agent_state import AgentState
from langchain_core.messages import HumanMessage

def memory_manager_node(state: AgentState) -> AgentState:
    """
    MemoryManager node: manages conversation history and context.
    """
    # Initialize memory context if not exists
    memory_context = state.get('memory_context', {})
    history = memory_context.get('history', [])
    
    # Add current user input to history
    if state.get('user_input'):
        history.append({'user': state['user_input'], 'timestamp': None})
        
        # Add to messages for LangChain compatibility
        messages = state.get('messages', [])
        messages.append(HumanMessage(content=state['user_input']))
        state['messages'] = messages
    
    # Keep only last 10 interactions to manage memory
    if len(history) > 10:
        history = history[-10:]
    
    memory_context['history'] = history
    state['memory_context'] = memory_context
    
    print("💾 Memory updated with conversation history")
    return state
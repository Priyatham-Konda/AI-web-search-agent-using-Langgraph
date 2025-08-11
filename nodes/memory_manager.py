def memory_manager_node(state: dict) -> dict:
    """
    MemoryManager node: stores and retrieves memory/context for the agent.
    Maintains conversation history and user preferences.
    """
    memory_context = state.get('memory_context', {})
    history = memory_context.get('history', [])
    # Add current user input to history
    if state.get('user_input'):
        history.append({'user': state['user_input']})
    memory_context['history'] = history
    state['memory_context'] = memory_context
    return state

def feedback_loop_node(state: dict) -> dict:
    """
    FeedbackLoop node: collects user feedback and logs it for active learning.
    """
    try:
        feedback = input("\nWas this answer helpful? (yes/no/other comments): ").strip()
    except Exception:
        feedback = ''
    state['feedback'] = feedback
    # Optionally, append feedback to memory_context for learning
    memory_context = state.get('memory_context', {})
    feedback_history = memory_context.get('feedback_history', [])
    feedback_history.append({'question': state.get('user_input', ''), 'answer': state.get('final_answer', ''), 'feedback': feedback})
    memory_context['feedback_history'] = feedback_history
    state['memory_context'] = memory_context
    return state

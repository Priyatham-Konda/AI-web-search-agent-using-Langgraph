"""
Feedback Loop node for continuous learning.
"""

from nodes.agent_state import AgentState

def feedback_loop_node(state: AgentState) -> AgentState:
    """
    Feedback loop node: collects user feedback for continuous improvement.
    """
    try:
        print("\n" + "="*50)
        feedback = input("💭 Was this answer helpful? (yes/no/comments): ").strip()
        
        if feedback:
            state['feedback'] = feedback
            
            # Store feedback in memory context for learning
            memory_context = state.get('memory_context', {})
            feedback_history = memory_context.get('feedback_history', [])
            
            feedback_entry = {
                'question': state.get('user_input', ''),
                'answer': state.get('final_answer', ''),
                'feedback': feedback,
                'evaluation': state.get('evaluation_result', ''),
                'tools_used': state.get('tools_to_use', [])
            }
            
            feedback_history.append(feedback_entry)
            
            # Keep only last 20 feedback entries
            if len(feedback_history) > 20:
                feedback_history = feedback_history[-20:]
            
            memory_context['feedback_history'] = feedback_history
            state['memory_context'] = memory_context
            
            print("📝 Feedback recorded for future improvements")
        else:
            state['feedback'] = ''
            
    except (EOFError, KeyboardInterrupt):
        state['feedback'] = ''
        print("\n⏭️ Skipping feedback collection")
    except Exception as e:
        print(f"❌ Feedback collection error: {e}")
        state['feedback'] = ''
    
    return state
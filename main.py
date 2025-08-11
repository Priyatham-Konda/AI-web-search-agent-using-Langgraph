"""
Main entry point for the LangGraph AI agent project.
Uses LangGraph built-in functions for cleaner, more maintainable code.
"""

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, List, Dict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Import nodes
from nodes.agent_state import AgentState
from nodes.memory_manager import memory_manager_node
from nodes.query_processor import query_processor_node
from nodes.tool_selector import tool_selector_node
from nodes.tool_executor import tool_executor_node
from nodes.evaluator import evaluator_node
from nodes.answer_synth import answer_synth_node
from nodes.feedback_loop import feedback_loop_node
from nodes.tools import get_tools

def should_continue(state: AgentState) -> str:
    """Determine if we should continue to tool execution or move to evaluation."""
    if state.get("tools_to_use"):
        return "execute_tools"
    return "evaluate"

def create_agent_workflow():
    """Create the LangGraph workflow using built-in functions."""
    
    # Initialize the state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("memory_manager", memory_manager_node)
    workflow.add_node("query_processor", query_processor_node)
    workflow.add_node("tool_selector", tool_selector_node)
    workflow.add_node("tool_executor", tool_executor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("answer_synth", answer_synth_node)
    workflow.add_node("feedback_loop", feedback_loop_node)
    
    # Set entry point
    workflow.set_entry_point("memory_manager")
    
    # Define the flow with conditional logic
    workflow.add_edge("memory_manager", "query_processor")
    workflow.add_edge("query_processor", "tool_selector")
    
    # Conditional edge based on whether tools are needed
    workflow.add_conditional_edges(
        "tool_selector",
        should_continue,
        {
            "execute_tools": "tool_executor",
            "evaluate": "evaluator"
        }
    )
    
    workflow.add_edge("tool_executor", "evaluator")
    workflow.add_edge("evaluator", "answer_synth")
    workflow.add_edge("answer_synth", "feedback_loop")
    workflow.add_edge("feedback_loop", END)
    
    # Compile the workflow
    return workflow.compile()

def main():
    """Main execution function."""
    
    print("🤖 LangGraph AI Search Agent (Refactored)")
    print("-" * 50)
    
    # Verify API keys
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set GOOGLE_API_KEY in your .env file")
        return
    
    # Create the workflow
    app = create_agent_workflow()
    
    while True:
        try:
            user_input = input('\nAsk a question (or "quit" to exit): ').strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
                
            if not user_input:
                continue
            
            # Initialize state
            initial_state = {
                'user_input': user_input,
                'messages': [],
                'processed_query': '',
                'tools_to_use': [],
                'tool_results': [],
                'evaluation_result': '',
                'final_answer': '',
                'feedback': '',
                'memory_context': {}
            }
            
            print("\n🔄 Processing through the graph...")
            
            # Execute the workflow
            result = app.invoke(initial_state)
            
            # Display the final answer
            print('\n' + '='*60)
            print('🎯 FINAL ANSWER:')
            print('='*60)
            print(result.get('final_answer', 'No answer generated.'))
            
            # Show tool results if available
            if result.get('tool_results'):
                print('\n📊 Information Sources:')
                for i, tool_result in enumerate(result['tool_results'][:3], 1):
                    if isinstance(tool_result, dict) and 'content' in tool_result:
                        content = str(tool_result['content'])[:100] + "..." if len(str(tool_result['content'])) > 100 else str(tool_result['content'])
                        print(f"  {i}. {content}")
            
            if result.get('feedback'):
                print(f'\n💭 Feedback: {result["feedback"]}')
                
        except KeyboardInterrupt:
            print("\n\nExiting... 👋")
            break
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()
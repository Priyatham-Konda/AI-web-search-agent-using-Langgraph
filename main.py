"""
Main entry point for the LangGraph AI agent project.
Defines the graph structure and orchestrates the flow between nodes.
"""


from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict

# Gemini agent utility
import google.generativeai as genai

def gemini_generate(prompt: str, model_name: str = 'gemini-pro') -> str:
    """
    Utility to call Gemini LLM for text generation.
    """
    genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your Gemini API key or load from env
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)

# Import your node functions
from nodes.memory_manager import memory_manager_node
from nodes.query_processor import query_processor_node
from nodes.tool_use import tool_use_node
from nodes.web_search import web_search_node
from nodes.evaluator import evaluator_node
from nodes.content_extract import content_extract_node
from nodes.source_verify import source_verify_node
from nodes.answer_synth import answer_synth_node
from nodes.feedback_loop import feedback_loop_node

# Proper state definition
class AgentState(TypedDict):
    user_input: str
    processed_query: str
    tools_needed: List[str]
    search_results: List[Dict]
    evaluation_result: str
    extracted_content: List[str]
    verified_sources: List[str]
    final_answer: str
    feedback: str
    memory_context: Dict

def create_agent_workflow():
    """Create the LangGraph workflow based on your sequential flow"""
    
    # Initialize the state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes in your specified order
    workflow.add_node("MemoryManager", memory_manager_node)
    workflow.add_node("QueryProcessor", query_processor_node)
    workflow.add_node("ToolUse", tool_use_node)
    workflow.add_node("WebSearch", web_search_node)
    workflow.add_node("Evaluator", evaluator_node)
    workflow.add_node("ContentExtract", content_extract_node)
    workflow.add_node("SourceVerify", source_verify_node)
    workflow.add_node("AnswerSynth", answer_synth_node)
    workflow.add_node("FeedbackLoop", feedback_loop_node)
    
    # Set entry point
    workflow.set_entry_point("MemoryManager")
    
    # Define the exact sequential flow you specified
    workflow.add_edge("MemoryManager", "QueryProcessor")
    workflow.add_edge("QueryProcessor", "ToolUse")
    workflow.add_edge("ToolUse", "WebSearch")
    workflow.add_edge("WebSearch", "Evaluator")
    workflow.add_edge("Evaluator", "ContentExtract")
    workflow.add_edge("ContentExtract", "SourceVerify")
    workflow.add_edge("SourceVerify", "AnswerSynth")
    workflow.add_edge("AnswerSynth", "FeedbackLoop")
    workflow.add_edge("FeedbackLoop", END)
    
    # Compile the workflow
    return workflow.compile()

def main():
    """Main execution function following your structure"""
    
    print("🤖 LangGraph AI Search Agent")
    print("-" * 40)
    
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
            
            # Initialize state with your structure
            initial_state = AgentState({
                'user_input': user_input,
                'processed_query': '',
                'tools_needed': [],
                'search_results': [],
                'evaluation_result': '',
                'extracted_content': [],
                'verified_sources': [],
                'final_answer': '',
                'feedback': '',
                'memory_context': {}
            })
            
            print("\n🔄 Processing through your graph flow...")
            
            # Execute the workflow
            result = app.invoke(initial_state)
            
            # Display the final answer
            print('\n' + '='*50)
            print('🎯 FINAL ANSWER:')
            print('='*50)
            print(result.get('final_answer', 'No answer generated.'))
            
            # Show additional info if available
            if result.get('verified_sources'):
                print('\n📚 Sources:')
                for i, source in enumerate(result['verified_sources'][:3], 1):
                    print(f"  {i}. {source}")
            
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

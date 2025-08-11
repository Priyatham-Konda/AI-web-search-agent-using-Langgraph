"""
Alternative main.py with centralized LLM approach.
This demonstrates the centralized LLM pattern.
"""

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, create_react_agent
from typing import TypedDict, List, Dict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Import nodes and tools
from nodes.agent_state import AgentState
from nodes.tools import get_tools

def create_centralized_llm_agent():
    """
    Create agent using centralized LLM approach with LangGraph's built-in functions.
    This is the most LangGraph-native approach.
    """
    
    # Verify API key
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set GOOGLE_API_KEY in your .env file")
    
    # Initialize the centralized LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Get tools
    tools = get_tools()
    
    # Create ReAct agent using LangGraph's built-in function
    # This handles tool selection, execution, and reasoning automatically
    agent = create_react_agent(
        llm, 
        tools,
        state_schema=AgentState,
        system_message="""You are a helpful AI assistant with access to web search and calculator tools.

Guidelines:
1. Use web_search for any questions requiring current information, facts, or research
2. Use calculator for mathematical calculations
3. Provide comprehensive, accurate answers
4. Cite sources when using web search results
5. If you cannot find relevant information, acknowledge limitations clearly

Always think step by step and use the most appropriate tools for each query."""
    )
    
    return agent

def create_hybrid_agent():
    """
    Create agent using hybrid approach - centralized LLM with custom nodes.
    This gives more control while still using LangGraph patterns.
    """
    
    # Initialize the centralized LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Get tools
    tools = get_tools()
    tool_executor = ToolExecutor(tools)
    
    def agent_node(state: AgentState) -> AgentState:
        """Main agent node with centralized LLM."""
        messages = state.get('messages', [])
        
        # Add system message if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            system_msg = SystemMessage(content="""You are a helpful AI assistant with access to tools.
            
Available tools:
- web_search: Search the web for current information
- calculator: Perform mathematical calculations

Use tools when needed and provide comprehensive answers.""")
            messages = [system_msg] + messages
        
        # Get LLM response
        response = llm.invoke(messages)
        messages.append(response)
        state['messages'] = messages
        
        # Check if tools are needed (simplified logic)
        if hasattr(response, 'tool_calls') and response.tool_calls:
            state['tools_to_use'] = [call['name'] for call in response.tool_calls]
        else:
            state['tools_to_use'] = []
            state['final_answer'] = response.content
        
        return state
    
    def tool_node(state: AgentState) -> AgentState:
        """Execute tools using ToolExecutor."""
        tools_to_use = state.get('tools_to_use', [])
        if not tools_to_use:
            return state
        
        # Execute tools (simplified)
        tool_results = []
        for tool_name in tools_to_use:
            # This would use proper tool calling in practice
            result = f"Mock result from {tool_name}"
            tool_results.append({'tool': tool_name, 'result': result})
        
        state['tool_results'] = tool_results
        return state
    
    def should_continue(state: AgentState) -> str:
        """Determine next step."""
        if state.get('tools_to_use'):
            return "tools"
        return END
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

def main():
    """Main execution with different agent options."""
    
    print("🤖 LangGraph AI Agent - Architecture Comparison")
    print("-" * 60)
    print("1. Centralized LLM (ReAct Agent) - Most LangGraph-native")
    print("2. Hybrid Approach - More control")
    print("3. Distributed LLM - Current approach")
    
    choice = input("\nChoose approach (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🚀 Using Centralized LLM (ReAct Agent)")
        app = create_centralized_llm_agent()
    elif choice == "2":
        print("\n🚀 Using Hybrid Approach")
        app = create_hybrid_agent()
    else:
        print("\n🚀 Using Distributed LLM (Current)")
        from main import create_agent_workflow
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
                'messages': [HumanMessage(content=user_input)],
                'processed_query': user_input,
                'tools_to_use': [],
                'tool_results': [],
                'evaluation_result': '',
                'final_answer': '',
                'feedback': '',
                'memory_context': {}
            }
            
            print("\n🔄 Processing...")
            
            # Execute the workflow
            result = app.invoke(initial_state)
            
            # Display result
            if choice == "1":
                # ReAct agent returns messages
                messages = result.get('messages', [])
                if messages:
                    print('\n' + '='*60)
                    print('🎯 FINAL ANSWER:')
                    print('='*60)
                    print(messages[-1].content)
            else:
                # Other approaches
                print('\n' + '='*60)
                print('🎯 FINAL ANSWER:')
                print('='*60)
                print(result.get('final_answer', 'No answer generated.'))
                
        except KeyboardInterrupt:
            print("\n\nExiting... 👋")
            break
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()
"""
Simplified main.py using LangGraph's create_react_agent - RECOMMENDED APPROACH
This is the most LangGraph-native way to build agents.
"""

import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from nodes.tools import get_tools

# Load environment variables
load_dotenv()

def create_react_agent_app():
    """
    Create a ReAct agent using LangGraph's built-in function.
    This is the recommended approach for most use cases.
    """
    
    # Verify API key
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("❌ Please set GOOGLE_API_KEY in your .env file")
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Get tools
    tools = get_tools()
    
    # Create ReAct agent - this handles everything automatically!
    agent = create_react_agent(
        llm, 
        tools,
        system_message="""You are a helpful AI research assistant with access to web search and calculator tools.

**Guidelines:**
1. **For factual questions**: Always use web_search to get current, accurate information
2. **For calculations**: Use the calculator tool for any mathematical operations
3. **Be comprehensive**: Provide detailed, well-structured answers
4. **Cite sources**: When using web search, mention the sources of information
5. **Acknowledge limitations**: If you cannot find relevant information, say so clearly
6. **Think step-by-step**: Break down complex questions into manageable parts

**Tool Usage:**
- Use web_search for: current events, facts, research, definitions, recent developments
- Use calculator for: math problems, percentages, conversions, statistical calculations

Always prioritize accuracy and provide the most helpful response possible."""
    )
    
    return agent

def main():
    """Main execution function using ReAct agent."""
    
    print("🤖 LangGraph ReAct Agent - Simplified & Powerful")
    print("=" * 55)
    print("✨ Using LangGraph's built-in create_react_agent")
    print("🔧 Automatic tool selection and execution")
    print("🧠 ReAct (Reasoning + Acting) pattern")
    print("-" * 55)
    
    try:
        # Create the agent
        agent = create_react_agent_app()
        print("✅ Agent initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Main interaction loop
    while True:
        try:
            user_input = input('\n💬 Ask a question (or "quit" to exit): ').strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
            
            print("\n🔄 Processing your question...")
            print("-" * 40)
            
            # Execute the agent - simple one-liner!
            result = agent.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            
            # Extract and display the final answer
            messages = result.get("messages", [])
            if messages:
                final_message = messages[-1]
                
                print('\n' + '='*60)
                print('🎯 ANSWER:')
                print('='*60)
                print(final_message.content)
                
                # Show tool usage if any
                tool_calls_made = []
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tool_calls_made.append(tool_call.get('name', 'unknown'))
                
                if tool_calls_made:
                    print(f'\n🛠️ Tools used: {", ".join(set(tool_calls_made))}')
            else:
                print("❌ No response generated")
                
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different question.")
            continue

if __name__ == "__main__":
    main()
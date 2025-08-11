"""
Main entry point for the LangGraph AI agent using ReAct pattern.
This is the recommended LangGraph approach using built-in functions.
"""

import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from nodes.tools import get_tools

# Load environment variables
load_dotenv()

def create_agent():
    """
    Create a ReAct agent using LangGraph's built-in function.
    This replaces the entire distributed node architecture with a single, powerful agent.
    """
    
    # Verify API key
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("❌ Please set GOOGLE_API_KEY in your .env file")
    
    # Initialize LLM - single instance for the entire agent
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

**Your Capabilities:**
- Web Search: Get current information, facts, news, and research
- Calculator: Perform mathematical calculations and analysis
- Memory: Remember conversation context and learn from feedback

**Guidelines:**
1. **Always use tools when needed**: Don't guess when you can search or calculate
2. **For factual questions**: Use web_search to get current, accurate information
3. **For calculations**: Use calculator for any mathematical operations
4. **Be comprehensive**: Provide detailed, well-structured answers
5. **Cite sources**: When using web search, mention sources of information
6. **Think step-by-step**: Break down complex questions into manageable parts
7. **Acknowledge limitations**: If you cannot find relevant information, say so clearly

**Tool Usage Examples:**
- Current events, facts, definitions → web_search
- Math problems, percentages, conversions → calculator
- Research questions → web_search
- Data analysis → calculator + web_search

Always prioritize accuracy and provide the most helpful response possible."""
    )
    
    return agent

def collect_feedback(question: str, answer: str) -> str:
    """Simple feedback collection for continuous improvement."""
    try:
        print("\n" + "="*50)
        feedback = input("💭 Was this answer helpful? (yes/no/comments): ").strip()
        if feedback:
            print("📝 Feedback recorded - thank you!")
            return feedback
        return ""
    except (EOFError, KeyboardInterrupt):
        print("\n⏭️ Skipping feedback")
        return ""

def main():
    """Main execution function using ReAct agent."""
    
    print("🤖 LangGraph AI Agent - ReAct Pattern")
    print("=" * 50)
    print("✨ Powered by LangGraph's create_react_agent")
    print("🔧 Automatic tool selection and execution")
    print("🧠 ReAct (Reasoning + Acting) pattern")
    print("💡 Minimal code, maximum power")
    print("-" * 50)
    
    try:
        # Create the agent
        agent = create_agent()
        print("✅ Agent initialized successfully!")
        
        # Simple conversation memory
        conversation_history = []
        
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
            
            # Prepare messages with conversation history
            messages = []
            
            # Add recent conversation context (last 3 exchanges)
            for exchange in conversation_history[-3:]:
                messages.append(HumanMessage(content=exchange['question']))
                messages.append(HumanMessage(content=f"Previous answer: {exchange['answer'][:200]}..."))
            
            # Add current question
            messages.append(HumanMessage(content=user_input))
            
            # Execute the agent
            result = agent.invoke({"messages": messages})
            
            # Extract and display the final answer
            agent_messages = result.get("messages", [])
            if agent_messages:
                final_message = agent_messages[-1]
                answer = final_message.content
                
                print('\n' + '='*60)
                print('🎯 ANSWER:')
                print('='*60)
                print(answer)
                
                # Show tool usage
                tool_calls_made = []
                for msg in agent_messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tool_calls_made.append(tool_call.get('name', 'unknown'))
                
                if tool_calls_made:
                    print(f'\n🛠️ Tools used: {", ".join(set(tool_calls_made))}')
                
                # Store in conversation history
                conversation_history.append({
                    'question': user_input,
                    'answer': answer,
                    'tools_used': list(set(tool_calls_made))
                })
                
                # Collect feedback
                feedback = collect_feedback(user_input, answer)
                if feedback:
                    conversation_history[-1]['feedback'] = feedback
                
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
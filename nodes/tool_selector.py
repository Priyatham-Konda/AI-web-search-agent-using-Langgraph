"""
Tool Selector node using LangChain for intelligent tool selection.
"""

import os
from nodes.agent_state import AgentState
from nodes.tools import get_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def tool_selector_node(state: AgentState) -> AgentState:
    """
    Tool selector node: uses LLM to intelligently select appropriate tools.
    """
    processed_query = state.get('processed_query', '')
    available_tools = get_tools()
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Create tool descriptions
    tool_descriptions = []
    for tool in available_tools:
        tool_descriptions.append(f"- {tool.name}: {tool.description}")
    
    tools_text = "\n".join(tool_descriptions)
    
    # Create messages for tool selection
    messages = [
        SystemMessage(content=f"""You are a tool selection expert. Given a query, select the most appropriate tools from the available options.

Available tools:
{tools_text}

Rules:
1. Select only tools that are directly relevant to answering the query
2. For factual questions, always include web_search
3. For calculations, include calculator
4. Return tool names as a comma-separated list
5. If no tools are needed, return "none"
6. Return only the tool names, nothing else"""),
        HumanMessage(content=f"Query: {processed_query}")
    ]
    
    try:
        response = llm.invoke(messages)
        selected_tools_text = response.content.strip().lower()
        
        if selected_tools_text == "none":
            selected_tools = []
        else:
            # Parse selected tools
            selected_tools = []
            tool_names = [tool.name for tool in available_tools]
            
            for tool_name in selected_tools_text.split(','):
                tool_name = tool_name.strip()
                if tool_name in tool_names:
                    selected_tools.append(tool_name)
        
        state['tools_to_use'] = selected_tools
        print(f"🛠️ Selected tools: {selected_tools}")
        
    except Exception as e:
        print(f"❌ Tool selection error: {e}")
        state['tools_to_use'] = ["web_search"]  # Default fallback
    
    return state
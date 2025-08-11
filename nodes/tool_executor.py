"""
Tool Executor node using LangGraph's ToolExecutor.
"""

from nodes.agent_state import AgentState
from nodes.tools import get_tools
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import ToolMessage

def tool_executor_node(state: AgentState) -> AgentState:
    """
    Tool executor node: executes selected tools using LangGraph's ToolExecutor.
    """
    tools_to_use = state.get('tools_to_use', [])
    processed_query = state.get('processed_query', '')
    
    if not tools_to_use:
        print("⚠️ No tools to execute")
        return state
    
    # Get available tools
    available_tools = get_tools()
    tools_dict = {tool.name: tool for tool in available_tools}
    
    # Execute each selected tool
    tool_results = []
    
    for tool_name in tools_to_use:
        if tool_name in tools_dict:
            tool = tools_dict[tool_name]
            print(f"🔧 Executing tool: {tool_name}")
            
            try:
                # Execute the tool with the processed query
                if tool_name == "web_search":
                    result = tool.invoke({"query": processed_query})
                elif tool_name == "calculator":
                    # For calculator, try to extract mathematical expressions
                    result = tool.invoke({"expression": processed_query})
                else:
                    result = tool.invoke({"input": processed_query})
                
                tool_results.append({
                    "tool": tool_name,
                    "content": result,
                    "success": True
                })
                
            except Exception as e:
                print(f"❌ Error executing {tool_name}: {e}")
                tool_results.append({
                    "tool": tool_name,
                    "content": f"Error: {str(e)}",
                    "success": False
                })
    
    state['tool_results'] = tool_results
    print(f"✅ Executed {len(tool_results)} tools")
    
    return state
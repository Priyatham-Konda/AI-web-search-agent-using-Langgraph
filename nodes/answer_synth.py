"""
Answer Synthesis node using LangChain for comprehensive answer generation.
"""

import os
from nodes.agent_state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def answer_synth_node(state: AgentState) -> AgentState:
    """
    Answer synthesis node: creates a comprehensive answer using LangChain.
    """
    user_input = state.get('user_input', '')
    tool_results = state.get('tool_results', [])
    evaluation_result = state.get('evaluation_result', '')
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3  # Slightly higher for more natural responses
    )
    
    # Prepare context from tool results
    context_parts = []
    for result in tool_results:
        if result.get('success'):
            tool_name = result.get('tool', 'unknown')
            content = str(result.get('content', ''))
            context_parts.append(f"From {tool_name}: {content}")
    
    context = "\n\n".join(context_parts) if context_parts else "No additional context available."
    
    # Create messages for answer synthesis
    messages = [
        SystemMessage(content=f"""You are a helpful AI assistant that provides comprehensive, accurate answers.

Guidelines:
1. Answer the user's question directly and clearly
2. Use the provided context to support your answer
3. If the context is insufficient, acknowledge limitations
4. Be concise but thorough
5. Cite sources when relevant
6. If you cannot answer based on the context, say so clearly

Context quality: {evaluation_result}"""),
        HumanMessage(content=f"""Question: {user_input}

Context:
{context}

Please provide a comprehensive answer to the question.""")
    ]
    
    try:
        response = llm.invoke(messages)
        final_answer = response.content.strip()
        state['final_answer'] = final_answer
        print("✨ Answer synthesized successfully")
        
    except Exception as e:
        print(f"❌ Answer synthesis error: {e}")
        state['final_answer'] = "I apologize, but I encountered an error while generating the answer. Please try again."
    
    return state
# LangGraph AI Search Agent (Refactored)

A sophisticated AI agent built with LangGraph that uses built-in functions for cleaner, more maintainable code.

## Features

- **Memory Management**: Maintains conversation history and context
- **Intelligent Query Processing**: Optimizes user queries for better results
- **Smart Tool Selection**: Uses LLM to select appropriate tools
- **Tool Execution**: Leverages LangGraph's built-in ToolExecutor
- **Result Evaluation**: Assesses the quality of retrieved information
- **Answer Synthesis**: Creates comprehensive responses
- **Feedback Loop**: Learns from user interactions

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   
   Required API keys:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `SERPAPI_API_KEY`: Your SerpAPI key (optional, will use mock search if not provided)

3. **Run the Agent**:
   ```bash
   python main.py
   ```

## Architecture

The agent uses a sequential flow with conditional logic:

1. **Memory Manager**: Manages conversation history
2. **Query Processor**: Optimizes user queries using LangChain
3. **Tool Selector**: Intelligently selects appropriate tools
4. **Tool Executor**: Executes tools using LangGraph's ToolExecutor
5. **Evaluator**: Assesses result quality
6. **Answer Synthesis**: Creates comprehensive responses
7. **Feedback Loop**: Collects user feedback for improvement

## Key Improvements

- **LangChain Integration**: Uses `ChatGoogleGenerativeAI` for consistent LLM interactions
- **Built-in ToolExecutor**: Leverages LangGraph's tool execution capabilities
- **Proper State Management**: Uses TypedDict with proper annotations
- **Conditional Logic**: Smart routing based on tool selection
- **Error Handling**: Robust error handling throughout the pipeline
- **Memory Management**: Efficient conversation history management
- **Modular Design**: Clean separation of concerns

## Available Tools

- **Web Search**: Real-time web search using SerpAPI
- **Calculator**: Safe mathematical calculations

## Usage Examples

```
Ask a question (or "quit" to exit): What is the current weather in New York?
Ask a question (or "quit" to exit): Calculate 15% of 250
Ask a question (or "quit" to exit): What are the latest developments in AI?
```

The agent will automatically select appropriate tools and provide comprehensive answers based on the retrieved information.
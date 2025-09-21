# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph-based SQL robot application with a Next.js frontend UI. The main components are:

1. A Python backend (`graph.py`) that implements a LangGraph agent with multiple tools for:
   - SQL database querying and data extraction
   - Python code execution
   - Data visualization
   - Web search capabilities

2. A Next.js frontend UI (`agent-chat-ui/`) that provides a chat interface for interacting with the LangGraph agent.

## Key Files and Architecture

### Backend (Python)
- `graph.py`: Main LangGraph implementation with agent logic and tool definitions
- `.env`: Environment variables including database credentials and API keys
- `langgraph.json`: LangGraph configuration file

### Frontend (Next.js)
- `agent-chat-ui/`: Complete Next.js application for chat interface
- `agent-chat-ui/package.json`: Dependencies and scripts for the frontend

## Development Commands

### Backend Development
```bash
# Run the LangGraph server (command would depend on how it's deployed)
# The graph is defined in graph.py and configured in langgraph.json
```

### Frontend Development
```bash
# Navigate to the frontend directory
cd agent-chat-ui

# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build for production
pnpm build

# Run linting
pnpm lint
pnpm lint:fix

# Format code
pnpm format
pnpm format:check
```

## Environment Variables

The project uses environment variables defined in `.env`:
- Database connection: HOST, PORT, USER, PASSWORD, DATABASE
- API keys: DEEPSEEK_API_KEY, OPENAI_API_KEY, TAVILY_API_KEY
- LangSmith configuration: LANGSMITH_TRACING, LANGSMITH_ENDPOINT, LANGSMITH_API_KEY, LANGSMITH_PROJECT
- Frontend configuration: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_ASSISTANT_ID

## Code Architecture

The Python backend implements a LangGraph agent with five main tools:
1. `sql_inter`: Execute SQL queries on a MySQL database
2. `extract_data`: Extract data from MySQL to pandas DataFrames
3. `python_inter`: Execute Python code (non-plotting)
4. `fig_inter`: Execute Python code for data visualization
5. `search_tool`: Web search using Tavily

The frontend uses the Agent Chat UI pattern to communicate with the LangGraph backend through a streaming API interface.
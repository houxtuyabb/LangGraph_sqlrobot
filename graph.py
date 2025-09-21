import os
from typing import TypedDict, List, Annotated
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.constants import END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from tools import search_tool, sql_inter, extract_data, python_inter, fig_inter



load_dotenv(override=True)


tools = [search_tool,sql_inter,extract_data,python_inter,fig_inter]
tool_node = ToolNode(tools=tools)

model = ChatDeepSeek(model="deepseek-chat")
model_with_tools = model.bind_tools(tools, tool_choice="auto")

class AgentState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage | ToolMessage], add_messages]
    user_input: str

def create_agent_graph():
    workflow = StateGraph(AgentState)

    def agent_node(state: AgentState):
        """智能体节点"""
        messages = state.get("messages", [])
        user_input = state.get("user_input", None)

        if user_input:
            messages = messages + [HumanMessage(content=user_input)]
            user_input = None

        elif not messages:
            messages = [HumanMessage(content="你有什么功能？")]

        response = model_with_tools.invoke(messages)

        return {
            "messages": messages + [response],
            "user_input": user_input
        }

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")



    workflow.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END
        }
    )

    workflow.add_edge("tools", "agent")


    return workflow.compile()

graph = create_agent_graph()










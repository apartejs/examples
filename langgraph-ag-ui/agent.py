"""A LangGraph agent served over AG-UI, with a tool that waits for a person."""

import os
from typing import Annotated

from ag_ui_langgraph import LangGraphAgent, add_langgraph_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt

load_dotenv()


@tool
def send_email(to: str, subject: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Send an email. A person has to approve it first."""
    # The reason and the call's id are what make the chat open its approval panel.
    answer = interrupt({"reason": "tool_call", "toolCallId": tool_call_id, "message": f"Send this email to {to}?"})
    if not (isinstance(answer, dict) and answer.get("approved")):
        return "The user refused: the email was not sent."
    return f"Email sent to {to}: {subject}"


def make_model():
    if os.environ.get("MODEL"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=os.environ["MODEL"], streaming=True)

    from scripted_model import ScriptedModel

    return ScriptedModel()


tools = [send_email]
model = make_model().bind_tools(tools)


async def call_model(state: MessagesState):
    return {"messages": [await model.ainvoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

app = FastAPI()
add_langgraph_fastapi_endpoint(
    app,
    # emit_interrupt_outcome: a pause ends the run the way AG-UI 1.0 describes it, which is what the chat reads.
    LangGraphAgent(name="assistant", graph=builder.compile(checkpointer=MemorySaver()), emit_interrupt_outcome=True),
    path="/agent",
)

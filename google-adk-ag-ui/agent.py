"""A Google ADK agent served over AG-UI, with a tool that waits for a person."""

import os

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

load_dotenv()


def send_email(to: str, subject: str) -> str:
    """Send an email. A person has to approve it first."""
    return f"Email sent to {to}: {subject}"


def make_model():
    if os.environ.get("MODEL"):
        return os.environ["MODEL"]

    from scripted_model import ScriptedModel

    return ScriptedModel()


agent = LlmAgent(
    name="assistant",
    model=make_model(),
    instruction="You help the user. Send an email only when asked to.",
    tools=[FunctionTool(send_email, require_confirmation=True)],
)

app = FastAPI()
add_adk_fastapi_endpoint(
    app,
    # emit_interrupt_outcome: a pause ends the run the way AG-UI 1.0 describes it, which is what the chat reads.
    ADKAgent(adk_agent=agent, app_name="example", user_id="reader", emit_interrupt_outcome=True),
    path="/agent",
)

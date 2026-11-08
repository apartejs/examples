"""A Pydantic AI agent served over AG-UI, with a tool that waits for a person."""

import os

from dotenv import load_dotenv
from pydantic_ai import Agent, DeferredToolRequests
from pydantic_ai.ui.ag_ui import AGUIAdapter
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

load_dotenv()


def make_model():
    if os.environ.get("MODEL"):
        from pydantic_ai.models.openai import OpenAIChatModel

        return OpenAIChatModel(os.environ["MODEL"])

    from scripted_model import scripted_model

    return scripted_model


# DeferredToolRequests in the output is what lets a run stop and wait for an approval.
agent = Agent(make_model(), output_type=[str, DeferredToolRequests])


@agent.tool_plain(requires_approval=True)
def send_email(to: str, subject: str) -> str:
    """Send an email. A person has to approve it first."""
    return f"Email sent to {to}: {subject}"


async def run_agent(request: Request) -> Response:
    return await AGUIAdapter.dispatch_request(request, agent=agent)


app = Starlette(routes=[Route("/agent", run_agent, methods=["POST"])])

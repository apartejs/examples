"""Answers when no model is configured, and says so. It streams word by word, as a real model does."""

import json
from collections.abc import AsyncIterator
from uuid import uuid4

from pydantic_ai.messages import ModelMessage, ToolReturnPart
from pydantic_ai.models.function import AgentInfo, DeltaToolCall, DeltaToolCalls, FunctionModel

NOTE = "This is a scripted reply: set MODEL in .env to talk to a real model."


async def stream(messages: list[ModelMessage], info: AgentInfo) -> AsyncIterator[str | DeltaToolCalls]:
    last = messages[-1].parts[-1]
    if isinstance(last, ToolReturnPart):
        text = f"{last.content} {NOTE}"
    elif "email" in str(last.content).lower():
        args = {"to": "ada@example.com", "subject": "Hello from Pydantic AI"}
        yield {0: DeltaToolCall(name="send_email", json_args=json.dumps(args), tool_call_id=f"call_{uuid4().hex}")}
        return
    else:
        text = f"{NOTE} Ask me to **send an email** to see a tool wait for your approval."
    for i, word in enumerate(text.split(" ")):
        yield word if i == 0 else f" {word}"


scripted_model = FunctionModel(stream_function=stream)

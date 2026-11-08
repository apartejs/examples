"""Answers when no model is configured, and says so. It streams word by word, as a real model does."""

from collections.abc import AsyncGenerator
from uuid import uuid4

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

NOTE = "This is a scripted reply: set MODEL in .env to talk to a real model."


def text_response(text: str, partial: bool) -> LlmResponse:
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]), partial=partial)


class ScriptedModel(BaseLlm):
    model: str = "scripted"

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        last = llm_request.contents[-1].parts[-1]
        if last.function_response:
            response = last.function_response.response or {}
            text = f"{response.get('result') or response.get('error')} {NOTE}"
        elif "email" in (last.text or "").lower():
            call = types.FunctionCall(id=f"call_{uuid4().hex}", name="send_email", args={"to": "ada@example.com", "subject": "Hello from Google ADK"})
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=call)]))
            return
        else:
            text = f"{NOTE} Ask me to **send an email** to see a tool wait for your approval."

        if stream:
            words = text.split(" ")
            for i, word in enumerate(words):
                yield text_response(word if i == 0 else f" {word}", partial=True)
        yield text_response(text, partial=False)

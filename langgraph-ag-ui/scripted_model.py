"""Answers when no model is configured, and says so. It streams word by word, as a real model does."""

import json
from typing import Any, Iterator
from uuid import uuid4

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult

NOTE = "This is a scripted reply: set MODEL in .env to talk to a real model."


class ScriptedModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "scripted"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "ScriptedModel":
        return self

    def _reply(self, messages: list[BaseMessage]) -> AIMessage:
        last = messages[-1]
        if isinstance(last, ToolMessage):
            return AIMessage(content=f"{last.content} {NOTE}")
        if "email" in str(last.content).lower():
            args = {"to": "ada@example.com", "subject": "Hello from LangGraph"}
            return AIMessage(content="", tool_calls=[{"id": f"call_{uuid4().hex}", "name": "send_email", "args": args}])
        return AIMessage(content=f"{NOTE} Ask me to **send an email** to see a tool wait for your approval.")

    def _generate(self, messages: list[BaseMessage], stop: Any = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._reply(messages))])

    def _stream(self, messages: list[BaseMessage], stop: Any = None, run_manager: Any = None, **kwargs: Any) -> Iterator[ChatGenerationChunk]:
        reply = self._reply(messages)
        if reply.tool_calls:
            call = reply.tool_calls[0]
            chunk = {"id": call["id"], "name": call["name"], "args": json.dumps(call["args"]), "index": 0}
            yield ChatGenerationChunk(message=AIMessageChunk(content="", tool_call_chunks=[chunk]))
            return
        words = str(reply.content).split(" ")
        for i, word in enumerate(words):
            yield ChatGenerationChunk(message=AIMessageChunk(content=word if i == 0 else f" {word}"))

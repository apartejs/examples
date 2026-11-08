"""Runs the agent with the scripted model, through the same route the page calls. CI runs this file."""

import json
from uuid import uuid4

from starlette.testclient import TestClient

from agent import app

client = TestClient(app)


def run(thread_id: str, **body) -> list[dict]:
    payload = {"threadId": thread_id, "runId": uuid4().hex, "state": {}, "messages": [], "tools": [], "context": [], "forwardedProps": {}, **body}
    response = client.post("/agent", json=payload, headers={"accept": "text/event-stream"})
    assert response.status_code == 200, response.text
    return [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]


def user(text: str) -> dict:
    return {"id": uuid4().hex, "role": "user", "content": text}


def of_type(events: list[dict], name: str) -> list[dict]:
    return [e for e in events if e["type"] == name]


events = run(uuid4().hex, messages=[user("Hello")])
assert events[0]["type"] == "RUN_STARTED" and events[-1]["type"] == "RUN_FINISHED", events
text = "".join(e["delta"] for e in of_type(events, "TEXT_MESSAGE_CONTENT"))
assert "scripted reply" in text, text
assert len(of_type(events, "TEXT_MESSAGE_CONTENT")) > 1, "the reply did not stream"

thread = uuid4().hex
ask = user("Send an email")
paused = run(thread, messages=[ask])
call = of_type(paused, "TOOL_CALL_START")[0]
assert call["toolCallName"] == "send_email", paused
args = "".join(e["delta"] for e in of_type(paused, "TOOL_CALL_ARGS"))
interrupts = paused[-1]["outcome"]["interrupts"]
assert interrupts[0]["reason"] == "tool_call" and interrupts[0]["toolCallId"] == call["toolCallId"], interrupts

# The agent keeps nothing between runs: the page sends the conversation back with its answer.
assistant = {
    "id": uuid4().hex,
    "role": "assistant",
    "toolCalls": [{"id": call["toolCallId"], "type": "function", "function": {"name": "send_email", "arguments": args}}],
}
resumed = run(
    thread,
    messages=[ask, assistant],
    resume=[{"interruptId": interrupts[0]["id"], "status": "resolved", "payload": {"approved": True}}],
)
result = of_type(resumed, "TOOL_CALL_RESULT")[0]["content"]
assert "Email sent" in result, resumed
assert of_type(resumed, "RUN_FINISHED")[-1].get("outcome", {"type": "success"})["type"] == "success", resumed

print("ok")

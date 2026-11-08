# LangGraph + aparté

A [LangGraph](https://langchain-ai.github.io/langgraph/) agent served over [AG-UI](https://docs.ag-ui.com), with [aparté](https://apartejs.dev) as its chat. Replies stream, tool calls show as they run, and one tool waits for a person before it runs.

The page knows nothing about LangGraph: `@aparte/runner-ag-ui` reads the agent's AG-UI stream.

## Run it

The agent runs in Python, so this one runs on your machine and not on StackBlitz. Tested with Python 3.13 and Node 24.

```bash
npx degit apartejs/examples/langgraph-ag-ui my-agent
cd my-agent
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn agent:app --port 8000
```

In a second terminal:

```bash
npm install
npm run dev
```

Open http://localhost:5173 and ask it to send an email.

With nothing configured, a scripted model answers, and says it is scripted. For a real model, copy `.env.example` to `.env` and set `MODEL` and `OPENAI_API_KEY`. `OPENAI_BASE_URL` points it at any OpenAI-compatible API, a local one included.

## What to look at

- [`agent.py`](./agent.py): the graph and its FastAPI route. `send_email` calls `interrupt()` with a `reason` and the call's id, which is what opens the chat's approval panel. `emit_interrupt_outcome=True` ends a paused run the way AG-UI 1.0 describes it.
- [`src/main.ts`](./src/main.ts): the whole page.
- [`scripted_model.py`](./scripted_model.py): the stand-in model.
- [`smoke_test.py`](./smoke_test.py): what CI runs against the route: a reply, a pause, and a resume.

# Pydantic AI + aparté

A [Pydantic AI](https://ai.pydantic.dev) agent served over [AG-UI](https://docs.ag-ui.com), with [aparté](https://apartejs.dev) as its chat. Replies stream, tool calls show as they run, and one tool waits for a person before it runs.

The page knows nothing about Pydantic AI: `@aparte/runner-ag-ui` reads the agent's AG-UI stream.

## Run it

The agent runs in Python, so this one runs on your machine and not on StackBlitz. Tested with Python 3.13 and Node 24.

```bash
npx degit apartejs/examples/pydantic-ai-ag-ui my-agent
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

- [`agent.py`](./agent.py): the agent and its route. `requires_approval=True` on the tool, with `DeferredToolRequests` in the agent's output, is all it takes to pause for a person. The agent keeps nothing between runs: the page sends the conversation back with its answer.
- [`src/main.ts`](./src/main.ts): the whole page.
- [`scripted_model.py`](./scripted_model.py): the stand-in model.
- [`smoke_test.py`](./smoke_test.py): what CI runs against the route: a reply, a pause, and a resume.

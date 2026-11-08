# Google ADK + aparté

A [Google ADK](https://google.github.io/adk-docs/) agent served over [AG-UI](https://docs.ag-ui.com), with [aparté](https://apartejs.dev) as its chat. Replies stream, tool calls show as they run, and one tool waits for a person before it runs.

## Run it

The agent runs in Python, so this one runs on your machine and not on StackBlitz. Tested with Python 3.13 and Node 24.

```bash
npx degit apartejs/examples/google-adk-ag-ui my-agent
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

With nothing configured, a scripted model answers, and says it is scripted. For a real model, copy `.env.example` to `.env` and set `MODEL` to a Gemini model and `GOOGLE_API_KEY` to your key.

## What to look at

- [`agent.py`](./agent.py): the agent and its FastAPI route. `require_confirmation=True` on the tool pauses the run for a person, and `emit_interrupt_outcome=True` ends that run the way AG-UI 1.0 describes it.
- [`src/main.ts`](./src/main.ts): the whole page. ADK asks for a confirmation through a tool of its own, `adk_request_confirmation`, so `registerToolDisplay` hides that row and has the question name the real tool. The rest knows nothing about ADK: `@aparte/runner-ag-ui` reads the agent's AG-UI stream.
- [`scripted_model.py`](./scripted_model.py): the stand-in model.
- [`smoke_test.py`](./smoke_test.py): what CI runs against the route: a reply, a pause, and a resume.

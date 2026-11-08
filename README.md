# aparté examples

Apps built on [aparté](https://github.com/apartejs/aparte), an MIT chat UI for AI made of Web Components. Each folder is a whole app: copy it and run it, or open it in StackBlitz when it runs there.

| Example | Stack | What it shows | Try it |
|---|---|---|---|
| [sveltekit-ai-sdk](./sveltekit-ai-sdk) | SvelteKit, Vercel AI SDK | A tool the model can only run once the user approves it, drawn by a Svelte component; Markdown formatted as it streams | [StackBlitz](https://stackblitz.com/github/apartejs/examples/tree/main/sveltekit-ai-sdk?file=src/lib/chat.ts) |
| [langgraph-ag-ui](./langgraph-ag-ui) | LangGraph, AG-UI | A Python agent streaming into the chat, and a tool that waits for a person through `interrupt()` | On your machine |
| [pydantic-ai-ag-ui](./pydantic-ai-ag-ui) | Pydantic AI, AG-UI | A Python agent streaming into the chat, and a tool that waits for a person through `requires_approval` | On your machine |
| [google-adk-ag-ui](./google-adk-ag-ui) | Google ADK, AG-UI | A Python agent streaming into the chat, a tool that waits for a person through `require_confirmation`, and ADK's confirmation tool kept off the transcript | On your machine |

## Run one on your machine

```bash
npx degit apartejs/examples/sveltekit-ai-sdk my-chat
cd my-chat
npm install
npm run dev
```

With no API key, an example answers with a scripted model, which is how it runs on StackBlitz. Each folder's `.env.example` names the key that switches it to a real model. An example with a Python agent starts that agent first: its README has the commands.

## Adding an example

- **One folder, one app.** Nothing is installed at the root, and no folder imports from another: a folder copied alone must run.
- **Name it after its stack**, framework first: `sveltekit-ai-sdk`, `nextjs-ai-sdk`. Add the topic only when two examples share a stack.
- **aparté comes from npm**, at a published version, with the lockfile committed: the example installs what a reader's app would.
- **It runs without a key.** A scripted model answers when the key is missing, and its answer says it is scripted.
- **It has `check` and `build` scripts.** CI runs `npm ci`, `npm run check` and `npm run build` in every folder that has a `package.json`, and Dependabot updates each folder's lockfile. A folder with a `requirements.txt` holds a Python agent: CI installs it and runs its `smoke_test.py`.
- **Its README says how to try it**, with a StackBlitz link when it runs there (a Python agent does not), and it gets a row in the table above.

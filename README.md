# aparté examples

Apps built on [aparté](https://github.com/apartejs/aparte), an MIT chat UI for AI made of Web Components. Each folder is a whole app: open it in StackBlitz, or copy it and run it.

| Example | Stack | What it shows | Try it |
|---|---|---|---|
| [sveltekit-ai-sdk](./sveltekit-ai-sdk) | SvelteKit, Vercel AI SDK | A tool the model can only run once the user approves it, drawn by a Svelte component; Markdown formatted as it streams | [StackBlitz](https://stackblitz.com/github/apartejs/examples/tree/main/sveltekit-ai-sdk?file=src/lib/chat.ts) |

## Run one on your machine

```bash
npx degit apartejs/examples/sveltekit-ai-sdk my-chat
cd my-chat
npm install
npm run dev
```

With no API key, an example answers with a scripted model, which is how it runs on StackBlitz. Each folder's `.env.example` names the key that switches it to a real model.

## Adding an example

- **One folder, one app.** Nothing is installed at the root, and no folder imports from another: a folder copied alone must run.
- **Name it after its stack**, framework first: `sveltekit-ai-sdk`, `nextjs-ai-sdk`. Add the topic only when two examples share a stack.
- **aparté comes from npm**, at a published version, with the lockfile committed: the example installs what a reader's app would.
- **It runs without a key.** A scripted model answers when the key is missing, and its answer says it is scripted.
- **It has `check` and `build` scripts.** CI runs `npm ci`, `npm run check` and `npm run build` in every folder that has a `package.json`, and Dependabot updates each folder's lockfile.
- **Its README opens with a StackBlitz link**, and it gets a row in the table above.

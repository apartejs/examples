# SvelteKit + Vercel AI SDK: the user approves every tool call

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/apartejs/examples/tree/main/sveltekit-ai-sdk?file=src/lib/chat.ts)

A task list you talk to. The model can call one tool, `add_task`, and the task is added only once you click **Approve**.

- `src/routes/api/chat/+server.ts`: the model call, on the server, so the API key never reaches the browser.
- `src/lib/chat.ts`: where the chat sends its requests, the Markdown renderer, and the `add_task` tool with its approval.
- `src/lib/TaskCard.svelte`: how a call to `add_task` is drawn in the conversation.
- `src/routes/+page.svelte`: the page, the chat beside the list.

## Run it

```bash
npm install
npm run dev
```

It needs Node 22.17 or later, SvelteKit's minimum.

## Without a key, a scripted model answers

With no `ANTHROPIC_API_KEY`, `src/lib/server/scripted-model.ts` answers instead of a real model. It understands nothing: it offers to add whatever you wrote as a task, and its answer says it is scripted. It is there so the approval, the tool card and the streaming Markdown can be tried anywhere, StackBlitz included.

## With a real model

```bash
cp .env.example .env
```

Put your Anthropic key in `.env` and restart `npm run dev`. Keep the key out of StackBlitz: run the app on your machine to use it.

For another provider, swap `@ai-sdk/anthropic` for its AI SDK package in `src/routes/api/chat/+server.ts`.

Built with [aparté](https://github.com/apartejs/aparte): `@aparte/svelte`, `@aparte/provider-ai-sdk` and `@aparte/plugin-marked`.

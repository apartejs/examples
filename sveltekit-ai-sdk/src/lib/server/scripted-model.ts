// Answers when no ANTHROPIC_API_KEY is set, so this example runs anywhere, StackBlitz included.
// It understands nothing: it offers to add whatever you wrote as a task, then says what happened.
import { MockLanguageModelV4, simulateReadableStream } from 'ai/test';

const usage = {
  inputTokens: { total: 0, noCache: 0, cacheRead: 0, cacheWrite: 0 },
  outputTokens: { total: 0, text: 0, reasoning: 0 },
};

const note = '\n\n_A scripted answer: put an `ANTHROPIC_API_KEY` in `.env` to talk to a real model._';

/** One text block, sent in pieces the way a model streams it. */
function text(id: string, deltas: string[]) {
  return [
    { type: 'text-start', id },
    ...deltas.map((delta) => ({ type: 'text-delta', id, delta })),
    { type: 'text-end', id },
  ];
}

/** What the user last wrote, as a task title: one line, without Markdown's table and emphasis characters. */
function lastWords(prompt: ReadonlyArray<{ role: string; content: unknown }>): string {
  const message = [...prompt].reverse().find((m) => m.role === 'user');
  const parts: Array<{ type?: string; text?: string }> = Array.isArray(message?.content) ? message.content : [];
  const words = parts
    .map((part) => (part.type === 'text' ? (part.text ?? '') : ''))
    .join(' ')
    .replace(/[\s|*_`#>]+/g, ' ')
    .trim();
  return words.slice(0, 80) || 'Something to do';
}

export const scriptedModel = new MockLanguageModelV4({
  doStream: async ({ prompt }) => {
    const title = lastWords(prompt);
    const last = prompt.at(-1);
    const chunks: unknown[] = [{ type: 'stream-start', warnings: [] }];

    if (last?.role !== 'tool') {
      chunks.push(
        ...text('ask', ['I can add that ', 'to your list.']),
        { type: 'tool-call', toolCallId: `call-${Date.now()}`, toolName: 'add_task', input: JSON.stringify({ title }) },
        { type: 'finish', finishReason: { unified: 'tool-calls', raw: undefined }, usage },
      );
    } else if (/rejected|refused/i.test(JSON.stringify(last.content))) {
      chunks.push(
        ...text('no', ['Fine, I left it ', 'off the list.', note]),
        { type: 'finish', finishReason: { unified: 'stop', raw: undefined }, usage },
      );
    } else {
      // The bold and the table arrive in pieces: they are formatted before they are complete.
      const cut = Math.ceil(title.length / 2);
      chunks.push(
        ...text('done', [
          `Done: **${title.slice(0, cut)}`,
          `${title.slice(cut)}** is on your list.\n\n`,
          '| Task | Status |\n|---|---|\n',
          `| ${title} `,
          '| To do |',
          note,
        ]),
        { type: 'finish', finishReason: { unified: 'stop', raw: undefined }, usage },
      );
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return { stream: simulateReadableStream({ chunks: chunks as any[], chunkDelayInMs: 80 }) };
  },
});

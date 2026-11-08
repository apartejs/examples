import { createAnthropic } from '@ai-sdk/anthropic';
import { streamText } from 'ai';
import type { AparteChatRequest, AparteStreamEvent } from '@aparte/core';
import { fullStreamToAparteEvents, toModelMessages, toToolChoice, toToolSet } from '@aparte/provider-ai-sdk';
import { ANTHROPIC_API_KEY } from '$app/env/private';
import { scriptedModel } from '#lib/server/scripted-model.ts';
import type { RequestHandler } from './$types';

const anthropic = createAnthropic({ apiKey: ANTHROPIC_API_KEY });

export const POST: RequestHandler = async ({ request: req }) => {
  // In a real app, check the user's session here: this route spends your key.
  const { request } = (await req.json()) as { request: AparteChatRequest };

  const result = streamText({
    // The server picks the model, not the page. No key: the scripted model answers.
    model: ANTHROPIC_API_KEY ? anthropic('claude-haiku-5-5') : scriptedModel,
    system: `You keep the user's task list. Today is ${new Date().toDateString()}.`,
    messages: toModelMessages(request.messages),
    abortSignal: req.signal,
    ...(request.tools?.length
      ? { tools: toToolSet(request.tools), toolChoice: toToolChoice(request.toolChoice) ?? 'auto' }
      : {}),
  });

  const ndjson = fullStreamToAparteEvents(result.fullStream)
    .pipeThrough(
      new TransformStream<AparteStreamEvent, string>({
        transform(event, controller) {
          if (event.type === 'error') {
            console.error('[api/chat]', event.message); // the vendor's words stay in your log
            event = { type: 'error', message: 'The model call failed.' };
          }
          controller.enqueue(JSON.stringify(event) + '\n');
        },
      }),
    )
    .pipeThrough(new TextEncoderStream());

  return new Response(ndjson, { headers: { 'content-type': 'application/x-ndjson' } });
};

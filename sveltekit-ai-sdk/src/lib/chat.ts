import { aparteGlobalConfig, AparteBackendTransport } from '@aparte/core';
import { createAiSdkProvider } from '@aparte/provider-ai-sdk';
import { setupMarkedStreamingProvider } from '@aparte/plugin-marked/streaming';
import { tasks, type Task } from './tasks.svelte.ts';

// Models answer in Markdown: format it as it streams, not after.
setupMarkedStreamingProvider();

// The page sends every request to /api/chat; the model call happens there.
aparteGlobalConfig.registerAIProvider(
  createAiSdkProvider({
    id: 'server',
    name: 'Server',
    languageModel: () => {
      throw new Error('The model runs on the server.');
    },
  }),
);
aparteGlobalConfig.setTransport(new AparteBackendTransport({ endpoint: '/api/chat' }));
aparteGlobalConfig.setModelConfig({ defaultProvider: 'server', defaultModel: 'claude-haiku-5-5' });

// A tool the model may call, but only after the user says yes.
aparteGlobalConfig.registerTool(
  {
    name: 'add_task',
    description: "Add a task to the user's list.",
    inputSchema: {
      type: 'object',
      properties: {
        title: { type: 'string' },
        due: { type: 'string', description: 'Due date, YYYY-MM-DD' },
      },
      required: ['title'],
    },
    needsApproval: true,
  },
  async (call) => {
    const task: Task = {
      title: String(call.input['title']),
      due: call.input['due'] ? String(call.input['due']) : undefined,
    };
    tasks.push(task);
    return { toolCallId: call.id, content: `Added "${task.title}".`, structuredContent: task };
  },
);

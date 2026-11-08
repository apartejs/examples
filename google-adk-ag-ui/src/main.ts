import '@aparte/core/styles.css';
import { AparteClient, aparteGlobalConfig } from '@aparte/core';
import { setupMarkedProvider } from '@aparte/plugin-marked';
import { createAgUiRunner } from '@aparte/runner-ag-ui';

setupMarkedProvider();

// ADK asks for an approval through a tool of its own, whose arguments are its protocol.
// Keep it off the transcript, and have the question name the tool it is really about.
type Confirmation = { originalFunctionCall?: { name?: string; args?: unknown } };

aparteGlobalConfig.registerToolDisplay('adk_request_confirmation', {
  hidden: true,
  label: (segment) => (segment.toolCall.input as Confirmation).originalFunctionCall?.name ?? 'this tool',
  formatInput: (input) => JSON.stringify((input as Confirmation).originalFunctionCall?.args ?? {}, null, 2),
});

// The rest of the page knows nothing about Google ADK: it reads the agent's AG-UI stream.
new AparteClient({ streamRunner: createAgUiRunner({ endpoint: '/agent' }) }).start();

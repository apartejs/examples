import '@aparte/core/styles.css';
import { AparteClient } from '@aparte/core';
import { setupMarkedProvider } from '@aparte/plugin-marked';
import { createAgUiRunner } from '@aparte/runner-ag-ui';

setupMarkedProvider();

// The page knows nothing about Pydantic AI: it reads the agent's AG-UI stream.
new AparteClient({ streamRunner: createAgUiRunner({ endpoint: '/agent' }) }).start();

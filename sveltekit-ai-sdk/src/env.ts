import { defineEnvVars } from '@sveltejs/kit/env';

export const variables = defineEnvVars({
  // Optional: without a key, a scripted model answers, so the example runs anywhere.
  ANTHROPIC_API_KEY: { schema: (value) => value || undefined },
});

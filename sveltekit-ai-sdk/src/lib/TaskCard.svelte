<script lang="ts">
  import type { AparteToolCallView } from '@aparte/svelte/runes';
  import type { Task } from './tasks.svelte.ts';

  let { tool }: { tool: AparteToolCallView } = $props();

  // The model's arguments, still arriving while the call streams.
  const task = $derived((tool.input ?? {}) as Partial<Task>);

  const labels: Record<string, string> = {
    'awaiting-approval': 'Waiting for your OK',
    resolved: 'Added',
    rejected: 'Not added',
  };
</script>

<div class="task-card" data-status={tool.status}>
  <strong>{task.title ?? '…'}</strong>
  {#if task.due}<span>due {task.due}</span>{/if}
  <em>{labels[tool.status] ?? 'Preparing…'}</em>
</div>

<style>
  .task-card {
    display: grid;
    gap: 0.25rem;
    max-width: 22rem;
    padding: 0.75rem 1rem;
    border: 1px solid var(--aparte-border);
    border-radius: 0.75rem;
    background: var(--aparte-surface-1);
  }
  span {
    color: var(--aparte-text-muted);
    font-size: 0.875rem;
  }
  em {
    font-style: normal;
    font-size: 0.8125rem;
    color: var(--aparte-accent);
  }
  [data-status='rejected'] em {
    color: var(--aparte-text-muted);
  }
</style>

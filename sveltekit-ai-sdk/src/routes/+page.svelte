<script lang="ts" module>
  import '#lib/chat.ts';
</script>

<script lang="ts">
  import { AparteChat, AparteToolUI, createAparteClient } from '@aparte/svelte/runes';
  import '@aparte/core/styles.css';
  import TaskCard from '#lib/TaskCard.svelte';
  import { tasks } from '#lib/tasks.svelte.ts';

  createAparteClient();
</script>

<AparteToolUI name="add_task">
  {#snippet children(tool)}<TaskCard {tool} />{/snippet}
</AparteToolUI>

<main>
  <section class="chat">
    <AparteChat centerWhenEmpty placeholder="What do you need to do?">
      {#snippet emptyState()}<p>Tell me what you need to do, I'll keep the list.</p>{/snippet}
    </AparteChat>
  </section>
  <aside>
    <h2>Tasks</h2>
    {#each tasks as task}
      <p>{task.title}{task.due ? ` · ${task.due}` : ''}</p>
    {:else}
      <p class="empty">Nothing yet.</p>
    {/each}
  </aside>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: var(--aparte-bg);
    color: var(--aparte-text);
  }
  main {
    display: grid;
    grid-template-columns: 1fr 16rem;
    height: 100dvh;
  }
  .chat {
    display: flex;
    min-height: 0;
  }
  .chat :global(aparte-chat) {
    flex: 1;
    min-height: 0;
  }
  aside {
    padding: 1rem;
    border-inline-start: 1px solid var(--aparte-border);
  }
  h2 {
    margin: 0 0 0.75rem;
    font-size: 1rem;
  }
  .empty {
    color: var(--aparte-text-muted);
  }
</style>

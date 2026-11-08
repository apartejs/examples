export type Task = { title: string; due?: string };

export const tasks = $state<Task[]>([]);

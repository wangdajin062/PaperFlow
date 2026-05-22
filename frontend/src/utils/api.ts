import type { Workflow, ExecutionResults } from '../types/workflow';

const API_BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API error ${res.status}: ${err}`);
  }
  return res.json();
}

export const api = {
  listWorkflows: () => request<{ workflows: Workflow[] }>('/workflows'),
  getWorkflow: (id: string) => request<Workflow>(`/workflows/${id}`),
  createWorkflow: (data: Partial<Workflow>) =>
    request<Workflow>('/workflows', { method: 'POST', body: JSON.stringify(data) }),
  updateWorkflow: (id: string, data: Partial<Workflow>) =>
    request<Workflow>(`/workflows/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  deleteWorkflow: (id: string) =>
    request<{ ok: boolean }>(`/workflows/${id}`, { method: 'DELETE' }),

  runWorkflow: (workflowId: string, providerOverrides?: Record<string, unknown>) =>
    request<ExecutionResults>('/execution/run', {
      method: 'POST',
      body: JSON.stringify({
        workflow_id: workflowId,
        provider_overrides: providerOverrides || {},
      }),
    }),
};

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
  // Workflows
  listWorkflows: () => request<any[]>('/workflows'),
  getWorkflow: (id: string) => request<any>(`/workflows/${id}`),
  createWorkflow: (data: any) =>
    request<any>('/workflows', { method: 'POST', body: JSON.stringify(data) }),
  updateWorkflow: (id: string, data: any) =>
    request<any>(`/workflows/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteWorkflow: (id: string) =>
    request<any>(`/workflows/${id}`, { method: 'DELETE' }),

  // Execution
  runWorkflow: (workflowId: string, providerOverrides?: Record<string, any>) =>
    request<any>('/execution/run', {
      method: 'POST',
      body: JSON.stringify({ workflow_id: workflowId, provider_overrides: providerOverrides || {} }),
    }),

  // Models
  listModelConfigs: () => request<any[]>('/models'),
  saveModelConfig: (data: any) =>
    request<any>('/models', { method: 'POST', body: JSON.stringify(data) }),
};

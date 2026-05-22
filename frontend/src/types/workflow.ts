export interface WorkflowNode {
  id: string;
  type: 'prompt' | 'code' | 'output' | 'start';
  position: { x: number; y: number };
  data: Record<string, unknown>;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string | null;
  targetHandle?: string | null;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  created_at?: string;
  updated_at?: string;
}

export interface ModelConfig {
  id: string;
  provider: 'claude' | 'openai' | 'gemini' | 'deepseek';
  api_key: string;
  model_name: string;
  is_active: number;
}

export interface ExecutionResults {
  workflow_id: string;
  results: Record<string, string>;
}

export type NodeType = 'prompt' | 'code' | 'output' | 'start';

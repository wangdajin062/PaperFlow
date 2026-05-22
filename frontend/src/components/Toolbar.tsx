import { useState, useCallback } from 'react';
import { api } from '../utils/api';
import { __getWorkflowData, __setWorkflowNodes, __setWorkflowEdges } from './WorkflowEditor';
import { UIUXDesignWorkflow } from '../templates/uiux-workflow';
import type { WorkflowNode } from '../types/workflow';

interface ToolbarProps {
  workflowId: string | null;
  onWorkflowSaved: (id: string) => void;
}

export default function Toolbar({ workflowId, onWorkflowSaved }: ToolbarProps) {
  const [name, setName] = useState('');
  const [saving, setSaving] = useState(false);
  const [running, setRunning] = useState(false);
  const [saved, setSaved] = useState(false);

  // Auto-clear saved indicator after 2s
  const flashSaved = useCallback(() => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }, []);

  const handleSave = async () => {
    const data = __getWorkflowData();
    if (!data) return;

    setSaving(true);
    try {
      const payload = {
        name: name || 'Untitled Workflow',
        nodes: data.nodes as WorkflowNode[],
        edges: data.edges,
      };

      if (workflowId) {
        await api.updateWorkflow(workflowId, payload);
      } else {
        const result = await api.createWorkflow(payload);
        onWorkflowSaved(result.id);
      }
      flashSaved();
    } catch (err) {
      console.error('Save failed', err); // eslint-disable-line no-console
    } finally {
      setSaving(false);
    }
  };

  const handleRun = async () => {
    if (!workflowId) return;

    setRunning(true);
    try {
      await api.runWorkflow(workflowId);
    } catch (err) {
      console.error('Run failed', err); // eslint-disable-line no-console
    } finally {
      setRunning(false);
    }
  };

  const handleLoadTemplate = () => {
    const { nodes, edges } = UIUXDesignWorkflow;
    __setWorkflowNodes([...nodes]);
    __setWorkflowEdges([...edges]);
  };

  return (
    <div className="toolbar">
      <div className="toolbar-left">
        <input
          className="workflow-title-input"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Untitled Workflow"
        />
        {saving && <span className="save-indicator saving">Saving...</span>}
        {saved && <span className="save-indicator saved">Saved</span>}
      </div>
      <div className="toolbar-right">
        <button
          className="toolbar-btn"
          onClick={handleLoadTemplate}
          title="Load workflow template"
        >
          模板
        </button>
        <button
          className="toolbar-btn primary"
          onClick={handleSave}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save'}
        </button>
        <button
          className="toolbar-btn primary"
          onClick={handleRun}
          disabled={running || !workflowId}
        >
          {running ? 'Running...' : 'Run'}
        </button>
      </div>
    </div>
  );
}

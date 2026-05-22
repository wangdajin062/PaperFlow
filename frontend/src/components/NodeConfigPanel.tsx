import { useState, useEffect, useCallback } from 'react';
import ModelSelector from './ModelSelector';
import { __getWorkflowData, __setWorkflowNodes } from './WorkflowEditor';

interface NodeConfigPanelProps {
  nodeId: string;
  onChatMessage: (msg: { role: string; content: string }) => void;
}

const NODE_LABELS: Record<string, string> = {
  prompt: 'Prompt 节点',
  code: 'Code 节点',
  output: 'Output 节点',
  start: 'Start 节点',
};

export default function NodeConfigPanel({ nodeId, onChatMessage }: NodeConfigPanelProps) {
  const [nodeType, setNodeType] = useState<string>('');
  const [localData, setLocalData] = useState<Record<string, any>>({});

  // Load node data from workflow state when nodeId changes
  useEffect(() => {
    const wf = __getWorkflowData();
    if (!wf) return;
    const node = wf.nodes.find((n) => n.id === nodeId);
    if (node) {
      setNodeType(node.type || '');
      setLocalData({ ...node.data });
    }
  }, [nodeId]);

  // Sync a single field to workflow node data
  const syncField = useCallback(
    (key: string, value: any) => {
      setLocalData((prev) => ({ ...prev, [key]: value }));

      const wf = __getWorkflowData();
      if (!wf) return;
      const updated = wf.nodes.map((n) =>
        n.id === nodeId ? { ...n, data: { ...n.data, [key]: value } } : n,
      );
      __setWorkflowNodes(updated);
    },
    [nodeId],
  );

  // Handle ModelSelector change
  const handleModelChange = useCallback(
    (provider: string, modelName: string) => {
      syncField('provider', provider);
      syncField('model', modelName);
    },
    [syncField],
  );

  // Open file in VS Code (requires backend API endpoint from Task 11)
  const handleOpenInVSCode = useCallback(async () => {
    const filePath = localData.file_path;
    if (!filePath) return;
    try {
      const res = await fetch('/api/vscode/open', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath }),
      });
      const data = await res.json();
      if (data.success) {
        onChatMessage({ role: 'assistant', content: `已在 VS Code 中打开: ${filePath}` });
      } else {
        onChatMessage({ role: 'assistant', content: `打开失败: ${data.error || '未知错误'}` });
      }
    } catch {
      onChatMessage({ role: 'assistant', content: 'VS Code API 不可用（Task 11 后将支持）' });
    }
  }, [localData.file_path, onChatMessage]);

  if (!nodeType) {
    return (
      <>
        <div className="panel-header">节点配置</div>
        <div className="panel-content">
          <div className="config-section">
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 20px', fontSize: 13 }}>
              未找到节点
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="panel-header">
        <span>{NODE_LABELS[nodeType] || '节点配置'}</span>
      </div>
      <div className="panel-content">
        {/* ========== Prompt Node ========== */}
        {nodeType === 'prompt' && (
          <div className="config-section">
            <div className="config-section-title">提示词配置</div>

            <div className="config-field">
              <label className="config-label">系统提示词</label>
              <textarea
                className="config-textarea"
                value={localData.system_prompt || ''}
                onChange={(e) => syncField('system_prompt', e.target.value)}
                placeholder="系统角色设定、行为约束等..."
                rows={3}
              />
            </div>

            <div className="config-field">
              <label className="config-label">提示词模板</label>
              <textarea
                className="config-textarea"
                value={localData.prompt || ''}
                onChange={(e) => syncField('prompt', e.target.value)}
                placeholder="输入提示词内容，可使用 {{变量}} 模板语法..."
                rows={4}
              />
            </div>

            <div className="config-section-title" style={{ marginTop: 16 }}>模型配置</div>

            <div className="config-field">
              <ModelSelector
                provider={localData.provider || ''}
                modelName={localData.model || ''}
                onChange={handleModelChange}
              />
            </div>

            <div className="config-field">
              <label className="config-label">API Key</label>
              <input
                className="config-input"
                type="password"
                value={localData.api_key || ''}
                onChange={(e) => syncField('api_key', e.target.value)}
                placeholder="输入 API Key..."
              />
            </div>
          </div>
        )}

        {/* ========== Code Node ========== */}
        {nodeType === 'code' && (
          <div className="config-section">
            <div className="config-section-title">代码任务配置</div>

            <div className="config-field">
              <label className="config-label">任务描述</label>
              <textarea
                className="config-textarea"
                value={localData.description || ''}
                onChange={(e) => syncField('description', e.target.value)}
                placeholder="描述该代码节点的功能..."
                rows={3}
              />
            </div>

            <div className="config-field">
              <label className="config-label">文件路径</label>
              <input
                className="config-input"
                type="text"
                value={localData.file_path || ''}
                onChange={(e) => syncField('file_path', e.target.value)}
                placeholder="如: output/analysis.py"
              />
            </div>

            <button
              style={{
                width: '100%',
                padding: '8px 0',
                borderRadius: 6,
                border: '1px solid var(--border-color)',
                background: 'var(--bg-tertiary)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                fontSize: 13,
                marginTop: 8,
              }}
              onClick={handleOpenInVSCode}
              disabled={!localData.file_path}
            >
              在 VS Code 中打开
            </button>
          </div>
        )}

        {/* ========== Output Node ========== */}
        {nodeType === 'output' && (
          <div className="config-section">
            <div className="config-section-title">输出节点</div>
            <div
              style={{
                background: 'var(--bg-tertiary)',
                borderRadius: 8,
                padding: 16,
                fontSize: 13,
                lineHeight: 1.6,
                color: 'var(--text-secondary)',
              }}
            >
              <p style={{ marginBottom: 8 }}>
                该节点将收集所有上游节点的输出结果。
              </p>
              <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                工作流执行完成后，此处会显示最终输出内容。
              </p>
            </div>
            {localData.output && (
              <div style={{ marginTop: 12 }}>
                <label className="config-label">输出内容</label>
                <div
                  style={{
                    background: 'var(--bg-tertiary)',
                    borderRadius: 6,
                    padding: 12,
                    fontSize: 12,
                    fontFamily: 'var(--font-mono)',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    maxHeight: 300,
                    overflow: 'auto',
                    color: 'var(--text-primary)',
                    border: '1px solid var(--border-light)',
                  }}
                >
                  {localData.output}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========== Start Node ========== */}
        {nodeType === 'start' && (
          <div className="config-section">
            <div className="config-section-title">开始节点</div>
            <div
              style={{
                background: 'var(--bg-tertiary)',
                borderRadius: 8,
                padding: 16,
                fontSize: 13,
                lineHeight: 1.6,
                color: 'var(--text-secondary)',
              }}
            >
              <p style={{ marginBottom: 8 }}>
                该节点是工作流的起点。
              </p>
              <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                所有工作流都从一个开始节点出发。连接其他节点以构建您的工作流。
              </p>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

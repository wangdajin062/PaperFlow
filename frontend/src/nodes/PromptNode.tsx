import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function PromptNode({ data, selected }: NodeProps) {
  return (
    <div className={`prompt-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>Prompt</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.prompt ? data.prompt.substring(0, 60) + (data.prompt.length > 60 ? '...' : '') : '点击配置提示词'}
      </div>
      {data.provider && (
        <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>
          Model: {data.provider}/{data.model || 'default'}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(PromptNode);

import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function CodeNode({ data, selected }: NodeProps) {
  return (
    <div className={`code-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>Code</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.description || '点击配置代码任务'}
      </div>
      {data.file_path && (
        <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>
          File: {data.file_path.split('\\').pop()}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(CodeNode);

import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function OutputNode({ data, selected }: NodeProps) {
  return (
    <div className={`output-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>Output</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.output ? data.output.substring(0, 80) + '...' : '等待执行...'}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(OutputNode);

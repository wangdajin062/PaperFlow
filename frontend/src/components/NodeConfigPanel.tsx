interface NodeConfigPanelProps {
  nodeId: string;
  onChatMessage: (msg: { role: string; content: string }) => void;
}

export default function NodeConfigPanel({ nodeId, onChatMessage }: NodeConfigPanelProps) {
  return (
    <div className="panel">
      <div className="panel-header">Node Config</div>
      <div className="panel-content" />
    </div>
  );
}

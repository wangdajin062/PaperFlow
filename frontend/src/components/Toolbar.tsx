interface ToolbarProps {
  workflowId: string | null;
  onWorkflowSaved: (id: string) => void;
}

export default function Toolbar({ workflowId, onWorkflowSaved }: ToolbarProps) {
  return (
    <div className="toolbar">
      <div className="toolbar-left">
        <span>Toolbar</span>
      </div>
      <div className="toolbar-right" />
    </div>
  );
}

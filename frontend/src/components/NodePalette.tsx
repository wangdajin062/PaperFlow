export default function NodePalette() {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="node-palette">
      <div className="node-palette-title">Nodes</div>

      <div
        className="palette-item"
        draggable
        onDragStart={(e) => onDragStart(e, 'prompt')}
      >
        <div className="palette-item-icon prompt">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
          </svg>
        </div>
        <div>
          <div className="palette-item-label">Prompt</div>
          <div className="palette-item-desc">LLM prompt node</div>
        </div>
      </div>

      <div
        className="palette-item"
        draggable
        onDragStart={(e) => onDragStart(e, 'code')}
      >
        <div className="palette-item-icon code">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="16 18 22 12 16 6" />
            <polyline points="8 6 2 12 8 18" />
          </svg>
        </div>
        <div>
          <div className="palette-item-label">Code / VS Code</div>
          <div className="palette-item-desc">Execute code or open in VS Code</div>
        </div>
      </div>

      <div
        className="palette-item"
        draggable
        onDragStart={(e) => onDragStart(e, 'output')}
      >
        <div className="palette-item-icon output">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
        </div>
        <div>
          <div className="palette-item-label">Output</div>
          <div className="palette-item-desc">View workflow output</div>
        </div>
      </div>
    </div>
  );
}

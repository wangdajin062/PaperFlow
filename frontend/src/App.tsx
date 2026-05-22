import { useState } from 'react';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import Toolbar from './components/Toolbar';
import NodePalette from './components/NodePalette';
import WorkflowEditor from './components/WorkflowEditor';
import ChatPanel from './components/ChatPanel';
import NodeConfigPanel from './components/NodeConfigPanel';
import ReferencePanel from './components/ReferencePanel';

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<{ role: string; content: string }[]>([]);
  const [showReferences, setShowReferences] = useState(false);

  const handleNodeSelect = (nodeId: string) => {
    setSelectedNodeId(nodeId);
    setShowReferences(false);
  };

  return (
    <div className="app-layout">
      {/* Left sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">PaperFlow</div>
        <NodePalette />
        <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', padding: '8px 12px' }}>
          <button
            onClick={() => {
              setShowReferences(true);
              setSelectedNodeId(null);
            }}
            style={{
              width: '100%',
              padding: '8px 12px',
              borderRadius: 6,
              border: 'none',
              background: showReferences ? 'var(--accent-bg)' : 'transparent',
              color: showReferences ? 'var(--accent)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontSize: 13,
              display: 'flex',
              alignItems: 'center',
              gap: 8,
            }}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 19.5A2.5 2.5 0 016.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
            </svg>
            文献管理
          </button>
        </div>
      </div>

      {/* Center canvas */}
      <div className="main-area">
        <Toolbar
          workflowId={workflowId}
          onWorkflowSaved={(id) => setWorkflowId(id)}
        />
        <div className="canvas-area">
          <ReactFlowProvider>
            <WorkflowEditor
              onNodeSelect={handleNodeSelect}
            />
          </ReactFlowProvider>
        </div>
      </div>

      {/* Right panel */}
      <div className="panel">
        {selectedNodeId ? (
          <NodeConfigPanel
            nodeId={selectedNodeId}
            onChatMessage={(msg) => setChatMessages((prev) => [...prev, msg])}
          />
        ) : showReferences ? (
          <ReferencePanel />
        ) : (
          <ChatPanel messages={chatMessages} />
        )}
      </div>
    </div>
  );
}

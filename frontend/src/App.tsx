import { useState, useCallback } from 'react';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import Toolbar from './components/Toolbar';
import NodePalette from './components/NodePalette';
import WorkflowEditor from './components/WorkflowEditor';
import ChatPanel from './components/ChatPanel';
import NodeConfigPanel from './components/NodeConfigPanel';

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<{ role: string; content: string }[]>([]);

  return (
    <div className="app-layout">
      {/* Left sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">PaperFlow</div>
        <NodePalette />
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
              onNodeSelect={(nodeId) => setSelectedNodeId(nodeId)}
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
        ) : (
          <ChatPanel messages={chatMessages} />
        )}
      </div>
    </div>
  );
}

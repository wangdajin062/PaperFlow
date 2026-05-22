import { useCallback, useRef } from 'react';
import ReactFlow, {
  useNodesState,
  useEdgesState,
  addEdge,
  MiniMap,
  Controls,
  Background,
  BackgroundVariant,
  Node,
  Edge,
  Connection,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { nodeTypes } from './nodeTypes';

// Module-level accessors for Toolbar/Template access (Tasks 8, 12)
let _getWorkflowData: (() => { nodes: Node[]; edges: Edge[] }) | null = null;
let _setWorkflowNodes: ((nodes: Node[]) => void) | null = null;
let _setWorkflowEdges: ((edges: Edge[]) => void) | null = null;

export const __getWorkflowData = () => _getWorkflowData?.();
export const __setWorkflowNodes = (nodes: Node[]) => _setWorkflowNodes?.(nodes);
export const __setWorkflowEdges = (edges: Edge[]) => _setWorkflowEdges?.(edges);

const initialNodes: Node[] = [
  {
    id: 'start',
    type: 'start',
    position: { x: 250, y: 25 },
    data: { label: 'Start', prompt: 'Start' },
  },
];

interface WorkflowEditorProps {
  onNodeSelect: (nodeId: string) => void;
}

function WorkflowEditorInner({ onNodeSelect }: WorkflowEditorProps) {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowInstance = useReactFlow();

  const getWorkflowData = useCallback(() => ({ nodes, edges }), [nodes, edges]);

  // Store accessors in module-level variables
  _getWorkflowData = getWorkflowData;
  _setWorkflowNodes = setNodes;
  _setWorkflowEdges = setEdges;

  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) => addEdge(connection, eds));
    },
    [setEdges],
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');
      if (!type || !type.trim()) return;

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: Node = {
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: {},
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [reactFlowInstance, setNodes],
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      onNodeSelect(node.id);
    },
    [onNodeSelect],
  );

  const onPaneClick = useCallback(() => {
    onNodeSelect('');
  }, [onNodeSelect]);

  return (
    <div ref={reactFlowWrapper} style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        fitView
        deleteKeyCode="Delete"
        multiSelectionKeyCode="Shift"
      >
        <Controls />
        <MiniMap
          nodeColor={(n) => {
            switch (n.type) {
              case 'prompt':
              case 'start':
                return '#4c9af5';
              case 'code':
                return '#2ecc71';
              case 'output':
                return '#f39c12';
              default:
                return '#5c5f66';
            }
          }}
        />
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
      </ReactFlow>
    </div>
  );
}

export default function WorkflowEditor(props: WorkflowEditorProps) {
  return <WorkflowEditorInner {...props} />;
}

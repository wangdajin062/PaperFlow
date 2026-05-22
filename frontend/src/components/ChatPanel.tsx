interface ChatMessage {
  role: string;
  content: string;
}

interface ChatPanelProps {
  messages: ChatMessage[];
}

export default function ChatPanel({ messages }: ChatPanelProps) {
  return (
    <div className="panel">
      <div className="panel-header">Chat</div>
      <div className="panel-content" />
    </div>
  );
}

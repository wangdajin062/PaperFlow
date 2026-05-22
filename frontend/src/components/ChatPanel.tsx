import { useEffect, useRef, useState } from 'react';

interface ChatMessage {
  role: string;
  content: string;
}

interface ChatPanelProps {
  messages: ChatMessage[];
  onSend?: (message: string) => void;
}

export default function ChatPanel({ messages, onSend }: ChatPanelProps) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (input.trim() && onSend) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <div className="panel-header">
        <span>对话</span>
        {messages.length > 0 && (
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
            {messages.length} 条消息
          </span>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div
            style={{
              textAlign: 'center',
              color: 'var(--text-muted)',
              padding: '40px 20px',
              fontSize: 13,
              lineHeight: 1.8,
            }}
          >
            暂无消息
            <br />
            <span style={{ fontSize: 12 }}>选择一个节点开始配置或运行工作流</span>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.role}`}>
              {msg.content}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {onSend && (
        <div className="chat-input-area">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入消息..."
            rows={1}
          />
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={!input.trim()}
            title="发送"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
              <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" />
            </svg>
          </button>
        </div>
      )}
    </>
  );
}

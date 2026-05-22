import { useState, useEffect } from 'react';
import { api } from '../utils/api';

const PROVIDERS = [
  { value: 'claude', label: 'Claude (Anthropic)' },
  { value: 'openai', label: 'GPT (OpenAI)' },
  { value: 'gemini', label: 'Gemini (Google)' },
  { value: 'deepseek', label: 'DeepSeek' },
];

interface Props {
  provider: string;
  modelName: string;
  onChange: (provider: string, modelName: string) => void;
}

export default function ModelSelector({ provider, modelName, onChange }: Props) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <label style={{ fontSize: 12, fontWeight: 600, color: '#555' }}>模型</label>
      <select
        value={provider}
        onChange={(e) => onChange(e.target.value, modelName)}
        style={selectStyle}
      >
        <option value="">-- 选择模型 --</option>
        {PROVIDERS.map((p) => (
          <option key={p.value} value={p.value}>{p.label}</option>
        ))}
      </select>
      {provider && (
        <input
          type="text"
          placeholder="模型名称（留空用默认）"
          value={modelName}
          onChange={(e) => onChange(provider, e.target.value)}
          style={inputStyle}
        />
      )}
    </div>
  );
}

const selectStyle: React.CSSProperties = {
  padding: '6px 8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
};

const inputStyle: React.CSSProperties = {
  padding: '6px 8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
};

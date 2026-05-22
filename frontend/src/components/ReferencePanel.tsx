import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from '../utils/api';

interface Reference {
  id: string;
  title: string;
  authors: string[];
  year: string;
  journal: string;
  doi: string;
  ref_type: string;
}

export default function ReferencePanel() {
  const [refs, setRefs] = useState<Reference[]>([]);
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadRefs = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.listReferences();
      setRefs(data.references as unknown as Reference[]);
      setError('');
    } catch (err) {
      setError('加载文献失败: ' + (err instanceof Error ? err.message : String(err)));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRefs();
  }, [loadRefs]);

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImporting(true);
    setError('');
    try {
      await api.importReference(file);
      await loadRefs();
    } catch (err) {
      setError('导入失败: ' + (err instanceof Error ? err.message : String(err)));
    } finally {
      setImporting(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deleteReference(id);
      setRefs((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      setError('删除失败: ' + (err instanceof Error ? err.message : String(err)));
    }
  };

  const handleClearAll = async () => {
    try {
      await api.deleteAllReferences();
      setRefs([]);
    } catch (err) {
      setError('清空失败: ' + (err instanceof Error ? err.message : String(err)));
    }
  };

  const authorSummary = (authors: string[] | undefined) => {
    if (!authors || authors.length === 0) return '';
    if (authors.length <= 2) return authors.join(', ');
    return authors[0] + ' et al.';
  };

  return (
    <>
      <div className="panel-header">
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M4 19.5A2.5 2.5 0 016.5 17H20" />
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
          </svg>
          文献管理
        </span>
        <div style={{ display: 'flex', gap: 6 }}>
          <button
            className="toolbar-btn"
            onClick={() => fileInputRef.current?.click()}
            disabled={importing}
            style={{ padding: '4px 10px', fontSize: 12 }}
          >
            {importing ? '导入中...' : '导入'}
          </button>
          <button
            className="toolbar-btn"
            onClick={handleClearAll}
            disabled={refs.length === 0}
            style={{ padding: '4px 10px', fontSize: 12 }}
          >
            清空
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".ris,.bib"
            style={{ display: 'none' }}
            onChange={handleImport}
          />
        </div>
      </div>
      <div className="panel-content">
        {error && (
          <div style={{ padding: '8px 12px', margin: '0 12px', background: 'var(--danger)', borderRadius: 6, fontSize: 12, color: '#fff', marginTop: 8 }}>
            {error}
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 20px', fontSize: 13 }}>
            加载中...
          </div>
        ) : refs.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 20px', fontSize: 13 }}>
            <div style={{ fontSize: 32, marginBottom: 12, opacity: 0.3 }}>📄</div>
            <p>暂无文献</p>
            <p style={{ fontSize: 12, marginTop: 8 }}>
              点击「导入」按钮上传 .ris 或 .bib 文件
            </p>
          </div>
        ) : (
          <div style={{ padding: '0 12px' }}>
            <div style={{ fontSize: 11, color: 'var(--text-muted)', padding: '8px 0', borderBottom: '1px solid var(--border-color)' }}>
              共 {refs.length} 条文献
            </div>
            {refs.map((ref) => (
              <div
                key={ref.id}
                style={{
                  padding: '10px 0',
                  borderBottom: '1px solid var(--border-light)',
                  fontSize: 13,
                }}
              >
                <div style={{ fontWeight: 600, marginBottom: 2, lineHeight: 1.4, color: 'var(--text-primary)' }}>
                  {ref.title || '(无标题)'}
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 4 }}>
                  {authorSummary(ref.authors)}
                  {ref.year && <span> · {ref.year}</span>}
                  {ref.journal && <span> · {ref.journal}</span>}
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  {ref.doi && (
                    <span style={{ fontSize: 11, color: 'var(--accent)' }}>
                      DOI: {ref.doi}
                    </span>
                  )}
                  <button
                    onClick={() => handleDelete(ref.id)}
                    style={{
                      fontSize: 11,
                      color: 'var(--danger)',
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      padding: 0,
                      marginLeft: 'auto',
                    }}
                  >
                    删除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        <div
          style={{
            margin: '12px',
            padding: '12px',
            background: 'var(--bg-tertiary)',
            borderRadius: 8,
            fontSize: 12,
            lineHeight: 1.6,
            color: 'var(--text-secondary)',
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: 4, color: 'var(--text-primary)' }}>💡 使用提示</div>
          <p>在 Prompt 节点的提示词中使用 <code style={{ background: 'var(--bg-surface)', padding: '1px 4px', borderRadius: 3, fontSize: 11 }}>{'{{references}}'}</code> 来引用已导入的文献。</p>
          <p style={{ marginTop: 4 }}>支持的格式: <strong>.ris</strong> (EndNote, Zotero) 和 <strong>.bib</strong> (BibTeX)</p>
        </div>
      </div>
    </>
  );
}

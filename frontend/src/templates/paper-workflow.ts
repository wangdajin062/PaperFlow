import { Node, Edge } from 'reactflow';

export const PaperWritingWorkflow: { nodes: Node[]; edges: Edge[]; name?: string } = {
  name: '科研论文写作工作流',
  nodes: [
    {
      id: 'start',
      type: 'start',
      position: { x: 400, y: 0 },
      data: { label: 'Start', prompt: '开始论文写作' },
    },
    {
      id: 'lit-review',
      type: 'prompt',
      position: { x: 200, y: 150 },
      data: {
        label: 'Literature Review',
        prompt: '请帮我总结以下论文的核心贡献和方法论：\n\n{{start}}\n\n要求：\n1. 每篇论文用3句话总结\n2. 指出共同点和差异\n3. 识别研究空白',
        system_prompt: '你是一个顶级的科研助手，擅长文献综述。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'outline',
      type: 'prompt',
      position: { x: 600, y: 150 },
      data: {
        label: 'Outline',
        prompt: '基于以下文献综述结果，请为研究论文设计一个详细的提纲：\n\n{{lit-review}}\n\n论文主题：请根据上下文推断\n\n提纲要求：\n1. 包含Introduction, Method, Experiments, Results, Discussion, Conclusion\n2. 每个部分列出3-5个子要点\n3. 标注每个部分预期使用的模型和方法',
        system_prompt: '你是一个顶级的科研写作助手，擅长论文结构设计。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'code-exp',
      type: 'code',
      position: { x: 200, y: 320 },
      data: {
        label: 'Experiments Code',
        description: '根据论文提纲实现实验代码',
        file_path: 'C:\\Users\\wangd\\projects\\paper\\experiments\\main.py',
      },
    },
    {
      id: 'method-writing',
      type: 'prompt',
      position: { x: 600, y: 320 },
      data: {
        label: 'Method Section',
        prompt: '请根据以下提纲和实验代码，撰写论文的 Method 部分：\n\n提纲：\n{{outline}}\n\n代码：\n{{code-exp}}\n\n要求：\n1. 详细描述方法设计\n2. 包含公式和算法描述（LaTeX格式）\n3. 说明实验设置和参数',
        system_prompt: '你是一个顶级的科研论文写作助手，擅长方法部分写作。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'results-writing',
      type: 'prompt',
      position: { x: 400, y: 480 },
      data: {
        label: 'Results & Discussion',
        prompt: '请根据以下方法描述和实验结果，撰写论文的Results与Discussion部分：\n\n方法：\n{{method-writing}}\n\n要求：\n1. 客观呈现实验结果\n2. 分析和解释发现\n3. 与现有工作进行对比\n4. 指出局限性和未来方向',
        system_prompt: '你是一个顶级的科研论文写作助手。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'review',
      type: 'prompt',
      position: { x: 600, y: 620 },
      data: {
        label: 'Review & Polish',
        prompt: '请对以下论文草稿进行全面审阅和润色：\n\nIntroduction: 请根据已有内容撰写\nRelated Work: {{lit-review}}\nMethod: {{method-writing}}\nResults: {{results-writing}}\n\n审阅要求：\n1. 检查逻辑连贯性\n2. 优化学术表达\n3. 确保各部分风格一致\n4. 检查LaTeX公式正确性',
        system_prompt: '你是一个顶级的论文审稿助手，擅长学术写作润色。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'abstract-title',
      type: 'prompt',
      position: { x: 400, y: 760 },
      data: {
        label: 'Abstract & Title',
        prompt: '基于以下完整的论文内容，请生成标题和摘要：\n\n论文全文：\n{{review}}\n\n要求：\n1. 提供3个候选标题\n2. 摘要控制在200-300字\n3. 包含：背景、问题、方法、结果、结论',
        system_prompt: '你是一个顶级的科研写作助手。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'final-output',
      type: 'output',
      position: { x: 400, y: 900 },
      data: { label: 'Final Output', format: 'markdown' },
    },
  ],
  edges: [
    { id: 'e-start-lit', source: 'start', target: 'lit-review' },
    { id: 'e-lit-outline', source: 'lit-review', target: 'outline' },
    { id: 'e-outline-code', source: 'outline', target: 'code-exp' },
    { id: 'e-outline-method', source: 'outline', target: 'method-writing' },
    { id: 'e-code-method', source: 'code-exp', target: 'method-writing' },
    { id: 'e-method-results', source: 'method-writing', target: 'results-writing' },
    { id: 'e-results-review', source: 'results-writing', target: 'review' },
    { id: 'e-lit-review', source: 'lit-review', target: 'review' },
    { id: 'e-method-review', source: 'method-writing', target: 'review' },
    { id: 'e-review-abstract', source: 'review', target: 'abstract-title' },
    { id: 'e-abstract-output', source: 'abstract-title', target: 'final-output' },
  ],
};

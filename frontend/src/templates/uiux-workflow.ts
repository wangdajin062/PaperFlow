import { Node, Edge } from 'reactflow';

export const UIUXDesignWorkflow: { nodes: Node[]; edges: Edge[]; name?: string } = {
  name: 'UI/UX 可视化设计工作流',
  nodes: [
    {
      id: 'start',
      type: 'start',
      position: { x: 400, y: 0 },
      data: { label: 'Start', prompt: '开始 UI/UX 设计流程' },
    },
    {
      id: 'requirement',
      type: 'prompt',
      position: { x: 400, y: 140 },
      data: {
        label: '需求分析',
        prompt:
          '请根据以下产品信息，进行需求分析：\n\n{{start}}\n\n请输出以下内容：\n' +
          '1. 产品定位与目标用户\n' +
          '2. 核心功能列表（按优先级排列）\n' +
          '3. 关键业务目标与成功指标\n' +
          '4. 竞品分析要点\n' +
          '5. 约束条件与技术限制',
        system_prompt:
          '你是一个资深的 UX 产品经理，擅长从零到一梳理产品需求。请用中文以结构化 Markdown 格式输出。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'personas',
      type: 'prompt',
      position: { x: 400, y: 300 },
      data: {
        label: '用户画像',
        prompt:
          '基于以下需求分析结果，创建详细的用户画像：\n\n{{requirement}}\n\n' +
          '请为每个画像包含：\n' +
          '1. 姓名、年龄、职业等基本信息\n' +
          '2. 用户目标与动机\n' +
          '3. 痛点和需求\n' +
          '4. 使用场景描述\n' +
          '5. 技术熟练度\n\n共生成 2-3 个典型用户画像。',
        system_prompt:
          '你是一个 UX 研究员，擅长用户研究和人物建模。请用中文以卡片式 Markdown 格式输出。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'info-arch',
      type: 'prompt',
      position: { x: 400, y: 460 },
      data: {
        label: '信息架构',
        prompt:
          '基于以下用户画像，设计产品信息架构：\n\n{{personas}}\n\n' +
          '请输出：\n' +
          '1. 站点地图（Sitemap）- 用缩进列表表示层级结构\n' +
          '2. 主要页面与功能对应关系表\n' +
          '3. 用户核心操作流程（2-3 个关键任务流）\n' +
          '4. 导航方案（顶部导航、侧边栏、标签页等）',
        system_prompt:
          '你是一个信息架构师，擅长设计清晰易用的产品结构。请用中文以 Markdown 格式输出。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'ui-spec',
      type: 'prompt',
      position: { x: 400, y: 620 },
      data: {
        label: 'UI 设计规范',
        prompt:
          '基于以下信息架构，制定详细的 UI 设计规范：\n\n{{info-arch}}\n\n' +
          '请输出：\n' +
          '1. 色彩体系：主色、辅色、中性色、语义色，附 Hex 值\n' +
          '2. 字体排版：标题/正文/小字的字号、字重、行高\n' +
          '3. 间距体系：基础间距单位和常用间距值\n' +
          '4. 圆角与阴影规范\n' +
          '5. 核心组件风格描述：按钮、输入框、卡片、导航等\n' +
          '6. 暗色模式配色调整方案',
        system_prompt:
          '你是一个资深 UI 设计师，擅长设计系统和视觉规范制定。请用中文以结构化 Markdown+表格格式输出。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'component-code',
      type: 'code',
      position: { x: 150, y: 780 },
      data: {
        label: '组件代码生成',
        description:
          '根据 UI 设计规范，生成核心组件的 HTML/CSS 代码',
        file_path: 'uiux/components.html',
      },
    },
    {
      id: 'page-prototype',
      type: 'code',
      position: { x: 650, y: 780 },
      data: {
        label: '页面原型生成',
        description:
          '生成完整的可交互 HTML 页面原型，内联 CSS，浏览器可直接打开',
        file_path: 'uiux/prototype.html',
      },
    },
    {
      id: 'usability-test',
      type: 'prompt',
      position: { x: 400, y: 940 },
      data: {
        label: '可用性测试方案',
        prompt:
          '基于以下设计产出，设计可用性测试方案：\n\n' +
          '设计规范：\n{{ui-spec}}\n\n页面原型说明：\n{{page-prototype}}\n\n' +
          '请输出：\n' +
          '1. 测试目标与范围\n' +
          '2. 招募条件（筛选 5-8 名参与者）\n' +
          '3. 测试任务（3-5 个关键任务，让用户操作）\n' +
          '4. 评价指标：任务完成率、时间、错误率、SUS 评分\n' +
          '5. 测试脚本大纲',
        system_prompt:
          '你是一个可用性专家，擅长设计用户测试方案。请用中文以 Markdown 格式输出。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'final-output',
      type: 'output',
      position: { x: 400, y: 1100 },
      data: { label: '最终设计交付物', format: 'markdown' },
    },
  ],
  edges: [
    { id: 'e-start-req', source: 'start', target: 'requirement' },
    { id: 'e-req-personas', source: 'requirement', target: 'personas' },
    { id: 'e-personas-arch', source: 'personas', target: 'info-arch' },
    { id: 'e-arch-spec', source: 'info-arch', target: 'ui-spec' },
    { id: 'e-spec-component', source: 'ui-spec', target: 'component-code' },
    { id: 'e-spec-page', source: 'ui-spec', target: 'page-prototype' },
    { id: 'e-component-page', source: 'component-code', target: 'page-prototype' },
    { id: 'e-page-test', source: 'page-prototype', target: 'usability-test' },
    { id: 'e-spec-test', source: 'ui-spec', target: 'usability-test' },
    { id: 'e-test-output', source: 'usability-test', target: 'final-output' },
  ],
};

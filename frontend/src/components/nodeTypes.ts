import PromptNode from '../nodes/PromptNode';
import CodeNode from '../nodes/CodeNode';
import OutputNode from '../nodes/OutputNode';

export const nodeTypes = {
  prompt: PromptNode,
  code: CodeNode,
  output: OutputNode,
  start: PromptNode, // start node reuses PromptNode rendering
};

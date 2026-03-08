# RAG Eval Report

- 数据集规模：20 条（smoke/regression/adversarial）。
- 关键指标：
  - 命中率（Hit Rate）
  - MRR
  - 引用正确率（Citation Accuracy）
  - 注入拦截率（Injection Block Rate）
- 当前策略：词重叠召回 + prompt injection 规则拦截。
- 后续建议：引入向量检索与 rerank，对抗样例做持续回归。

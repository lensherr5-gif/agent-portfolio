# Capstone Architecture

## State Graph

`ingest -> plan -> retrieve -> analyze -> draft_report -> risk_check -> approve? -> publish`

## Sequence

1. 用户提交 trend query。
2. 编排层调用检索工具并聚合证据。
3. 分析节点生成结构化结论。
4. 风险检查节点执行策略校验。
5. 高风险时进入 HITL 审批。
6. 通过后发布报告并写审计日志。

## Permission Model

- Viewer: 仅查看报告。
- Operator: 可触发运行。
- Approver: 可批准高风险动作。
- Admin: 管理策略与密钥。

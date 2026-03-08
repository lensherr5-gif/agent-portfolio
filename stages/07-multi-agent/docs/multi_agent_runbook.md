# Multi-Agent Runbook

## 架构

- Supervisor: 控制流、错误处理、降级策略。
- Planner: 生成任务计划。
- Researcher: 汇总上下文证据。
- Executor: 执行工具动作（受权限白名单约束）。

## 风险控制

- 越权调用触发 `blocked`。
- 执行失败触发 `degraded`，返回降级报告。
- trace 统一输出 `run_id + agent_id`。

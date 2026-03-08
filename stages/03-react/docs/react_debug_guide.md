# ReAct Debug Guide

## 常见失败类型

- planning_error: 规划动作非法或输出结构错误。
- tool_error: 工具执行失败并达到失败阈值。
- execution_timeout: 总时长超过超时预算。
- execution_budget: 达到 max_steps 仍未完成。

## 排障步骤

1. 打开 `runs/<run_id>.json` 查看最后一步动作和 observation。
2. 核对 `action/tool/args` 是否满足 allowlist 和 schema。
3. 若为 tool_error，检查工具实现和参数边界。
4. 若为 execution_budget，优先优化 planner 终止条件。

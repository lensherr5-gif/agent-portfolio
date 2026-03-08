# 关卡 07：多智能体工程化（Supervisor 架构）

## 目标

- 构建可控的多 Agent 协作系统，而不是简单并发调用。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小多 Agent 框架

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个最小多智能体系统：
1) Supervisor + Planner + Researcher + Executor
2) 任务通过 handoff 传递，包含目标、约束、上下文
3) Executor 仅允许白名单工具
4) 失败时由 Supervisor 决定重试或降级
5) 提供 3 个测试（正常协作、越权阻断、失败降级）
```

### 你只做 3 件事

- 跑通 1 个端到端任务。
- 验证越权调用被拒绝。
- 验证失败后能进入降级路径。

## Level 2（1-2 小时）：工程加固任务

- 增加权限矩阵：`agent x tool x action`。
- 增加幂等控制，避免重复执行副作用。
- 增加统一追踪字段：`trace_id/run_id/agent_id`。
- 增加集成测试覆盖 5 个协作场景。

## Level 3（2-4 小时）：面试可讲深度

- 增加混沌测试（随机超时/空结果/429）。
- 增加隔离策略（敏感任务必须人工确认）。
- 增加性能基线（并发下成功率和延迟）。
- 产出 `multi_agent_runbook.md`。

## 产物

- `src/agents/`
- `src/policies/permissions.yaml`
- `docs/multi_agent_runbook.md`

## 验收

- L1：最小协作流程稳定可跑。
- L2：权限与追踪机制完整。
- L3：有混沌测试与性能基线。

## 本阶段新增能力（skills.md 对齐补充）

- Supervisor 编排 Planner/Researcher/Executor。
- 权限矩阵与越权阻断。
- 执行失败降级路径与 trace 字段。

## 5 分钟启动

```bash
cd stages/07-multi-agent
uv sync --dev
uv run python -m pytest -q
```

## 常用命令

```bash
./scripts/run.sh
./scripts/test.sh
./scripts/lint.sh
```

## 常见故障排查

- 总是 blocked：检查 `src/policies/permissions.yaml`。
- 降级未触发：确认执行阶段抛出可捕获异常。

## 验收标准

- 正常协作、越权阻断、失败降级三路径可复现。
- trace 包含 `run_id/agent_id`。

# 关卡 05：LangGraph 编排

## 目标

- 将 Agent 从脚本升级为可恢复状态机。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小状态图

### 直接给 AI 的提示词（可复制）

```text
帮我把 ReAct 重构成 LangGraph 最小流程：
1) 节点：plan -> act -> observe -> decide
2) 支持 checkpoint 和中断恢复
3) 高风险动作进入 human approval 节点
4) 提供最小可运行示例与 3 个测试
```

### 你只做 3 件事

- 跑通一次完整流程。
- 中断后从 checkpoint 恢复。
- 验证审批节点会拦截高风险操作。

## Level 2（1-2 小时）：工程加固任务

- 梳理统一状态结构（上下文、任务、错误、指标）。
- 增加条件分支与失败回路。
- 增加节点超时和重试策略。
- 增加状态迁移日志。

## Level 3（2-4 小时）：面试可讲深度

- 输出 `architecture.md`（状态图 + 时序图）。
- 增加 run replay：可按节点重放。
- 增加节点级 SLA（耗时阈值与告警）。
- 产出一次“卡在某节点”的定位案例。

## 产物

- `src/workflow/graph.py`
- `docs/architecture.md`
- `runs/checkpoints/`

## 验收

- L1：流程可恢复并可审批。
- L2：失败路径有清晰回路。
- L3：可用图和指标解释架构决策。

## 本阶段新增能力（skills.md 对齐补充）

- 状态图流程与 checkpoint 持久化。
- 中断恢复（resume）与审批节点（HITL）。
- 失败回路与迁移事件日志。

## 5 分钟启动

```bash
cd stages/05-langgraph
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

- 恢复失败：确认 `runs/checkpoints/<run_id>.json` 存在。
- 一直等待审批：恢复时需传入 `approved=True`。

## 验收标准

- 高风险任务会进入审批节点。
- checkpoint 可恢复并完成流程。

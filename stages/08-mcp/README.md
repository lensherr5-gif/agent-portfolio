# 关卡 08：MCP 工程化（协议化工具接入）

## 目标

- 通过 MCP 标准化工具接入，避免私有协议导致不可扩展。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小 MCP Server

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个最小 MCP server（todo 场景）：
1) 工具 add_task/list_tasks/done_task
2) sqlite 存储
3) token 鉴权
4) 调用审计日志（调用方、参数摘要、结果、耗时）
5) 提供 3 个测试（正常、鉴权失败、参数非法）
```

### 你只做 3 件事

- 跑通本地 server。
- 用 agent 客户端调用 3 个工具。
- 验证无 token 请求会被拒绝。

## Level 2（1-2 小时）：工程加固任务

- 增加 schema 契约测试（客户端/服务端一致性）。
- 增加版本字段与兼容策略。
- 增加超时与重试边界。
- 增加并发调用测试。

## Level 3（2-4 小时）：面试可讲深度

- 增加越权与重放攻击防护。
- 增加审计查询能力（按 run_id 检索调用链）。
- 增加部署配置（容器化 + 健康检查）。
- 产出 `mcp_contract.md`。

## 产物

- `mcp-server/`
- `mcp-server/tests/`
- `docs/mcp_contract.md`

## 验收

- L1：Agent 能稳定调用 MCP 工具。
- L2：契约和并发测试通过。
- L3：安全与可运维能力可展示。

## 本阶段新增能力（skills.md 对齐补充）

- MCP 风格 todo 工具：`add_task/list_tasks/done_task`。
- sqlite 持久化与 token 鉴权。
- 审计日志（caller/参数摘要/结果摘要/耗时）。

## 5 分钟启动

```bash
cd stages/08-mcp
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

- 鉴权失败：确认 token 与服务端一致。
- `task_not_found`：确认 task_id 已存在且 > 0。

## 验收标准

- 工具调用稳定，未授权请求被拒绝。
- 审计日志字段完整。

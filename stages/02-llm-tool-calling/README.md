# 关卡 02：LLM API + Tool Calling

## 目标

- 结构化输出稳定可解析。
- 工具调用有参数校验与失败恢复。

## L1 当前实现

- `json_guard`：解析失败后自动修复并重试。
- 工具白名单 + 参数 schema 校验。
- regression 用例 >= 20。

## L2 当前实现

- 工具调用超时保护与错误分类（`SCHEMA_ERROR/TOOL_TIMEOUT/TOOL_EXEC_ERROR/POLICY_BLOCKED`）。
- 审计日志字段完整：`run_id,module,tool_name,event,error_code,attempt,latency_ms,args_digest,result_digest`。
- 回归集按 `smoke/regression/adversarial` 分层。

## L3 当前实现

- 敏感工具策略：`write_file_guarded` 需要确认。
- 指标统计与 `eval_report.md`。
- prompt 回归通过 `evals` 用例持续验证。
- CI 工作流：`.github/workflows/ci-stage02.yml`。

## 运行与验收

```bash
cd python-agent-starter
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run python -m pytest -q
uv run python -m evals.run_eval --mode all --report reports/eval_report.md
```

验收阈值：结构化解析成功率 >= 95%。

# stage02-llm-tool-calling

L1-L3 一次完成版本：JSON Guard + Tool Calling + Eval + CI。

## 5 分钟启动

```bash
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run python -m pytest -q
uv run python -m evals.run_eval --mode all --report reports/eval_report.md
```

## 双模式 LLM

- `LLM_MODE=mock`（默认，离线可跑）
- `LLM_MODE=openai`（需要 `OPENAI_API_KEY`）

## 工具集（通用三件套）

- `calculator`
- `web_search_mock`
- `write_file_guarded`（高风险，默认策略阻断）

## Tool Policy

`write_file_guarded` 需要 `confirm_sensitive=true`，否则返回 `POLICY_BLOCKED`。

## 评估输出

- 用例：`evals/cases/*.json`（smoke / regression(20+) / adversarial）
- 报告：`reports/eval_report.md`
- 指标：`success_rate`、`schema_valid_rate`、`tool_success_rate`、`auto_repair_success_rate`、Top3 failures

## 常用命令

```bash
bash scripts/test.sh
bash scripts/lint.sh
bash scripts/eval.sh
```

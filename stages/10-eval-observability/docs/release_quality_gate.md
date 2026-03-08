# Release Quality Gate

## 发布门禁

- `success_rate >= 0.90`
- `schema_valid_rate >= 0.98`
- `tool_success_rate >= 0.95`
- `p95_latency_ms <= 8000`

## 变更策略

- prompt / model / tool 任一变更后必须执行全量评估。
- 未达标禁止发布。
- 线上失败样例回灌 `evals/regression.json`。

## 5 分钟排障路径

1. 从 `reports/eval_report.md` 找 Top failure。
2. 通过 run_id 定位对应 trace。
3. 针对最高频错误先修复，再回归验证。

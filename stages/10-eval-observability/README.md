# 关卡 10：评估与可观测（回归体系）

## 目标

- 把 Agent 从能跑升级为可持续演进且不退化。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小评估框架

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个最小 Agent 评估框架：
1) 三类数据集：smoke/regression/adversarial
2) 统计指标：成功率、schema 合法率、工具成功率、平均延迟
3) 生成 eval_report.md
4) 失败分类：schema_error/tool_timeout/retrieval_miss/policy_block
5) 提供一个命令一键跑评估
```

### 你只做 3 件事

- 跑一次全量评估。
- 看报告中的 Top 失败类型。
- 修复 1 个最高频失败点。

## Level 2（1-2 小时）：工程加固任务

- 为每次变更增加评估门禁（改 prompt/模型/工具必跑）。
- 把线上失败 case 回灌到回归集。
- 增加 trace 与日志联动（统一 run_id）。
- 增加 P95 延迟和错误率趋势统计。

## Level 3（2-4 小时）：面试可讲深度

- 增加发布质量门槛（未达标禁止发布）。
- 增加 A/B 对比评估（新旧策略对比）。
- 增加可观测看板截图与排障案例。
- 产出 `release_quality_gate.md`。

## 产物

- `evals/`
- `reports/eval_report.md`
- `docs/release_quality_gate.md`

## 验收

- L1：可一键生成评估报告。
- L2：评估结果能拦截有风险变更。
- L3：有质量门禁与真实排障证据。

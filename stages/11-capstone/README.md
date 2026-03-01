# 关卡 11：Capstone（工程完整度）

## 目标

- 产出可投简历、可演示、可二开的完整 Agent 系统。

## 选型

- A：Agentic Trend Radar（趋势/舆情分析）。
- B：IM Agent Infrastructure（多平台 Agent 基建）。

## 强制工程要求

- 架构：分层清晰（Ingest / Orchestrate / Tools / Output / Governance）。
- 安全：权限分级、HITL、沙箱执行、审计留痕。
- 可靠性：重试、超时、熔断、降级。
- 可运维：Docker Compose 一键启动、健康检查、基础告警。
- 可评估：有固定回归集和发布门禁。

## 交付清单

- `README.md`（架构图、运行方式、限制说明）。
- `architecture.md`（状态图、时序图、权限模型）。
- `threat-model.md`（威胁面、风险等级、缓解策略）。
- `eval_report.md`（核心指标、失败分类、改进计划）。
- `demo.mp4`（2-3 分钟端到端演示）。

## 非功能性指标（建议）

- P95 响应延迟 < 8s（按你的场景可调整）。
- 关键链路可用性 >= 99%。
- 高风险操作审计覆盖率 = 100%。

## 面试答辩要点

- 为什么这样拆模块。
- 哪些风险用什么机制控制。
- 指标如何证明系统变好。
- 出故障如何 5 分钟内定位。

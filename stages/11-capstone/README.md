# Capstone: Agentic Trend Radar

## Overview

一个可演示的趋势分析 Agent 系统，覆盖采集、编排、工具调用、治理与评估闭环。

## Architecture Layers

- Ingest: 输入主题与时间窗口。
- Orchestrate: Supervisor + workflow graph。
- Tools: 检索、摘要、评分、报告生成。
- Output: 可追溯报告（sources + risk flags）。
- Governance: 权限、HITL、审计、质量门禁。

## Run

```bash
# 占位流程
python3 -c "print('capstone demo placeholder')"
```

## Constraints

- 当前 repo 为离线示例，不包含真实线上 API key。
- demo.mp4 为占位文件，需要替换为真实演示录屏。

## 常用命令

```bash
# 当前为离线演示占位
python3 -c "print('capstone demo placeholder')"
```

## 常见故障排查

- 无法演示端到端：先替换 `demo.mp4` 为真实录屏并补 API 密钥。
- 风险控制不可展示：按 `threat-model.md` 补齐策略执行日志。

## 验收标准

- 文档、威胁模型、评估报告和演示文件齐全。

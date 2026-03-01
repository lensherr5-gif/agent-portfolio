# Architecture (Stage 00 Level 3)

## 目标

提供一个最小但工程化的 CLI Agent 基座，强调可观测与可排障。

## 模块

- `app.py`: 进程入口。
- `src/app/cli.py`: 参数处理、主流程编排、统一错误出口。
- `src/app/config.py`: `.env` 解析与配置校验。
- `src/common/errors.py`: 统一错误类型与错误元数据。
- `src/common/logging_utils.py`: JSON 日志输出。

## 时序

1. 解析 CLI 参数。
2. 生成或校验 `run_id`。
3. 加载配置并做必填/白名单校验。
4. 成功输出 `app_started`；失败输出 `app_failed`。

## 设计要点

- 结构化日志字段固定，便于检索和告警。
- 错误类型分层，便于后续统计失败原因。
- 测试覆盖成功路径与关键失败路径。

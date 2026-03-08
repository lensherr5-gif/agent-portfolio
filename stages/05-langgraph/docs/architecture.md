# LangGraph-style Architecture

## State

- `run_id`: 运行标识
- `task`: 当前任务
- `node`: 当前节点
- `approved`: 是否通过人工审批
- `events[]`: 节点迁移日志
- `status`: running / awaiting_approval / succeeded / failed

## Flow

`plan -> (human_approval)? -> act -> observe -> decide`

- 高风险任务进入 `human_approval`。
- 所有节点完成后写入 `runs/checkpoints/<run_id>.json`。
- 中断后可通过 `resume=True` 从 checkpoint 恢复。

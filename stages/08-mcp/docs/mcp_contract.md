# MCP Contract

## Tools

- `add_task(text)` -> `{id,text,done}`
- `list_tasks()` -> `{tasks:[...]}`
- `done_task(task_id)` -> `{id,text,done}`

## Security

- 所有调用必须提供 token。
- 失败返回鉴权或参数错误。

## Auditing

- 审计字段：`caller, tool, args_digest, result_digest, latency_ms`。
- 支持按调用链追踪工具执行情况。

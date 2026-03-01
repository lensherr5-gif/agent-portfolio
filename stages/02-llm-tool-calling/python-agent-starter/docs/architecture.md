# Stage02 Architecture

- `llm_client`: 负责 mock/openai 双模式文本生成。
- `json_guard`: 负责 JSON 解析、修复与 schema 校验。
- `tool_registry`: 负责工具注册、白名单、参数校验、审计日志、超时保护。
- `tool_policy`: 对高风险工具执行前做阻断策略。
- `orchestrator`: 把 LLM 输出、工具调用和恢复策略串起来。
- `evals/run_eval.py`: 跑 smoke/regression/adversarial 并输出报告。

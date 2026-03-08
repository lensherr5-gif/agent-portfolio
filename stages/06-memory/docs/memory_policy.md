# Memory Policy

## 写入策略

- 仅在 `confidence >= 0.6` 时允许写入长期记忆。
- 命中注入模式（如 `ignore previous instructions`）时拒绝写入。
- 命中敏感信息模式（密码、密钥、证件号）时拒绝写入。

## 召回策略

- 默认按用户隔离。
- 支持按 topic 过滤。
- 支持 TTL 到期自动失效。

## 审计

- 每次写入和拦截记录到 `audit_log`。

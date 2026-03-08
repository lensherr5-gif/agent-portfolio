# Threat Model

## Attack Surface

- Prompt injection
- Tool privilege escalation
- Replay attacks on sensitive actions
- Data exfiltration via report channel

## Risk Levels

- High: 越权写入、敏感数据外泄
- Medium: 错误引用导致误判
- Low: 非关键链路延迟抖动

## Mitigations

- 工具白名单 + 参数 schema + 审计。
- 高风险动作必须 HITL。
- 对外输出做敏感字段脱敏。
- 发布前执行回归评估与质量门禁。

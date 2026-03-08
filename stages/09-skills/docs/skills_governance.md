# Skills Governance

## 目标

- Skill 可发现、可版本化、可审计。
- 新增 Skill 不改主流程，仅注册到 router。

## 治理策略

- 版本：语义化版本号。
- 风险评级：low / medium / high。
- 授权：按用户白名单执行。
- 审计：记录命中、拦截、执行事件。

## 升级兼容

- 允许 v1/v2 并行注册。
- router 依据关键词与策略选择目标版本。

# Stages 导航（工程化执行版）

> 每个关卡一个独立目录，按 `README` 执行并提交产物。

## 目录

- [00-foundation](./00-foundation/README.md)
- [01-python-engineering](./01-python-engineering/README.md)
- [02-llm-tool-calling](./02-llm-tool-calling/README.md)
- [03-react](./03-react/README.md)
- [04-rag](./04-rag/README.md)
- [05-langgraph](./05-langgraph/README.md)
- [06-memory](./06-memory/README.md)
- [07-multi-agent](./07-multi-agent/README.md)
- [08-mcp](./08-mcp/README.md)
- [09-skills](./09-skills/README.md)
- [10-eval-observability](./10-eval-observability/README.md)
- [11-capstone](./11-capstone/README.md)

## 每关预计耗时

- 单关标准节奏：`Level 1` 0.5-1h，`Level 2` 1-2h，`Level 3` 2-4h，总计约 3.5-7h。
- 建议每周完成 1-2 关（工作日碎片时间 + 周末集中完成 L3）。

## 进入下一关门槛（Gate）

1. `00-foundation -> 01`：`python -m app --help` 可运行，`pytest` 全绿，含 `run_id` 日志。
2. `01-python-engineering -> 02`：超时/429 可恢复，至少 5 个测试，错误分类清晰。
3. `02-llm-tool-calling -> 03`：20 条样例结构化成功率 >= 95%，工具白名单生效。
4. `03-react -> 04`：ReAct 可终止、可追踪，`runs/<run_id>.json` 完整可读。
5. `04-rag -> 05`：回答带 `sources[]`，注入样例可阻断或降权。
6. `05-langgraph -> 06`：图编排可 checkpoint 恢复，高风险节点可人工确认。
7. `06-memory -> 07`：跨轮可复用用户偏好，污染文本不入长期记忆。
8. `07-multi-agent -> 08`：多 Agent 协作稳定，越权调用被阻断，失败可降级。
9. `08-mcp -> 09`：MCP 工具可用，鉴权生效，审计日志完整。
10. `09-skills -> 10`：新增 skill 不改主流程，skill 路由可测试可回归。
11. `10-eval-observability -> 11`：可一键生成评估报告，失败可在 5 分钟内定位。

## 通用执行规则

1. 每关至少产出：`README`、可运行代码、测试、`run` 样例日志。
2. 每关必须有可度量验收指标：成功率、延迟、失败分类。
3. 每关新增能力必须写回归用例，避免后续回归破坏。
4. 关卡 07 之后强制执行：权限分级、审计日志、HITL、风险清单。

# agent-portfolio

这是你的总控仓库（最大 repo），用于管理学习路线、阶段仓库链接和进度。

## 仓库结构策略

- `agent-portfolio`：总导航与治理，不放大量业务代码。
- `stage-XX-*`：每关独立仓库，按 `level-1/2/3` 分支演进。
- `agent-capstone`：最终工程化项目独立仓库（简历主仓库）。

## 命名规范

- `stage-00-foundation`
- `stage-01-python-engineering`
- `stage-02-llm-tool-calling`
- `stage-03-react`
- `stage-04-rag`
- `stage-05-langgraph`
- `stage-06-memory`
- `stage-07-multi-agent`
- `stage-08-mcp`
- `stage-09-skills`
- `stage-10-eval-observability`
- `agent-capstone`

## 分支规范（每个 stage repo）

- `level-1`：最小可运行
- `level-2`：工程加固
- `level-3`：面试深度
- `main`：最终稳定版本（由 level-3 合并而来）

## 当前本地映射

- `stage-00-foundation` -> `../stages/00-foundation`

## 建议工作流

1. 在阶段仓库完成对应 level 的开发。
2. 每个 level 结束后打标签：`v0-l1` / `v0-l2` / `v0-l3`。
3. 在本仓库记录进度与里程碑。

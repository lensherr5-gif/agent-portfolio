# skills.md

## 目标

用于章节（stage-00 ~ stage-11）代码生成时的统一约束，确保产出可运行、可测试、可评估、可维护。

## 项目上下文

- 仓库类型：单仓（monorepo）
- 仓库根目录：`/home/hairen/project/agent`
- 核心学习主线：`stages/00-foundation` 到 `stages/11-capstone`

## 技术栈基线

- Python >= 3.11
- 包管理：`uv`
- 测试：`pytest`
- 代码质量：`ruff` + `pre-commit`
- CI：GitHub Actions（`.github/workflows/`）

## 代码生成总规则

1. 必须先复用上一个阶段可用能力，再新增本阶段能力。
2. 每次生成都要包含：
   - 代码
   - 测试
   - README 更新
   - 运行命令
3. 默认生成最小可运行版本，再给工程加固点。
4. 不引入未使用的依赖，不生成无法运行的占位代码。
5. 主要代码必须有中文注释（详细且关键）。

## 目录与命名约束

- 每关目录：`stages/<stage-name>/`
- 若有可运行样例，统一放在：`python-agent-starter` 或该阶段独立子目录
- 文档统一放在：`docs/`
- 测试统一放在：`tests/`
- 脚本统一放在：`scripts/`

## 分层约束（Python）

- `src/app`：入口编排、参数解析、流程控制
- `src/common`：通用工具（日志、错误、配置基础能力）
- `src/<domain>`：阶段特定领域逻辑（如 rag、memory、agents）

## 错误与日志约束

- 错误类型统一继承基础错误类型（如 `AppError`）
- 错误日志至少包含：`module`, `error_code`, `reason`, `hint`
- 运行日志必须带 `run_id`
- 失败路径必须可观测、可定位

## 测试生成约束

每个阶段至少包含：

1. 成功路径测试
2. 参数/输入非法测试
3. 配置缺失或依赖异常测试
4. 关键日志字段测试
5. 本阶段新增能力专属测试

默认命令：

```bash
uv run python -m pytest -q
```

## CI 约束

- workflow 必须放在仓库根：`.github/workflows/*.yml`
- 至少执行：
  - `uv sync --dev`
  - `ruff check` + `ruff format --check`
  - `pytest`
- 对 monorepo 场景，使用 `paths` 仅触发相关阶段

## README 生成模板约束

每阶段 README 至少包含：

1. 阶段目标
2. 本阶段新增能力
3. 5 分钟启动
4. 常用命令（run/test/lint）
5. 常见故障排查
6. 验收标准

## Git 流程约束

- 分支策略：`main` + `stageXX-l1/stageXX-l2/stageXX-l3`（按阶段推进）
- 提交信息格式：
  - `level-1: ...`
  - `level-2: ...`
  - `level-3: ...`
- 每个 level 完成建议打标签：`stageXX-l1/l2/l3`
- 合并策略（强制）：`stageXX-l3` 提交后，必须在 CI 通过后自动合并到 `main`（建议使用 GitHub Auto-merge）。

## 阶段生成策略（后续章节）

- Level 1：最小可运行（必须能跑）
- Level 2：工程加固（错误处理、日志、测试增强）
- Level 3：工程深度（CI、质量门禁、复盘文档、可观测）
- 强制要求：所有章节的 Level 3 都必须包含 CI 测试配置，且 CI 至少执行 `uv sync --dev`、`ruff check + format --check`、`pytest`。

## Definition of Done（DoD）

一次章节代码生成完成的最低标准：

1. 本地可运行
2. 本地测试通过
3. README 可指导新人 5 分钟跑通
4. CI 配置可触发并通过
5. 至少 1 个真实失败场景有复盘文档

## 禁止事项

- 不要只改 README 不改代码
- 不要只加功能不加测试
- 不要在非根目录放 workflow
- 不要引入与阶段目标无关的大量依赖
- 不要删除已有可用能力而不提供迁移说明

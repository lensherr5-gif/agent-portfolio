# 关卡 03：ReAct 复现

## 目标

- 从零实现可运行 ReAct 循环并带工程护栏。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小 ReAct Loop

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个最小 ReAct Agent：
1) think -> act -> observe -> decide 循环
2) 支持 max_steps 和全局 timeout
3) 工具 allowlist + 参数校验
4) 每次运行保存 runs/<run_id>.json
5) 提供 3 个测试（成功任务、超步数终止、工具失败）
```

### 你只做 3 件事

- 跑通 3 个基础任务。
- 检查轨迹文件是否完整。
- 修复循环终止和异常处理。

## Level 2（1-2 小时）：工程加固任务

- 加入失败阈值策略（连续失败 N 次终止）。
- 为每一步记录 token、耗时、工具耗时。
- 增加“计划修正”分支（失败后改用备选工具）。
- 增加 10 条任务回归集。

## Level 3（2-4 小时）：面试可讲深度

- 增加 replay 能力（用历史轨迹回放运行）。
- 增加 deterministic 模式（固定随机种子/固定工具返回）。
- 增加 failure taxonomy（规划错、执行错、工具错）。
- 产出 `react_debug_guide.md`。

## 产物

- `src/agent/react_loop.py`
- `runs/*.json`
- `evals/react_tasks.json`

## 验收

- L1：基础任务可跑通，失败可终止。
- L2：10 条任务可复现并有指标。
- L3：支持回放与故障分类分析。

## 本阶段新增能力（skills.md 对齐补充）

- 可终止的 ReAct 循环（max_steps/timeout/failure threshold）。
- 工具 allowlist 与参数类型检查。
- 运行轨迹持久化到 `runs/<run_id>.json`。
- replay 能力与 failure taxonomy。

## 5 分钟启动

```bash
cd stages/03-react
uv sync --dev
uv run python -m pytest -q
```

## 常用命令

```bash
./scripts/run.sh
./scripts/test.sh
./scripts/lint.sh
```

## 常见故障排查

- `ModuleNotFoundError`：确认在阶段目录执行命令并已 `uv sync --dev`。
- 运行无输出轨迹：确认 `runs/` 目录可写。

## 验收标准

- 成功/失败路径都可终止且轨迹完整。
- `pytest` 通过，`ruff` 校验通过。

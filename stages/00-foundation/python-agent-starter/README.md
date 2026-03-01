# python-agent-starter

Level 3 工程化版本：可运行、可测试、可 lint、可 CI、可复盘。

## 5 分钟启动

```bash
# 1) 安装 uv（若已安装可跳过）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) 安装依赖
uv sync --dev

# 3) 准备配置
cp .env.example .env

# 4) 本地验证
uv run python -m app --help
uv run python -m pytest -q
```

## 架构说明

### 目录结构

- `app.py`：CLI 主入口。
- `src/app/cli.py`：参数解析、run_id 校验、错误出口。
- `src/app/config.py`：配置解析与校验（必填项/日志等级）。
- `src/common/errors.py`：统一错误类型与错误码。
- `src/common/logging_utils.py`：结构化日志输出。
- `tests/`：单元测试（参数、配置、日志、错误路径）。
- `scripts/`：工程脚本（`run/test/lint`）。
- `docs/`：工程文档与故障复盘。

### 运行时流程

1. `app.py` 调用 `src/app/cli.main()`。
2. CLI 解析参数并确定 `run_id`。
3. 加载配置并执行校验。
4. 成功路径输出 `app_started`；失败路径输出 `app_failed`，并携带 `module/error_code/reason/hint`。

## 常用命令

```bash
# 运行应用
make run
# 或
bash scripts/run.sh --run-id demo001

# 跑测试
make test
# 跑详细测试（显示每个测试名）
make test-v
# 或
bash scripts/test.sh

# Lint
make lint
# 或
bash scripts/lint.sh
```

## pre-commit

```bash
make precommit-install
uv run pre-commit run -a
```

## CI

已提供 GitHub Actions 工作流：

- `.github/workflows/ci.yml`
- 触发：`push` / `pull_request`
- 流程：`uv sync --dev` -> `ruff check + format --check` -> `pytest`

## 常见失败排查

### 1) `No module named src`

原因：未在项目根目录执行，或未通过 `uv run` 启动。

处理：

```bash
cd python-agent-starter
uv run python -m pytest -q
```

### 2) `pytest: command not found`

原因：系统环境没有 pytest。

处理：

```bash
uv sync --dev
uv run python -m pytest -q
```

### 3) 启动时报 `CFG_MISSING`

原因：`.env` 缺少 `APP_NAME` 或 `APP_ENV`。

处理：

```bash
cp .env.example .env
# 或显式指定
uv run python -m app --env-file /path/to/.env
```

## 故障复盘

- 文档：`docs/postmortem-env-missing.md`
- 场景：配置缺失导致启动失败
- 结论：通过配置必填校验 + 结构化错误日志，定位时间从分钟级降到秒级。

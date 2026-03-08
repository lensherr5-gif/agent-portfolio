# 关卡 01：Python 工程必修

## 目标

- 让代码具备可维护性、可排障性、可恢复性。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小工程能力

### 直接给 AI 的提示词（可复制）

```text
基于一个 Python agent starter，帮我补齐工程能力：
1) http_client，支持 timeout + retry + 指数退避 + 429 处理
2) 必须提供真实联网 transport（例如 httpx/requests），不是只写 mock
2) 统一异常模型（配置错误、请求错误、业务错误）
3) 日志包含 run_id 和 error_code
4) 至少 3 个 pytest（超时、429、正常返回）
请输出完整文件代码和修改说明。
```

### 你只做 3 件事

- 粘贴并落地生成代码。
- 本地运行 `pytest`。
- 修复导入路径或依赖问题，确保可运行。

### Level 1 新增强制要求（已更新）

- `http_client` 不能只依赖假 transport，必须有一个真实联网入口（可对公开 API 发起请求）。
- 测试仍优先使用 mock/假 transport，保证可重复和稳定。

### Level 1 当前实现（本仓库）

- 目录：`python-agent-starter/`
- 已实现：
  - `src/common/http_client.py`：超时重试、429 重试、指数退避
  - `src/common/errors.py`：统一异常模型（配置/请求/业务）
  - 日志字段：失败日志记录 `run_id` + `error_code`
  - `tests/test_http_client.py`：至少 3 条测试（当前 4 条）

### Level 1 验证命令

```bash
cd python-agent-starter
uv sync --dev
uv run python -m pytest -q
```

## Level 2（1-2 小时）：工程加固任务

- 为 `http_client` 增加可配置重试策略（最大次数、退避系数、可重试错误码）。
- 为网络调用增加超时分层（连接超时/读超时）。
- 统一错误映射：将第三方异常映射到内部错误码。
- 测试扩展到 5 个以上，覆盖边界输入。
- 增加 1 条真实联网 smoke 测试（可通过环境变量开关，仅在联网环境执行）。

### Level 2 当前实现（本仓库）

- 可配置重试策略：`RetryPolicy`
  - `max_retries`
  - `base_backoff_seconds`
  - `backoff_multiplier`
  - `retriable_error_codes`
  - `retriable_status_codes`
- 超时分层：`TimeoutPolicy`
  - `connect_timeout_seconds`
  - `read_timeout_seconds`
- 第三方异常映射：`map_external_error(...)`
  - `TimeoutError(connect/read)` -> `CONNECT_TIMEOUT / READ_TIMEOUT`
  - `ConnectionError` -> `NETWORK_ERROR`
  - 带 `status_code` 的异常 -> `HTTP_<status>`
- 真实联网 transport：`build_httpx_get_transport(...)`（httpx）
- 测试已扩展到 9 条，其中 1 条为联网 smoke（默认跳过，可通过环境变量开启）。

### Level 2 验证命令

```bash
cd python-agent-starter
uv run python -m pytest -q
STAGE01_HTTP_SMOKE=1 uv run python -m pytest -q -k real_http_transport_smoke
```

## Level 3（2-4 小时）：面试可讲深度

- 增加熔断机制（连续失败后快速失败）。
- 增加并发控制（Semaphore）防止瞬时洪峰。
- 增加故障注入测试（随机超时/随机 429）验证恢复能力。
- 产出一份 `postmortem.md`：一次失败如何定位与修复。

### Level 3 当前实现（本仓库）

- 熔断机制：`CircuitBreaker`
  - 连续失败达到阈值后转为 `OPEN`
  - 熔断打开期间快速失败，避免继续放大上游压力
- 并发控制：`request_many_with_semaphore(...)`
  - 使用 `asyncio.Semaphore` 限制并发度
- 故障注入测试：
  - 随机注入 `timeout` 与 `429`，验证重试恢复能力
- 复盘文档：
  - `python-agent-starter/docs/postmortem.md`
- CI（Level 3 强制项）：
  - 根目录工作流：`.github/workflows/ci-stage01.yml`
  - 自动执行 `uv sync --dev`、`ruff`、`pytest`

### Level 3 验证命令

```bash
cd python-agent-starter
uv run python -m pytest -q
uv run ruff check . && uv run ruff format --check .
```

## 产物

- `src/common/http_client.py`
- `src/common/errors.py`
- `tests/test_http_client.py`

## 验收

- L1：超时与 429 场景可恢复，`pytest` 全绿。
- L2：失败日志能定位到重试次数与最终失败原因。
- L3：有故障注入结果和复盘文档。

# stage01-python-engineering

Level 3 工程深度实现：熔断 + 并发控制 + 故障注入测试 + CI。

## 快速开始

```bash
uv sync --dev
uv run python -m pytest -q
```

## 核心能力

- `src/common/http_client.py`
  - 支持 `RetryPolicy` 自定义重试（次数、退避系数、可重试错误码/状态码）
  - 支持 `TimeoutPolicy`（连接超时、读取超时）
  - 支持真实联网 transport：`build_httpx_get_transport(...)`
  - 支持第三方异常映射为内部错误码
  - 支持 `CircuitBreaker` 熔断保护
  - 支持 `request_many_with_semaphore(...)` 并发限流
  - 支持 `run_id` 与 `error_code` 日志
- `src/common/errors.py`
  - 统一错误层次：配置错误 / 请求错误 / 业务错误

## 主要测试

- 正常请求成功返回
- 超时后自动重试并成功（含连接/读取区分）
- 429 后自动重试并成功
- 非重试状态码（500）快速失败
- 自定义策略禁用重试时快速失败
- 超过重试上限后抛错
- 真实联网 smoke 测试（环境变量开关，默认跳过）
- 熔断打开后快速失败
- Semaphore 并发上限验证
- 随机故障注入恢复验证

## 联网 smoke 测试（可选）

```bash
STAGE01_HTTP_SMOKE=1 uv run python -m pytest -q -k real_http_transport_smoke
```

## CI

- 工作流：`/home/hairen/project/agent/.github/workflows/ci-stage01.yml`
- 触发分支：`main, stage01-l1, stage01-l2, stage01-l3`
- 检查项：`uv sync --dev` -> `ruff` -> `pytest`

## 故障复盘

- 文档：`docs/postmortem.md`

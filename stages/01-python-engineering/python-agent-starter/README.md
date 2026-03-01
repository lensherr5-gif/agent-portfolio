# stage01-python-engineering

Level 2 工程加固实现：可配置重试策略 + 超时分层 + 第三方异常映射。

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

## 联网 smoke 测试（可选）

```bash
STAGE01_HTTP_SMOKE=1 uv run python -m pytest -q -k real_http_transport_smoke
```

# stage01-python-engineering

Level 1 最小工程实现：可重试 HTTP Client + 统一错误模型 + 基础测试。

## 快速开始

```bash
uv sync --dev
uv run python -m pytest -q
```

## 核心能力

- `src/common/http_client.py`
  - 支持超时重试
  - 支持 429 指数退避重试
  - 支持 `run_id` 与 `error_code` 日志
- `src/common/errors.py`
  - 统一错误层次：配置错误 / 请求错误 / 业务错误

## 主要测试

- 正常请求成功返回
- 超时后自动重试并成功
- 429 后自动重试并成功
- 超过重试上限后抛错

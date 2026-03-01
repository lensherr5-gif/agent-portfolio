# Postmortem: 配置缺失导致启动失败

## 事件摘要

- 时间：本地开发阶段
- 影响：CLI 启动失败，返回码 2
- 现象：日志输出 `app_failed`，错误码 `CFG_MISSING`

## 复现步骤

```bash
tmp=$(mktemp)
printf 'APP_ENV=dev\n' > "$tmp"
uv run python -m app --env-file "$tmp" --run-id demo002
rm -f "$tmp"
```

## 观测到的日志

```json
{"level":"ERROR","message":"app_failed","module":"config","error_code":"CFG_MISSING","reason":"missing required env key: APP_NAME","hint":"set APP_NAME in .env or pass --env-file"}
```

## 根因

- 配置文件缺少必填字段 `APP_NAME`。

## 修复

- 在配置加载层增加必填校验 `_require(...)`。
- 在错误对象中增加 `hint`，输出可执行修复提示。

## 预防措施

- `.env.example` 保持完整并在 README 给出启动前检查步骤。
- CI 持续跑测试，保证关键错误路径不回归。

# 关卡 00：开局装备（Foundation）

## 目标

- 建立可复用 Python 工程模板。
- 建立最小 Git 流程与提交规范。

## 推荐执行方式（先快后深）

不要从 0 手敲。先让 AI 生成最小可运行模板，再做二级/三级任务加深。

## Git 操作（完成三个 Level）

### 1) 初始化与分支

```bash
cd stages/00-foundation
git init
git branch -m main
git switch -c level-1
git switch main
git switch -c level-2
git switch main
git switch -c level-3
```

### 2) Level 1 提交与标签

```bash
git switch level-1
git add .
git commit -m "level-1: complete minimal starter"
git tag v0-l1
```

### 3) Level 2 提交与标签

```bash
git switch level-2
git add .
git commit -m "level-2: complete engineering hardening"
git tag v0-l2
```

### 4) Level 3 提交与标签

```bash
git switch level-3
git add .
git commit -m "level-3: complete engineering depth"
git tag v0-l3
```

### 5) 合并到 main（最终稳定版）

```bash
git switch main
git merge --no-ff level-1 -m "merge level-1 into main"
git merge --no-ff level-2 -m "merge level-2 into main"
git merge --no-ff level-3 -m "merge level-3 into main"
```

### 6) 推送远程仓库（可选）

```bash
git remote add origin <your-repo-url>
git push -u origin main
git push origin level-1 level-2 level-3
git push origin v0-l1 v0-l2 v0-l3
```

## Level 1（30-60 分钟）：AI 生成最小模板

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个 Python agent starter 最小工程，要求：
1) 目录：src/, tests/, scripts/, docs/
2) 可运行 CLI：python -m app --help
3) 配置：.env.example + 配置加载
4) 日志：结构化日志，包含 run_id
5) 测试：至少 2 个 pytest（配置加载、CLI 参数解析）
6) 输出完整文件树和每个文件代码
```

### 你只做 3 件事

- 把生成代码落地到仓库。
- 本地运行：`pytest`、`python -m app --help`。
- 修复能看到的报错，直到可运行。

## Level 2（1-2 小时）：工程加固任务

- 给 `src` 加分层：`common/`, `app/`，避免所有代码堆在一个文件。
- 引入统一错误类型：配置错误、参数错误、运行时错误分开。
- CLI 增加 `--run-id`（可选传入，不传则自动生成）。
- 测试扩展到 5 个：参数缺失、非法参数、环境变量缺失、日志字段校验、help 输出。

## Level 3（2-4 小时）：面试可讲深度

- 增加 `Makefile` 或 `scripts/`：`run`, `test`, `lint`。
- 增加 `pre-commit`（格式化 + lint + 基础安全检查）。
- 增加 CI（GitHub Actions）：push/PR 自动跑测试。
- README 增加“架构说明 + 常见失败排查 + 5 分钟启动”。
- 输出一次真实排障记录（例如 env 缺失导致失败，如何定位和修复）。

## 产物

- `python-agent-starter` 仓库或目录。
- 一条从 clone 到运行的 5 分钟文档路径。

## 验收

- L1：新机器按 README 可跑通，`pytest` 全绿。
- L2：测试不少于 5 个，失败日志可定位到模块和原因。
- L3：有 CI 截图或链接，有一次完整故障复盘记录。

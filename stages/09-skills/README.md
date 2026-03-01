# 关卡 09：Skills 工程化（可复用能力包）

## 目标

- 将能力从写死在主流程升级为可发现、可版本化、可审计的 Skill 包。

## 推荐执行方式（先快后深）

## Level 1（30-60 分钟）：AI 生成最小 Skill 包

### 直接给 AI 的提示词（可复制）

```text
帮我生成一个符合 Agent Skills 思路的最小 skill 包（job-hunter）：
1) skills/job-hunter/SKILL.md（用途、输入输出、示例）
2) scripts/parse_jd.py（解析 JD 结构化输出）
3) scripts/interview_qa.py（根据 JD 生成面试题）
4) skill router（按关键词路由）
5) 提供 3 个测试（命中路由、未命中、越权阻断）
```

### 你只做 3 件事

- 跑通 1 次 skill 调用。
- 验证 router 能选中正确 skill。
- 验证未授权 skill 不会执行。

## Level 2（1-2 小时）：工程加固任务

- 给 skill 增加版本号和依赖声明。
- 给 skill 执行增加沙箱策略。
- 增加 skill registry（可发现、可禁用、可审计）。
- 增加 10 条 skill 路由回归样例。

## Level 3（2-4 小时）：面试可讲深度

- 增加 skill 风险评级（低/中/高）。
- 增加审批流（高风险 skill 需人工批准）。
- 增加升级兼容策略（v1/v2 并行）。
- 产出 `skills_governance.md`。

## 产物

- `skills/job-hunter/`
- `src/skills/router.py`
- `docs/skills_governance.md`

## 验收

- L1：技能可被调用且可复用。
- L2：新增技能不改主流程。
- L3：技能治理策略可讲清并可演示。

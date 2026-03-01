# AI Agent 系统学习路线图（闯关打开式 · 8 周从 0 到可面试作品集）

> **玩法**：按关卡顺序“解锁”。每关都要交付**可运行产物**（代码仓库 / README / Demo / Eval 报告）。
> **终局目标**：做出一个工程完整度较高的 Agent 项目（对标 **AstrBot / TrendRadar / TrendAgent** 这类“能跑、能用、能扩展”的系统），并能在面试中讲清楚**架构、可控性、安全、评估、可观测性**。

---

## 执行方式升级（建议采用）

为保证每一关都能真正落地，建议按关卡拆分独立目录与 README：

- 总导航：`stages/README.md`
- 每关独立执行文档：`stages/<stage-name>/README.md`
- 从关卡 07 开始，强制执行工程化要求：权限分级、HITL、审计日志、评估门禁、可回放 trace。

你可以直接从下面入口开始：

* [分关卡执行目录](./stages/README.md)

---

## 0）等级说明（每个知识点都标注 5 级）

* **了解**：能说清楚它解决什么问题；能跑通官方最小 demo。
* **熟悉**：能选型并落到项目里；遇到报错能读文档/issue解决；能讲清 trade-off。
* **必须掌握**：能独立实现核心流程（不是 copy）；有异常兜底；能写测试/日志。
* **看源码**：能沿调用链定位关键模块并改一处验证行为变化。
* **必须复现**：从零实现一个可运行版本（可简化），并用 demo/测试证明你复现了。

---

## 1）资源索引（官方 / GitHub 仓库地址）

> 建议你把本节复制到你的“学习总仓库 README”里，作为快捷入口。

### Agent/LLM 工程主栈

* OpenAI Cookbook（API 示例集合）

  * `https://github.com/openai/openai-cookbook` ([GitHub][1])
* OpenAI Evals（评估框架）

  * `https://github.com/openai/evals` ([GitHub][2])
* OpenAI Agents SDK（多智能体 + Guardrails + Tracing）

  * `https://github.com/openai/openai-agents-python` ([GitHub][3])
  * Docs：`https://openai.github.io/openai-agents-python/` ([OpenAI][4])

### LangChain / LangGraph 体系（强建议主学）

* LangChain

  * `https://github.com/langchain-ai/langchain` ([GitHub][5])
* LangGraph（图编排/状态机/可恢复）

  * `https://github.com/langchain-ai/langgraph` ([GitHub][6])
* LangChain Academy（官方课程仓库）

  * `https://github.com/langchain-ai/langchain-academy` ([GitHub][7])
* Memory Template（长期记忆服务模板）

  * `https://github.com/langchain-ai/memory-template` ([GitHub][8])

### MCP（工具/数据接入协议）

* MCP Specification

  * `https://github.com/modelcontextprotocol/modelcontextprotocol` ([GitHub][9])
* MCP Servers（参考实现集合）

  * `https://github.com/modelcontextprotocol/servers` ([GitHub][10])
* MCP Registry（注册中心）

  * `https://github.com/modelcontextprotocol/registry` ([GitHub][11])

### Skills（重点：AgentSkills + OpenClaw Skills 生态）

* Agent Skills（规范 + 文档 + 参考 SDK）

  * `https://github.com/agentskills/agentskills` ([GitHub][12])
* Agent Skills 规范页（SKILL.md 格式）

  * `https://agentskills.io/specification` ([agentskills.io][13])
* OpenClaw（个人助理 + Skills 生态）

  * `https://github.com/openclaw/openclaw` ([GitHub][14])
* OpenClaw Skills 文档

  * `https://docs.openclaw.ai/tools/skills` ([OpenClaw][15])
* ClawHub（OpenClaw 公共 Skills 注册中心）

  * Repo：`https://github.com/openclaw/clawhub` ([GitHub][16])
  * Docs：`https://docs.openclaw.ai/zh-CN/tools/clawhub` ([OpenClaw][17])
* OpenClaw skills 备份仓库（大量技能版本）

  * `https://github.com/openclaw/skills` ([GitHub][18])

### 观测 & 评估（面试拉开差距）

* promptfoo（本地 eval + red teaming）

  * `https://github.com/promptfoo/promptfoo` ([GitHub][19])
* Phoenix（开源 AI 可观测/评估）

  * `https://github.com/Arize-ai/phoenix` ([GitHub][20])

### 多智能体框架补充

* AutoGen

  * `https://github.com/microsoft/autogen` ([GitHub][21])
* Semantic Kernel

  * `https://github.com/microsoft/semantic-kernel` ([GitHub][22])
* CrewAI

  * `https://github.com/crewAIInc/crewAI` ([GitHub][23])
  * Examples：`https://github.com/crewAIInc/crewAI-examples` ([GitHub][24])
* AutoGPT

  * `https://github.com/Significant-Gravitas/AutoGPT` ([GitHub][25])

### 终局对标项目（你提到的风格）

* AstrBot（IM 多平台 + 插件/技能 + 沙箱等，工程完整度高）

  * `https://github.com/AstrBotDevs/AstrBot` ([GitHub][26])
* TrendRadar（多源热点/舆情聚合 + 推送 + Docker 等，工程完整度高）

  * `https://github.com/sansan0/TrendRadar` ([GitHub][27])
* trendagent / trend_agent（“趋势 agent”相关仓库示例，供对标）

  * `https://github.com/eesha2712/trendagent` ([GitHub][28])
  * `https://github.com/chenjianrui-111/trend_agent` ([GitHub][29])

---

## 2）主线关卡（闯关打开式）

> **建议你建一个总仓库**：`agent-portfolio/`
> 每关产出一个子项目仓库（或 monorepo 子目录），并在总仓库 README 里挂上链接与 Demo。

---

<details>
<summary><b>关卡 0：开局装备（环境 / Git / 基础工程模板）</b></summary>

### 解锁条件

* 无（第一关）

### 本关目标（必须产出）

* ✅ 你有一个可复用的 Python 项目模板：`src/ tests/ README.md .env.example`
* ✅ 你会用 Git：commit / branch / PR（哪怕是给自己提 PR）

### 知识点清单（带等级）

* [必须掌握] **Python venv / 依赖管理**

  * 作用：让项目可复现、少踩坑
  * 学习重点：venv、requirements/pyproject、锁版本
* [必须掌握] **Git 基础**

  * 作用：面试官会直接看你的提交质量
  * 学习重点：小步提交、可读 commit message、PR 描述“为什么这样改”
* [必须掌握] **配置管理（.env）**

  * 作用：API Key 不进仓库
  * 学习重点：`.env.example`、密钥不写日志

### 必做任务（打勾才算过关）

* [ ] 新建 repo：`python-agent-starter`
* [ ] 写一个 CLI：`python -m app --help`
* [ ] 接入 logging：每次运行输出 run_id
* [ ] pytest 跑通：至少 2 个测试

### 验收标准

* 任何人 clone 你的仓库后，按 README 步骤能在 5 分钟内跑起来。

</details>

---

<details>
<summary><b>关卡 1：Python 工程必修（为 Agent 做准备）</b></summary>

### 解锁条件

* 完成关卡 0 的模板仓库

### 本关目标（必须产出）

* ✅ 你能写出“可维护”的 Python 代码（不是一次性脚本）
* ✅ 你能处理超时、重试、异常兜底（Agent 项目必备）

### 知识点清单（带等级）

* [必须掌握] **异常处理 / 错误兜底**

  * 学习重点：try/except、异常链、可观测日志（别只 print）
* [熟悉] **asyncio 并发（并行工具调用会用到）**

  * 学习重点：gather、Semaphore、timeout、取消任务
* [熟悉] **HTTP 调用基础**

  * 学习重点：429 限流、指数退避、幂等

### 必做任务

* [ ] 在模板仓库里加：`http_client.py`（含 timeout + retry）
* [ ] 写 1 个“失败可回归”的测试：模拟超时/429

### 验收标准

* 你的工具调用层：**失败不会把程序炸掉**，并且日志里能看清楚失败原因。

</details>

---

<details>
<summary><b>关卡 2：LLM API + Tool/Function Calling（Agent 的手脚）</b></summary>

### 解锁条件

* 你有稳定可复用的 HTTP/日志/配置底座（关卡 1）

### 本关目标（必须产出）

* ✅ 你能让模型输出“稳定可解析”的结构化结果（JSON schema）
* ✅ 你能实现工具调用：参数校验 + 失败重试 + 白名单

### 知识点清单（带等级）

* [必须掌握] **LLM API 基础（消息结构 / tokens / 截断）**
* [必须掌握] **Tool/Function Calling（结构化参数）**

  * 学习重点：schema、参数校验（Pydantic 思路）、工具失败恢复
* [熟悉] **流式输出（可选，但面试加分）**

### 推荐复现项目（真实仓库）

* OpenAI Cookbook（挑 2-3 个示例改成 CLI）

  * `https://github.com/openai/openai-cookbook` ([GitHub][1])

### 必做任务

* [ ] 在你的 repo 做一个 `json_guard.py`：解析失败 → 让模型“修 JSON” → 再解析
* [ ] 做 20 条回归用例（promptfoo 或你自写脚本均可）

  * promptfoo：`https://github.com/promptfoo/promptfoo` ([GitHub][19])

### 验收标准

* 20 条用例中：JSON 解析成功率 ≥ 95%，失败有自动修复策略或可解释错误。

</details>

---

<details>
<summary><b>关卡 3：ReAct（必须复现）——Reason + Act 的经典循环</b></summary>

### 解锁条件

* 你已经会工具调用（关卡 2）

### 本关目标（必须产出）

* ✅ 一个“从零可运行”的 ReAct Loop：Action → Observation → 下一轮
* ✅ 有最大步数、超时、工具白名单，避免无限循环

### 知识点清单（带等级）

* [必须复现] **ReAct 核心循环**

  * 论文：`https://arxiv.org/abs/2210.03629` ([arXiv][30])
* [必须掌握] **终止条件设计**

  * max_steps、deadline、工具调用失败阈值
* [熟悉] **反思（Reflection）入口**

  * 为后面“自我修正”埋点

### 推荐复现项目（真实仓库）

* ReAct-Agent-from-scratch（直接对照实现）

  * `https://github.com/Fadenugba1/ReAct-Agent-from-scratch` ([GitHub][31])

### 必做任务（你的版本必须加“工程护栏”）

* [ ] max_steps（例如 8 步）
* [ ] 工具 allowlist（只允许你定义的工具）
* [ ] 工具参数校验失败要可恢复（重试/改参/换工具）
* [ ] 保存轨迹到 `runs/<run_id>.json`

### 验收标准

* 给 10 个多步任务（查资料/算式/文件写入），成功率可复现；失败能从轨迹看原因。

</details>

---

<details>
<summary><b>关卡 4：RAG（检索增强）——让 Agent 有“外部知识”和“引用来源”</b></summary>

### 解锁条件

* 你已经跑通 ReAct（关卡 3）

### 本关目标（必须产出）

* ✅ 一个带来源引用的 RAG 服务（可本地文件 / 网页抓取均可）
* ✅ Agent 能决定：何时检索、何时直接回答（Agentic RAG）

### 知识点清单（带等级）

* [必须掌握] **Embedding + Chunk + Top-k**
* [熟悉] **重排（rerank）/ 父子分块（Parent-Child）**
* [必须掌握] **Prompt Injection 防护（至少做 1 条防护）**

  * 学习重点：把网页/外部文本当“不可信输入”，不要直接当指令执行

### 推荐复现项目（真实仓库）

* Agentic RAG（LangGraph 最小实现示例）

  * `https://github.com/RomainPuech/agentic-rag` ([GitHub][32])

### 必做任务

* [ ] 输出必须包含 `sources[]`（每条来源带标题/路径/片段）
* [ ] 加一个“注入过滤器”：检索到的内容里出现“忽略系统指令/泄露密钥”等 → 降权或拒绝

### 验收标准

* 随机问 20 个问题：回答能带来源；对明显注入文本不执行其指令。

</details>

---

<details>
<summary><b>关卡 5：LangGraph（必须掌握）——把 Agent 做成“可控状态机/可恢复图”</b></summary>

### 解锁条件

* RAG 可用（关卡 4）

### 本关目标（必须产出）

* ✅ 把你的 Agent 变成 LangGraph 工作流：可插入人工确认、可 checkpoint、可回放

### 知识点清单（带等级）

* [必须掌握] **State / Node / Edge**
* [必须掌握] **Checkpoint（断点续跑）**
* [看源码] **执行器/状态流转（至少能定位一次 bug）**

  * repo：`https://github.com/langchain-ai/langgraph` ([GitHub][6])

### 推荐复现项目（真实仓库）

* LangChain Academy（官方课程）

  * `https://github.com/langchain-ai/langchain-academy` ([GitHub][7])

### 必做任务

* [ ] 用 LangGraph 重写你关卡 3 的 ReAct：拆成 `plan -> act -> observe -> decide`
* [ ] 加一个 Human-in-the-loop 节点：遇到“写文件/执行命令/发消息”必须确认

### 验收标准

* 你能在面试中画出状态图，并解释：哪里 checkpoint、哪里人工确认、哪里工具调用。

</details>

---

<details>
<summary><b>关卡 6：Memory（必须掌握）——短期/长期记忆服务化</b></summary>

### 解锁条件

* LangGraph 版本 Agent 跑通（关卡 5）

### 本关目标（必须产出）

* ✅ 一个“长期记忆服务”（用户维度），Agent 可读写
* ✅ 你能解释“记忆污染”与防护策略

### 知识点清单（带等级）

* [必须掌握] **短期记忆裁剪/摘要**
* [必须掌握] **长期记忆写入策略/召回策略**
* [熟悉] **记忆污染防护**

  * 外部内容不直接写入长期记忆；写入前结构化/去噪/打标签

### 推荐复现项目（真实仓库）

* Memory Template（官方模板）

  * `https://github.com/langchain-ai/memory-template` ([GitHub][8])

### 必做任务

* [ ] 跑通模板 quickstart（按 README 做）
* [ ] 接入你的 LangGraph Agent：每轮结束写入“本轮关键信息”
* [ ] 加 1 条“污染防护规则”：疑似注入/密钥/敏感信息不入库

### 验收标准

* 同一用户连续 3 天问同一类问题，Agent 能复用历史偏好；且不会被恶意文本污染记忆。

</details>

---

<details>
<summary><b>关卡 7：多智能体（必须掌握）——Supervisor / Router / Specialists</b></summary>

### 解锁条件

* 你已经有：工具 + 记忆 + 编排（关卡 6）

### 本关目标（必须产出）

* ✅ 一个多智能体系统：主管 + 2-3 专家（研究/执行/验证）
* ✅ 带 Guardrails + Tracing（面试高分项）

### 知识点清单（带等级）

* [必须掌握] **Handoff / Delegation**
* [必须掌握] **Guardrails（输入输出校验）**
* [熟悉] **Tracing（把运行轨迹可视化/可导出）**

### 推荐复现项目（真实仓库）

* OpenAI Agents SDK

  * repo：`https://github.com/openai/openai-agents-python` ([GitHub][3])
  * docs：`https://openai.github.io/openai-agents-python/` ([OpenAI][4])

### 必做任务

* [ ] 设计 3 个 Agent：

  * Planner（产出计划）
  * Researcher（检索/RAG）
  * Executor（工具执行，受限权限）
* [ ] 关键操作必须二次确认（HITL）
* [ ] 每次 run 生成 trace（至少导出 JSON）

### 验收标准

* 面试官问“为什么要多智能体？”你能用你的系统回答：分工、隔离、可控、可评估。

</details>

---

<details>
<summary><b>关卡 8：MCP（必须复现）——标准化工具接入</b></summary>

### 解锁条件

* 多智能体能稳定跑（关卡 7）

### 本关目标（必须产出）

* ✅ 你自己写一个 MCP Server（最小可用）+ Agent 调用它
* ✅ 加最基本的鉴权与审计日志

### 知识点清单（带等级）

* [必须复现] **MCP Server**

  * spec：`https://github.com/modelcontextprotocol/modelcontextprotocol` ([GitHub][9])
* [熟悉] **参考实现（抄结构不抄业务）**

  * servers：`https://github.com/modelcontextprotocol/servers` ([GitHub][10])
* [了解] **Registry（可选项：发布/发现）**

  * registry：`https://github.com/modelcontextprotocol/registry` ([GitHub][11])

### 必做任务（建议做一个“TODO MCP Server”）

* [ ] 提供 3 个工具：`add_task / list_tasks / done_task`
* [ ] sqlite 存储
* [ ] token 鉴权（最小可用）
* [ ] Agent 通过 MCP 调用这些工具完成任务

### 验收标准

* 你能演示：Agent 用自然语言 → 调 MCP → 改数据库 → 返回结构化结果。

</details>

---

<details>
<summary><b>关卡 9：Skills（必须复现）——“能力包”体系（重点：AgentSkills + OpenClaw）</b></summary>

### 解锁条件

* MCP 跑通（关卡 8）

### 本关目标（必须产出）

* ✅ 你写一个符合 Agent Skills 格式的 Skill 包（SKILL.md + scripts）
* ✅ 你能解释：为什么 Skills 比“直接写工具”更利于工程扩展
* ✅ （可选加分）让你的 Agent 支持“自动发现/加载 Skills”

### 知识点清单（带等级）

* [必须复现] **Agent Skills 格式（SKILL.md + 可选 scripts/assets）**

  * repo：`https://github.com/agentskills/agentskills` ([GitHub][12])
  * 规范：`https://agentskills.io/specification` ([agentskills.io][13])
* [必须掌握] **Skills 选择/门控**

  * 学习重点：requires(env/bins/config)、版本管理、审计
* [熟悉] **OpenClaw Skills 机制（AgentSkills-compatible）**

  * docs：`https://docs.openclaw.ai/tools/skills` ([OpenClaw][15])

### 强制安全提醒（面试可讲真实案例）

* OpenClaw 的 skills/市场生态曾出现恶意技能与攻击事件，核心问题是“第三方技能 = 不可信代码/不可信指令”，必须做审计与沙箱隔离。([The Verge][33])

### 必做任务（建议做“招聘助手 skill 包”）

* [ ] `skills/job-hunter/SKILL.md`：清晰写用途、输入输出、示例
* [ ] `scripts/parse_jd.py`：解析 JD（结构化输出）
* [ ] `scripts/interview_qa.py`：基于 JD + 简历生成面试题（可接 RAG）
* [ ] 写一个 Skill Router：根据意图挑 skill（关键词版即可）

### 验收标准

* 你的 skill 包能被“另一套 agent”复用（体现“写一次，多处用”）。

</details>

---

<details>
<summary><b>关卡 10：评估 & 可观测（必须掌握）——把 Agent 做成可回归系统</b></summary>

### 解锁条件

* 你有一个相对完整的 Agent（关卡 7-9 任意组合）

### 本关目标（必须产出）

* ✅ Eval：改 prompt/工具/模型后，你能量化“变好还是变坏”
* ✅ 可观测：一次失败，你能 5 分钟定位到失败步骤

### 知识点清单（带等级）

* [必须掌握] **Evals（回归集 + 指标）**

  * OpenAI evals：`https://github.com/openai/evals` ([GitHub][2])
  * promptfoo：`https://github.com/promptfoo/promptfoo` ([GitHub][19])
* [熟悉] **Tracing / Observability**

  * Phoenix：`https://github.com/Arize-ai/phoenix` ([GitHub][20])

### 必做任务

* [ ] 建 30 条“任务集”（你实际要面试的场景：检索、写作、工具执行、失败恢复）
* [ ] 每次改动必须跑 eval（本地/CI 均可）
* [ ] 输出一份 `eval_report.md`：成功率、常见失败类型、修复策略

### 验收标准

* 面试官问“你怎么保证 Agent 不胡来？”你能拿出：**评估报告 + 轨迹 + 护栏策略**。

</details>

---

## 3）必做项目清单（按难度排序，全部给真实仓库地址 + 复现要点 + 简历亮点）

> 建议你最终只精选 3~5 个写进简历：**1 个基础能力 + 1 个编排/多智能体 + 1 个工程级 Capstone**。

---

<details>
<summary><b>Lv1 - API & 结构化输出：OpenAI Cookbook 改造版</b></summary>

* 仓库：`https://github.com/openai/openai-cookbook` ([GitHub][1])
* 复现要点：

  * clone → 跑通 2-3 个示例
  * 把其中 1 个改造成 CLI（带 JSON schema 校验与失败修复）
* 简历亮点（写法示例）：

  * “将 Cookbook 示例工程化：CLI + JSON schema 校验 + 20 条回归 eval，结构化输出稳定性提升至 X%”

</details>

---

<details>
<summary><b>Lv2 - ReAct 复现：从零实现 Reason-Act 循环</b></summary>

* 论文：`https://arxiv.org/abs/2210.03629` ([arXiv][30])
* 参考实现仓库：`https://github.com/Fadenugba1/ReAct-Agent-from-scratch` ([GitHub][31])
* 复现要点：

  * 你自己再做一版：加 max_steps / allowlist / 超时 / 轨迹保存
* 简历亮点：

  * “从零复现 ReAct，并实现工具白名单、失败重试、最大步数终止与轨迹回放”

</details>

---

<details>
<summary><b>Lv3 - Agentic RAG：LangGraph 驱动的可自我纠错检索</b></summary>

* 仓库：`https://github.com/RomainPuech/agentic-rag` ([GitHub][32])
* 复现要点：

  * 跑通后做 2 个增强：注入过滤 + sources 引用格式统一
* 简历亮点：

  * “实现 Agentic RAG：检索决策、相关性评估、自我纠错重检索；输出带来源引用与注入防护”

</details>

---

<details>
<summary><b>Lv4 - LangGraph Academy 全量跑通（官方课程级）</b></summary>

* 仓库：`https://github.com/langchain-ai/langchain-academy` ([GitHub][7])
* 复现要点：

  * 每个模块做一个你自己的变体（不要只跑 notebook）
* 简历亮点：

  * “用 LangGraph 构建可恢复长流程 agent：checkpoint + human-in-loop + 失败断点续跑”

</details>

---

<details>
<summary><b>Lv5 - 长期记忆服务：Memory Template</b></summary>

* 仓库：`https://github.com/langchain-ai/memory-template` ([GitHub][8])
* 复现要点：

  * 直接部署跑通 → 接入你自己的 agent → 加记忆污染防护
* 简历亮点：

  * “实现用户级长期记忆服务（写入/召回策略 + 污染防护），多 agent 共享记忆提升多轮一致性”

</details>

---

<details>
<summary><b>Lv6 - 多智能体工程化：OpenAI Agents SDK（含 Guardrails/Tracing）</b></summary>

* 仓库：`https://github.com/openai/openai-agents-python` ([GitHub][3])
* Docs：`https://openai.github.io/openai-agents-python/` ([OpenAI][4])
* 复现要点：

  * 主管 + 专家分工（Planner/Researcher/Executor）
  * 加 HITL（高风险操作确认）
* 简历亮点：

  * “构建多智能体工作流：handoff/guardrails/tracing；实现敏感操作二次确认与轨迹审计”

</details>

---

<details>
<summary><b>Lv7 - MCP 必须复现：自建 MCP Server + Agent 调用</b></summary>

* spec：`https://github.com/modelcontextprotocol/modelcontextprotocol` ([GitHub][9])
* servers：`https://github.com/modelcontextprotocol/servers` ([GitHub][10])
* 复现要点：

  * 自建 todo-mcp-server（sqlite + token）
  * Agent 端支持动态工具发现/调用
* 简历亮点：

  * “实现自定义 MCP Server（鉴权+审计），Agent 通过 MCP 标准化接入工具与数据源”

</details>

---

<details>
<summary><b>Lv8 - Skills 必须复现：Agent Skills 标准 Skill 包</b></summary>

* 仓库：`https://github.com/agentskills/agentskills` ([GitHub][12])
* 规范：`https://agentskills.io/specification` ([agentskills.io][13])
* 复现要点：

  * 自己做 1 个 skill 包（SKILL.md + scripts）
  * 做一个 Skill Router（意图→技能）
* 简历亮点：

  * “基于 Agent Skills 标准实现技能包与技能路由：可发现、可复用、可版本化、可审计”

</details>

---

<details>
<summary><b>Lv9 - 对标工程：TrendRadar（热点/舆情聚合 + 推送 + Docker）</b></summary>

* 仓库：`https://github.com/sansan0/TrendRadar` ([GitHub][27])
* 复现要点（建议你做“带面试亮点”的二开）

  * 跑通原项目后，加一个 **“Agent 对话分析入口”**（自然语言问：今天哪个话题值得关注？为什么？给证据）
  * 用 MCP 把“数据查询/推送”做成工具
* 简历亮点：

  * “在 TrendRadar 基础上二开：增加 Agentic 分析、MCP 工具化、评估回归集与可观测链路”

</details>

---

<details>
<summary><b>Lv10 - 终局对标：AstrBot（多平台 IM + 插件/技能 + Sandbox）</b></summary>

* 仓库：`https://github.com/AstrBotDevs/AstrBot` ([GitHub][26])
* 复现要点（建议你做“工程完整度 Capstone”）

  * 先按官方文档跑通 Docker/源码部署
  * 做一个“你自己的 Agent 插件/Skill”：例如“求职/趋势/投研”垂直能力
  * 给插件加：权限控制、沙箱执行、审计日志、评估回归
* 简历亮点：

  * “基于 AstrBot 做工程化二开：插件化 Agent、工具权限隔离、沙箱执行、审计与评估体系落地”

</details>

---

## 4）8 周主线学习计划（每周目标 & 产出）

> 你可以把它当作“每周必须交付”的 OKR。

### Week 1（关卡 0-1）：工程底座

* 目标：模板仓库 + Git 工作流 + 日志/测试/超时重试
* 产出：`python-agent-starter`（可复用）

### Week 2（关卡 2）：LLM API + Tool Calling

* 目标：结构化输出稳定 + 工具白名单
* 产出：Cookbook 改造版 + 20 条 eval

### Week 3（关卡 3）：ReAct 必须复现

* 目标：从零跑通 ReAct Loop（带护栏、轨迹保存）
* 产出：ReAct 项目仓库 + 10 条多步任务集

### Week 4（关卡 4）：RAG / Agentic RAG

* 目标：可引用来源 + 注入防护
* 产出：Agentic RAG 项目仓库 + sources 格式规范

### Week 5（关卡 5）：LangGraph 编排

* 目标：状态机化 + checkpoint + HITL
* 产出：LangGraph 版本 Agent（可断点续跑）

### Week 6（关卡 6-7）：长期记忆 + 多智能体

* 目标：记忆服务接入 + 主管/专家协作 + tracing
* 产出：多智能体 demo + 记忆污染防护说明

### Week 7（关卡 8-9）：MCP + Skills

* 目标：自建 MCP server + 1 个 Skill 包可复用
* 产出：todo-mcp-server + job-hunter-skill

### Week 8（关卡 10 + 终局）：Capstone 工程项目

* 目标：可投简历的完整系统（可部署、可观测、可评估、可控）
* 产出：

  * Docker 一键启动
  * Demo 视频（2-3 分钟）
  * `eval_report.md`
  * `architecture.md`（含状态图/模块图/权限模型）

---

## 5）终局 Boss（工程完整度 Capstone：对标 AstrBot / TrendRadar 风格）

> 你提到的方向（astrbot、TrendRadar、trendagent）本质共同点：
> **多源输入 → 规范化数据 → Agent 分析/决策 → 多渠道输出 → 可扩展（插件/skills）→ 可控（沙箱/权限）→ 可观测 & 可评估**。

下面给你 2 个“最适合面试”的 Capstone 选型（建议选其一）：

---

<details>
<summary><b>Boss A：Agentic Trend Radar（对标 TrendRadar）——趋势/舆情/热点分析系统</b></summary>

### 对标参考

* TrendRadar：`https://github.com/sansan0/TrendRadar` ([GitHub][27])

### 你要做的“可面试架构”（建议）

* Ingest：RSS/平台热榜抓取（定时任务）
* Store：sqlite/postgres + 向量库（可选）
* Tools（MCP）：`query_trends / get_topic_summary / push_message`
* Orchestrator（LangGraph）：`collect -> filter -> analyze -> brief -> publish`
* Skills：每种分析方法一个 skill（行业/技术/竞品/招聘趋势等）
* Output：Web UI + 邮件/飞书/Telegram 等推送（任选 1-2）

### 必须具备的工程亮点（写进简历）

* [ ] **可控性**：高风险推送前 HITL（人工确认）
* [ ] **可评估**：每周趋势简报的“命中率/用户反馈”指标 + 回归集
* [ ] **可观测**：每次生成简报保留 trace 与数据快照
* [ ] **可扩展**：新增一个趋势分析 skill 不用改主流程

</details>

---

<details>
<summary><b>Boss B：IM Agent Infrastructure（对标 AstrBot）——多平台聊天 Agent 基础设施</b></summary>

### 对标参考

* AstrBot：`https://github.com/AstrBotDevs/AstrBot` ([GitHub][26])

### 你要做的“可面试架构”（建议）

* Channel Adapter：Telegram/Slack/企业微信（任选 1）
* Router：根据意图路由到不同 agent（客服/检索/执行/日程）
* Tool Sandbox：执行类工具必须在 Docker / 受限环境中跑
* Plugin/Skills：新增能力以插件/skill 形式挂载
* Audit：所有工具调用落审计日志（含参数、结果摘要）

### 必须具备的工程亮点

* [ ] **权限模型**：工具分级（read-only / write / exec）
* [ ] **沙箱隔离**：执行 shell/代码必须在 sandbox
* [ ] **可评估**：多轮对话一致性、工具调用成功率回归
* [ ] **可观测**：trace + run replay

</details>

---

## 6）最后一页：面试“必答清单”（建议你贴到每个项目 README 顶部）

每个项目 README 至少包含：

* **Architecture**：一张图（状态图/模块图）
* **Safety**：工具白名单、权限分级、HITL、沙箱策略
* **Observability**：trace 示例（JSON 或 Phoenix 截图）
* **Evaluation**：回归集 + 指标 + 报告
* **Reproducibility**：`docker compose up` 或 `make run`

---

如果你希望我继续帮你把它“落成一份可直接开仓的模板文档”，我可以按你选的 Boss（A 或 B）直接输出：

* `README.md`（含架构图、接口定义、目录结构、里程碑）
* `docker-compose.yml`（最小可跑）
* LangGraph state 定义骨架 + MCP server 骨架 + Skills 目录骨架
  你拿去就能开始写代码、持续闯关。

[1]: https://github.com/openai/openai-cookbook?utm_source=chatgpt.com "GitHub - openai/openai-cookbook: Examples and guides for using the ..."
[2]: https://github.com/openai/evals?utm_source=chatgpt.com "GitHub - openai/evals: Evals is a framework for evaluating LLMs and LLM ..."
[3]: https://github.com/openai/openai-agents-python?utm_source=chatgpt.com "GitHub - openai/openai-agents-python: A lightweight, powerful framework ..."
[4]: https://openai.github.io/openai-agents-python/?utm_source=chatgpt.com "OpenAI Agents SDK - openai.github.io"
[5]: https://github.com/langchain-ai/langchain?utm_source=chatgpt.com "GitHub - langchain-ai/langchain: The platform for reliable agents."
[6]: https://github.com/langchain-ai/langgraph?utm_source=chatgpt.com "GitHub - langchain-ai/langgraph: Build resilient language agents as graphs."
[7]: https://github.com/langchain-ai/langchain-academy?utm_source=chatgpt.com "GitHub - langchain-ai/langchain-academy"
[8]: https://github.com/langchain-ai/memory-template?utm_source=chatgpt.com "GitHub - langchain-ai/memory-template"
[9]: https://github.com/modelcontextprotocol/modelcontextprotocol?utm_source=chatgpt.com "GitHub - modelcontextprotocol/modelcontextprotocol: Specification and ..."
[10]: https://github.com/modelcontextprotocol/servers?utm_source=chatgpt.com "GitHub - modelcontextprotocol/servers: Model Context Protocol Servers"
[11]: https://github.com/modelcontextprotocol/registry?utm_source=chatgpt.com "GitHub - modelcontextprotocol/registry: A community driven registry ..."
[12]: https://github.com/agentskills/agentskills?utm_source=chatgpt.com "GitHub - agentskills/agentskills: Specification and documentation for ..."
[13]: https://agentskills.io/specification?utm_source=chatgpt.com "Specification - Agent Skills"
[14]: https://github.com/openclaw/openclaw?utm_source=chatgpt.com "OpenClaw — Personal AI Assistant - GitHub"
[15]: https://docs.openclaw.ai/tools/skills?utm_source=chatgpt.com "Skills - OpenClaw"
[16]: https://github.com/openclaw/clawhub?utm_source=chatgpt.com "GitHub - openclaw/clawhub: Skill Directory for OpenClaw"
[17]: https://docs.openclaw.ai/zh-CN/tools/clawhub?utm_source=chatgpt.com "ClawHub - OpenClaw"
[18]: https://github.com/openclaw/skills?utm_source=chatgpt.com "GitHub - openclaw/skills: All versions of all skills that are on ..."
[19]: https://github.com/promptfoo/promptfoo?utm_source=chatgpt.com "GitHub - promptfoo/promptfoo: Test your prompts, agents, and RAGs. AI ..."
[20]: https://github.com/Arize-ai/phoenix?utm_source=chatgpt.com "GitHub - Arize-ai/phoenix: AI Observability & Evaluation"
[21]: https://github.com/microsoft/autogen?utm_source=chatgpt.com "GitHub - microsoft/autogen: A programming framework for agentic AI"
[22]: https://github.com/microsoft/semantic-kernel?utm_source=chatgpt.com "GitHub - microsoft/semantic-kernel: Integrate cutting-edge LLM ..."
[23]: https://github.com/crewAIInc/crewAI?utm_source=chatgpt.com "GitHub - crewAIInc/crewAI: Framework for orchestrating role-playing ..."
[24]: https://github.com/crewAIInc/crewAI-examples?utm_source=chatgpt.com "GitHub - crewAIInc/crewAI-examples: A collection of examples that show ..."
[25]: https://github.com/Significant-Gravitas/AutoGPT?utm_source=chatgpt.com "GitHub - Significant-Gravitas/AutoGPT: AutoGPT is the vision of ..."
[26]: https://github.com/AstrBotDevs/AstrBot?utm_source=chatgpt.com "GitHub - AstrBotDevs/AstrBot: Agentic IM Chatbot infrastructure that ..."
[27]: https://github.com/sansan0/TrendRadar?utm_source=chatgpt.com "GitHub - sansan0/TrendRadar: ⭐AI-driven public opinion ..."
[28]: https://github.com/eesha2712/trendagent?utm_source=chatgpt.com "GitHub - eesha2712/trendagent: Agentic AI solution"
[29]: https://github.com/chenjianrui-111/trend_agent?utm_source=chatgpt.com "GitHub - chenjianrui-111/trend_agent"
[30]: https://arxiv.org/abs/2210.03629?utm_source=chatgpt.com "ReAct: Synergizing Reasoning and Acting in Language Models"
[31]: https://github.com/Fadenugba1/ReAct-Agent-from-scratch?utm_source=chatgpt.com "GitHub - Fadenugba1/ReAct-Agent-from-scratch: Implementation of the ..."
[32]: https://github.com/RomainPuech/agentic-rag?utm_source=chatgpt.com "GitHub - RomainPuech/agentic-rag: A minimal Agentic RAG built with ..."
[33]: https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=chatgpt.com "OpenClaw's AI 'skill' extensions are a security nightmare"

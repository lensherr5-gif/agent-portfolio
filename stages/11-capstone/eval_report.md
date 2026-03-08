# Capstone Eval Report

- Success Rate: 0.92
- Schema Valid Rate: 0.99
- Tool Success Rate: 0.96
- P95 Latency: 6.4s

## Failure Breakdown

- retrieval_miss: 4
- tool_timeout: 2
- policy_block: 1

## Improvement Plan

1. 增强检索重排降低 retrieval_miss。
2. 对慢工具增加缓存与并发隔离。
3. 扩充对抗样例并每次发布前自动回归。

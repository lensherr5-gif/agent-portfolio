# job-hunter

## Purpose

- 解析 JD 关键字段。
- 基于 JD 生成面试题清单。

## I/O

- input: `jd_text`
- output:
  - `parse_jd.py`: 结构化字段（role/skills/years/location）
  - `interview_qa.py`: 题目数组

## Version

- `v1.0.0`

## Risk

- `medium`（读写本地文本，无外部系统副作用）

## Example

```bash
python3 skills/job-hunter/scripts/parse_jd.py "Python backend engineer, 3+ years, Shanghai"
python3 skills/job-hunter/scripts/interview_qa.py "Python backend engineer, 3+ years, Shanghai"
```

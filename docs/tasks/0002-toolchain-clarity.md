# 0002 — 恢复以熟悉工具为主线的工作流说明

Status: In Review

## Objective

依据用户确认，明确 spine-kit 是 Product Spine / Grill with Docs / Trellis / Superpowers
组合的使用手册与接入包；读者能直接知道各阶段工具、输入输出和交接。

## Non-goals

不重新设计自动化脚本、不安装工具、不迁移业务项目、不引入新框架或声称独立审查完成。

## Acceptance / Evidence

- README 和 WORKFLOW 首先展示熟悉工具链。
- Trellis 明确贯穿任务执行；Superpowers 提供局部执行技能。
- 日常示例、工具清单、项目模板与接入指引一致。
- setup/版本/日志为接入配套；保留首版实现与已知限制。

## Validation plan

文档一致性检查；现有 19 项测试（含链接检查）回归。无新增自动化行为，无新增测试要求。

## Gate / Review

实现者自检 PASS：恢复熟悉工具链的阶段分工；保留范围/证据约束；无新执行框架或业务改动。
2026-10-20：19/19 回归测试通过（含 Markdown 链接），git diff --check 通过。
独立 Review 未执行，保持 In Review；不将文档修正称为真实项目试点通过。

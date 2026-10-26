# 0001 — spine-kit 首版

Status: Superseded（2026-10-20，由 0003 接替；以下保留当时范围和验证事实）

## Objective

把讨论后的优化工作流提炼成可被 Claude Code / Codex 适配到新旧项目的独立仓库。

## Non-goals

不修改来源业务项目；不安装全局插件；不做业务脚手架；不自建复杂 CLI/服务；不宣称已完成真实项目试点。

## Acceptance / Evidence

- 完整工作流与分层职责，不是来源业务项目规则的复制。
- Agent 接入协议包含版本、已有文件保护、setup 日志、完成与恢复。
- 提供工具安装分级、项目模板和可运行自动化。
- 自动化边界有临时项目测试；记录验证范围与未完成试点。

## Validation plan

python3 -m unittest discover -s tests -v；链接检查；人工审查 Gate 与文档一致性。

## Product Path Gate

实现者自检 PASS：强化接入与验证闭环；不含来源业务项目的领域规则；不安装额外工具或改动业务项目；19 项自动化测试通过。

独立 Review：未执行。真实业务项目试点：未执行。首版是可试用候选，不标为已通过完整流程的 Done。

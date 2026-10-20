# Changelog

## 0.1.1 — 2026-10-20

依据用户反馈纠正定位：以 Product Spine / Grill with Docs / Trellis / Superpowers 的阶段用法为主线；
明确 Trellis 贯穿任务、Superpowers 按需辅助执行；setup 自动化退回配套接入章节。
同步 README、工作流、分工、使用示例、安装清单与项目模板。脚本接口与配置 schema 不变。
升级：阅读定位修正，手动合并相关指引；已有 task 不搬迁，明确实际 Trellis 路径/能力。
本版本未新增自动编排或插件安装；独立 Review / 业务试点仍待完成。

## 0.1.0 — 2026-10-16

首个试用版本：整合产品主线、风险分级、单一任务来源、按需技能、独立 Review、证据验收和经验回流。
提供 Agent 接入协议、项目模板、工具清单、固定 vendor 快照、setup JSONL 日志和显式 finalize。
Python 标准库脚本支持 plan/apply/validate/verify/finalize；没有自动插件安装、自动升级或部署。
迁移：首次接入已有项目须先做只读 plan，保留既有文件，手动合并入口；详见 ADOPT.md。
验证范围与局限见 docs/validation.md。

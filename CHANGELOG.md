# Changelog

## 0.2.0 — 2026-10-20（接入方式不兼容调整）

改为 Agent 可读的工作流配置源：盘点、合并本地规则、核对、记录；无本仓库运行时依赖。
保留熟悉工具链、按需技能、风险裁剪与经验回流；新增文字适配记录模板和模板选择指引。
移除 setup/verify 脚本、JSON 配置模板、专用 CI 示例/仓库脚本测试 CI、旧运行器测试。
项目规则模板自包含；安装清单不再要求为 spine-kit 安装 Python。
0.1.x 使用方需先依 docs/maintenance.md 提取规则/命令/证据并替换引用，不能直接删除旧目录。
旧版测试结果仅是历史；当前验证见 docs/validation.md。

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

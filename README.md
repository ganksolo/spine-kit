# spine-kit

面向 **1–3 人 + Claude Code / Codex** 的可复用开发工作流。

这个仓库帮助新项目建立流程、帮助已有项目渐进调整流程。它提供产品约束、按风险分级的任务路径、技能分工、验证与 Review、跨会话接续和反馈回流。它不是业务项目模板，不生成业务功能，也不是必须全量安装的 Agent 框架。

**给读取本仓库的 Agent：先读 [ADOPT.md](ADOPT.md)。用户要求“接入工作流”时，只调整开发流程；不顺便重构业务代码，不安装外部服务，不把本仓库的维护任务复制进业务项目。**

## 从这里开始

- 接入新项目或已有项目：[ADOPT.md](ADOPT.md)
- 完整流程与任务分级：[WORKFLOW.md](WORKFLOW.md)
- 分层职责、工具边界：[docs/layers.md](docs/layers.md)
- 安装清单（全局 / 项目 / 可选）：[tools/INSTALL.md](tools/INSTALL.md)
- 自动化、setup 日志、完成条件：[docs/automation.md](docs/automation.md)
- 日常使用：[docs/playbook.md](docs/playbook.md)
- 升级与撤销：[docs/maintenance.md](docs/maintenance.md)
- 实践反馈：[feedback/README.md](feedback/README.md)

## 给另一个项目的启动提示

```text
请读取 https://github.com/ganksolo/spine-kit 的 README.md 和 ADOPT.md，
将指定的 tag 或 commit 对应工作流适配到当前项目。若未指定，先解析并记录实际 commit。
这是开发流程接入，不是业务功能重构。
先检查现有指引、任务系统、技术栈、检查命令和工作区状态，给出适配计划。
保留已有文件和任务事实，明确冲突；用 setup 日志记录步骤与版本。
接入后运行验证，报告完成项、未完成项、工具安装需求和接续方式。
不要把复制模板或安装插件称为 setup 完成。
```

Agent 有本地文件能力时应先将指定版本检出到独立目录；只有浏览能力时，可阅读和提出方案，但不能声称已经接入项目。离线可使用本地固定快照。

## 最小依赖与快速预览

基础工作流无需第三方 skills。自动化脚本仅使用 Python 3.10+ 标准库；Git 用于版本追踪。

```bash
python3 /path/to/spine-kit/scripts/setup.py plan --target /path/to/project
python3 /path/to/spine-kit/scripts/setup.py apply --target /path/to/project
```

`plan` 不写文件。`apply` 只创建缺失文件，保留已有文件并记录冲突；默认状态是 `needs-adaptation`。接下来按 ADOPT 补齐项目内容、现有指引入口和验证配置，再完成 setup。执行写入前应符合目标目录权限与用户授权。

每个业务项目保存 `.spine/manifest.json` 和仓库内的工作流快照，不依赖每次联网读取最新规则。setup 日志位于 `.spine/setup/`。版本与内容摘要均被记录。

## 第一版边界

提供可运行的 setup、结构验证、检查命令执行和完成记录；不自动安装 skills，不自动配置宿主 hooks，不自动 merge / push / deploy，不自动更新已接入项目。升级使用人工审查的差异合并。

0.1.0 是首个试用版本。脚本的临时项目测试不等于真实业务项目试点；试点情况见 [验证记录](docs/validation.md)。

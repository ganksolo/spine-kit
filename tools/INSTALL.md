# Skills 与 CLI 安装清单

核对日期：2026-10-16。以下是能力选择和安装入口，不保证任意宿主版本的命令相同。
spine-kit 不自带第三方 skills、不复制其源码；使用上游许可证和更新机制。
**基础流程无需额外 skill；选择一个任务管理中心，避免整套框架叠加。**

## 本机与项目的分工

| 项目 | 必需性 | 安装/配置位置 | 如何验证 |
|---|---|---|---|
| Claude Code 或 Codex | 至少一个，已有则复用 | 本机宿主；使用各自官方安装方式 | 实际可启动、能读取目标项目和执行允许的命令 |
| Git | 推荐；版本/分支追踪需要 | 本机 | `git --version`，项目 `git status` |
| Python 3.10+ | 使用本仓库自动化必需 | 本机/CI | `python3 --version` |
| 项目运行时与包管理器 | 依业务技术栈决定 | 本机/CI；依赖在项目 | 真实运行项目检查，不安装无关工具链 |
| spine-kit 规则/配置 | 必需 | 业务项目 `.spine/` 及入口文件 | `setup.py validate` + report + finalize |
| GitHub CLI (`gh`) | 可选，管理 PR/issue 时 | 本机 | `gh --version`；认证单独配置，不记 token |
| Matt Pocock skills | 推荐按需选 Grill / retro / handoff | 宿主插件或 skills 目录，二选一 | 宿主能发现技能；用无副作用小例验证；记录版本 |
| Superpowers | 可选，优先调试/完成验证/TDD | 宿主插件或 skills 目录 | 确认具体技能可触发，没有抢占任务控制器 |
| Trellis CLI | 可选，需要完整上下文注入时试验 | CLI 本机、集成配置项目 | `trellis --help`，核对实际生成/注入能力 |
| OpenSpec / Spec Kit | 可选替代任务/规格层 | CLI + 项目配置 | 先试验；不要并存另一套权威任务状态 |
| Compound Engineering | 可借理念，不要求安装 | 选择其完整流程时才装 | 避免与已有实现/Review 编排重叠 |

## 建议的三种配置

1. **Minimal（默认）**：宿主 Agent + Git + Python + 本仓库。内置对话澄清、独立新上下文 Review、手动短复盘。
2. **Assisted**：Minimal + 按需 Matt Grill/retro/handoff + Superpowers 调试/验证技能。明确覆盖规则与触发方式。
3. **Managed（试验）**：选定完整 Trellis 等管理工具，映射其 task/spec/journal，停用重复状态和控制器。

## 安装操作

仅安装选择的项目；现有安装先核对来源、版本、自定义修改与重复副本。基础 setup 不自动安装以下工具。

- Matt skills：官方 README 提供各宿主插件入口。Claude Code 示例为
  `claude plugin install mattpocock-skills@claude-plugins-official`；可编辑文件方式为
  `npx skills@latest add mattpocock/skills`（交互选择宿主/技能）。插件与复制版二选一。
  不假设已有复制文件会自动更新；插件更新行为也应按宿主设置实测。
- Superpowers：按 [上游安装说明](https://github.com/obra/superpowers) 选择 Claude/Codex 对应入口；
  全量安装前阅读 bootstrap 的自动触发规则。项目限制只使用局部技能时先测试是否生效，不承诺所有版本都可选择性禁用。
- Trellis：官方当前入口 `npm install -g @mindfoldhq/trellis@latest`，在试验项目执行 `trellis init`。
  正式使用应记录实际版本，可将 `@latest` 换为已核实版本；不要直接对已有项目无审查 init。
- OpenSpec / Spec Kit：本版本不推荐默认安装；按下方来源选择，仅在替换任务层的明确决策后配置。

如安装命令与宿主实际帮助不一致，以宿主当前文档为准并记录，不猜测。
不自动创建新的 GLOSSARY：项目已有 CONTEXT/术语表时映射既有路径。

## 安装验收账本（填写在项目 setup report 或任务中）

| 能力 | required/optional | installed/missing/unknown/not-selected | 来源/版本/范围 | 验证证据 | 后续动作 |
|---|---|---|---|---|---|

required 缺失会阻塞相应能力；optional 不选不阻塞 setup。只有明确依赖某可选技能时它才成为本项目 required。
将选择写入 `.spine/config.json` 的 tools。该字段记录选择，脚本不验证宿主内部安装状态，由 Agent 提供证据。

## 上游来源

- [Codex 项目指引](https://developers.openai.com/codex/guides/agents-md)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Claude Code memory](https://code.claude.com/docs/en/memory)
- [Matt Pocock skills](https://github.com/mattpocock/skills)
- [Superpowers](https://github.com/obra/superpowers)
- [Trellis](https://github.com/mindfold-ai/Trellis)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [Spec Kit](https://github.com/github/spec-kit)
- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin)

这些来源是能力/安装说明，不是不同框架优劣的基准测试。升级后用项目任务验证收益，不自动追随最新版。

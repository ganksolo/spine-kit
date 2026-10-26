# Skills 与 CLI 准备清单

spine-kit 本身无需安装，也不要求 Python、专用 CLI 或项目配置目录。Agent 读取规范后，将选择写入项目本地规则和[适配记录](../templates/adoption-record.md)。
默认组合是 Product Spine + Grill with Docs + Trellis + Superpowers 的按需执行技能；职责需要落实，工具按项目能力选择。

## 本机与项目各准备什么

| 能力/工具 | 何时需要 | 本机或宿主 | 项目内配置与验收 |
|---|---|---|---|
| Claude Code 或 Codex | 至少一种执行宿主 | 复用已有安装 | 能读取项目规则并执行允许的命令；记录实际验证范围 |
| Product Spine / Product Path Gate | 必需职责 | 无需安装 | 适配产品边界与验收检查表 |
| Git | 推荐，用于版本与差异 | 本机，`git --version` | 记录分支、来源 commit、实际变更；无 Git 如实注明 |
| Grill with Docs | 需求存在未知时 | Matt Pocock skills 的宿主支持安装方式 | 读取现有文档，只澄清未决问题，结果进入任务/已有决策记录 |
| Trellis CLI / 集成 | 可选增强；任务职责本身必需 | 全局 CLI 及依赖，安装须用户同意 | 按下方“Trellis 接入决策”选择 CLI 或手动模式；仅有目录不代表自动注入可用 |
| Superpowers | 实现、排错、完成验证时按需 | 宿主支持的插件或 skills 安装 | 核对具体技能可发现/调用，与已有任务体系不冲突 |
| 项目运行时、包管理器、测试工具 | 按业务技术栈 | 本机/CI | 复用真实检查命令，无业务代码时记录不适用 |
| retro / handoff | 有复盘或交接需求时 | 可选 Matt Pocock skills | 输出回到现有任务、Journal 或接续指针，不增加平行进度表 |
| GitHub CLI | 需要用 CLI 管理 PR/issue 时 | 可选，本机 | 核对可用性与授权范围；记录不含凭证 |
| OpenSpec / Spec Kit | 明确决定替换任务/规格层时 | 按上游准备 | 映射到唯一任务事实源；不是默认叠加安装 |
| Compound Engineering | 明确需要其完整工具时 | 可选 | 默认仅借经验回流方法，无需安装插件 |

## Trellis 接入决策

必需的是 Trellis 承担的**职责**：唯一任务源、任务上下文、完成前核对（Trellis Check）、收尾记录。
Trellis CLI 是实现这些职责的可选增强，不是适配的必需项。WORKFLOW 中“Trellis Check”“Trellis 收尾”指职责，两种模式都要执行。

### CLI 比手动模式多什么

以下依据上游 README（2026-10-26 读取，未在本仓库实测，实际安装前须重新核对）：
- 安装：全局 npm 包，需要 Node.js 与 Python；`init` 在项目中写入 `.trellis/`（spec、tasks、workspace/journal）、平台相关生成文件和 hooks；上游提供 dry-run 与卸载命令。
- 能力：在宿主支持且所需 hooks/权限已启用时，可在会话中自动或按需注入 spec；implement/check 根据宿主能力由子 Agent 或主会话执行并获得精选上下文；finish-work 负责归档已完成任务并更新 Journal。具体能力必须按所用宿主实测。
手动模式没有这些自动能力，靠入口文件引用和 Agent 按规则执行，规范过期的风险更高。

### 盘点

确认三件事并写入适配记录，分开记录“已安装”“项目已初始化”“实际能力已验证”：
- 本机是否有可执行的 Trellis CLI 及版本；
- 项目是否已有 Trellis 生成的目录、hooks 或宿主配置；
- 新会话是否真的注入了 spec（只能实测，不从目录推断）。

### 三种结果

| 情况 | Agent 做什么 | 适配状态 |
|---|---|---|
| CLI 已安装且项目已初始化 | 用最小安全案例实测注入/check/收尾中所选能力，再写入本地规则 | 实测通过可 complete；未实测写明 |
| 未安装，用户同意本次安装 | 先告诉用户：会安装哪些全局包与依赖、`init` 会写入哪些项目文件和 hooks、如何 dry-run 与撤销；读取上游当前说明后执行；不迁移已有任务，除非用户决定 | 安装并实测后可 complete |
| 未安装，用户选择手动或尚未表态 | 采用下方手动模式，不执行任何安装或 `init` | 用户明确选择手动：手动模式是认可替代，可 complete；未表态：partial，待用户决定 |

适配授权只覆盖本地规则文本。全局安装和会写入项目的 `trellis init` 都需要用户在本次对话中明确同意，不能由“适配流程”推定。

### 手动模式的最小约定

- 任务文件：沿用项目已有任务目录；没有时用 `docs/tasks/<id>-<slug>.md`，字段按任务模板。
  不手工创建 `.trellis/` 目录，以免被误认为 CLI 已接入，或与日后 `init` 冲突。
- 规范上下文：代替 spec 注入的规则文件必须由 AGENTS/CLAUDE 入口直接引用，开工时读取。
- Trellis Check：按任务的 Acceptance → Evidence 与项目 Gate 核对最终 diff 和检查结果，写入任务。
- 收尾：更新任务状态与 Closeout，向项目 Journal（已有位置，或如 `docs/journal.md`）追加简短记录，更新接续指针。
- 项目 WORKFLOW 写明“Trellis：手动模式”，以后改用 CLI 时按上表重新决策并迁移。

## 按需组合技能

- 需求不清：选择 Grill with Docs；明确需求可以跳过。
- 可测试的行为变更：按需选择 TDD；文案/格式等低风险修改不强制。
- 故障定位：选择 systematic-debugging。
- 进入 Review 或声称完成前（Standard/High-risk 必需）：使用 verification-before-completion 或写明的手动等效步骤，逐条填写验收证据；外部验证缺项注明原因与后续方式。
- 出现返工信号（因原验收未满足从 done 重开、独立 Review 第 3 轮仍有阻塞项、同类缺陷复发；需求变更重开不算）：必须做 retro，落实预防措施或写明不新增的具体理由；其他情况按需，允许没有新增经验。
- 需要交接：选择 handoff，结果写回已有接续位置。

安装整个技能包不代表每个任务都调用全部技能。检查包的自动触发行为是否与本地规则冲突；不能假定任意版本均支持按技能禁用。已有复制版与插件版先查重，避免不同版本同时生效。

## 准备与验收顺序

1. 先盘点已有宿主、技能、CLI、项目规则和来源版本；可用的直接复用。
2. 根据本次适配需要选能力，记录 required / optional / not-selected 及安装范围。
3. 实际安装时读取上游对应宿主的当前说明，核对依赖与命令；不把历史示例当作最新命令。不在适配过程中默认升级所有工具。
4. 会改写项目的初始化先查看行为与差异，合并既有规则；不覆盖原任务历史。
5. 分开记录“已安装”“宿主能发现”“实际调用已验证”。使用最小安全案例验证选中的能力，不以 README 声明代替结果。
6. 在适配记录中写清缺项、证据、替代方式和下一步。只读适配无需自动安装外部工具。

required 能力缺失且没有认可的替代方案时，相应接入保持 partial/blocked。optional 未选择不阻塞。
可按 WORKFLOW 手动执行相应职责；例如 Trellis 按上文“手动模式的最小约定”执行，不得宣称已启用 CLI 自动注入或自动收尾。
插件是否自动更新取决于宿主配置，必须实测；本仓库不承诺安装后自动追踪上游。

## 上游安装入口

以下提供入口，不对当前版本号、安装命令或宿主兼容性作未经验证的保证。实际安装时核验并记录。

- [Matt Pocock skills](https://github.com/mattpocock/skills)
- [Superpowers](https://github.com/obra/superpowers)
- [Trellis](https://github.com/mindfold-ai/Trellis)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [Spec Kit](https://github.com/github/spec-kit)
- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin)

这些入口不是框架效果的基准测试。升级后用真实任务观察收益，不自动追随最新版。

# spine-kit

**把 Product Spine、Grill with Docs、Trellis、Superpowers 组合起来的项目使用手册与接入包。**

面向一个人或 2–3 人，使用 Claude Code / Codex 开发。你继续使用熟悉的工具；本仓库说明每个工具何时使用、输入输出如何交接，以及怎样把实践经验带到下一个项目。

## 先记住这条主线

```text
Product Spine：确定项目主线
    ↓
Grill with Docs：澄清这次需求（有关键未知时）
    ↓
Trellis：创建任务，组织上下文并跟踪执行
    ↓
Claude Code / Codex + Superpowers：实现、调试、自检
    ↓
独立 Review：另一个上下文检查实现
    ↓
Trellis Check：核对任务验收与检查结果
    ↓
Product Path Gate：确认结果符合产品主线
    ↓
Trellis 收尾：更新任务、Journal，沉淀必要经验
```

**Trellis 贯穿任务执行；Superpowers 提供按需执行技能。** 不让两个工具各管一份任务或重复指挥执行。
Product Spine 在项目启动和方向变化时维护，不是每项任务都重新写。范围明确的小修复可以跳过 Grill，简记任务后直接修复验证。

## 怎么读

1. [WORKFLOW.md](WORKFLOW.md)：按阶段说明什么时候用哪个工具。
2. [工具分工与交接](docs/layers.md)：每层的输入、输出和职责边界。
3. [日常使用示例](docs/playbook.md)：从新项目、新功能、修 Bug 到 Review 和收尾。
4. [安装清单](tools/INSTALL.md)：哪些是文档、哪些技能/CLI 需要安装。

要将这套组合接入其他项目时，再读 [ADOPT.md](ADOPT.md)。版本、setup 日志和脚本属于接入配套，不是日常开发的新阶段。

## 给另一个项目的 Agent

```text
请读取 https://github.com/ganksolo/spine-kit 的 README.md、WORKFLOW.md 和 ADOPT.md。
把 Product Spine → Grill with Docs → Trellis → Superpowers 辅助实现 → 独立 Review
→ Trellis Check → Product Path Gate → Trellis 收尾这套组合适配到当前项目。
先盘点已有文件和工具，保留已有规则与任务；不要重构业务代码。
确认 Trellis 实际任务路径，避免生成第二套任务系统。
固定并记录读取的版本/commit；按 ADOPT 记录接入步骤、工具缺项、验证与未完成项。
```

没有某个工具时说明缺项和临时手动方式，不能声称已获得该工具的自动能力。
已有其他任务体系时先明确映射/迁移决定，不自动重写历史或安装第二套控制器。

## 配套接入能力

[自动化说明](docs/automation.md) 提供 plan/apply/validate/verify/finalize；仅用 Python 3.10+ 标准库。
脚本保留已有文件，记录来源版本与 setup 细节。它不安装 Trellis/skills，不会自动执行整条开发链。
项目保存固定工作流快照，不需要每次联网读取最新版本。只有浏览能力的 Agent 可以提出方案，不能声称已写入项目。

- [升级与撤销](docs/maintenance.md)
- [实践反馈回流](feedback/README.md)
- [验证记录与局限](docs/validation.md)

当前 0.1.1 修正首版的定位和表达；独立 Review、真实业务项目试点情况见验证记录。

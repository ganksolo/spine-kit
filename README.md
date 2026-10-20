# spine-kit

**供 Agent 读取并适配到项目内的工作流配置规范。** 面向一个人或 2–3 人，使用 Claude Code / Codex 开发。

你让 Agent 读取本仓库；Agent 理解工作流、检查目标项目，再生成或调整项目自己的 AGENTS.md、CLAUDE.md、WORKFLOW.md、任务和验收规则。日常开发遵循项目内的规则，无需运行 spine-kit，也无需持续联网读取本仓库。

## 我们沿用的工具链

```text
Product Spine：确定项目主线
    ↓
Grill with Docs：有关键未知时澄清当前需求
    ↓
Trellis：建立任务，组织上下文，贯穿执行与记录
    ↓
Claude Code / Codex + Superpowers：按任务实现、调试、自检
    ↓
独立 Review
    ↓
Trellis Check：核对任务验收与检查结果
    ↓
Product Path Gate：确认结果符合产品主线
    ↓
Trellis 收尾：更新任务/Journal，回流必要经验
```

Trellis 管任务；Superpowers 按需提供执行技能，不再建立另一份任务状态。
产品主线不必每个任务重写；明确的小修复可跳过 Grill；复盘允许零新增规则。

## 给目标项目 Agent 的指令

```text
请读取 https://github.com/ganksolo/spine-kit 的 README.md、WORKFLOW.md 和 ADOPT.md，
按其中规范适配当前项目的开发流程。
这是流程配置，不是业务代码重构。先检查已有规则、任务、技术栈和工具，保留有效约定，合并冲突并补齐缺项。
让项目自己的 AGENTS.md / CLAUDE.md 指向本地规则，日常工作不依赖 spine-kit 的程序或远程文档。
记录参考版本/实际 commit、适配过程、改动、验证、工具缺项和项目例外。
缺少关键产品决定时询问，不编造；最后报告适配是否完成以及未完成项。
```

先读取 [ADOPT.md](ADOPT.md) 执行。新项目建立最小必要规则；已有项目渐进合并，不能直接覆盖指引或搬迁全部历史。
本仓库不需要安装。使用哪些第三方 skills / CLI，由目标项目选择与验证；见 [安装清单](tools/INSTALL.md)。

## 阅读顺序

1. [WORKFLOW.md](WORKFLOW.md)：各工具在什么阶段使用。
2. [docs/layers.md](docs/layers.md)：工具分工、输入输出和交接。
3. [ADOPT.md](ADOPT.md)：Agent 如何将规范转成目标项目规则。
4. [docs/playbook.md](docs/playbook.md)：日常开发指令。

配套材料：
- [templates/README.md](templates/README.md)：选择、合并模板的方式，不要求全量复制。
- [适配记录模板](templates/adoption-record.md) 与 [示例](docs/setup-example.md)：版本、步骤、完成证据。
- [项目自动化建议](docs/automation.md)：复用项目检查、Trellis 和可选 CI/hooks。
- [维护与旧版迁移](docs/maintenance.md)：比较规范变化，按项目决定采用。
- [经验回流](feedback/README.md)：项目改进如何反馈本仓库。
- [验证范围](docs/validation.md)：区分文档检查和真实项目试点。

## 当前版本

0.2.0 将接入机制改为文字协议与模板，不再提供安装器、验证运行器或要求项目建立专用配置目录。
版本与 commit 用于追溯参考来源，不会自动替目标项目升级。0.1.x 已接入项目请先读迁移说明，不要直接删除旧文件。

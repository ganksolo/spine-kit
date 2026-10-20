# 模板选择说明

模板供 Agent 参考并合并到目标项目，不全量复制。先读 ADOPT，再选择缺失内容。
本目录的 `TODO` 是适配占位符，不是可直接使用的项目规则。

| 模板 | 何时使用 | 目标位置 |
|---|---|---|
| [project/PRODUCT_SPINE.md](project/PRODUCT_SPINE.md) | 产品边界缺失 | 项目已有产品主线位置，或根目录 |
| [project/AGENTS.md](project/AGENTS.md)、[project/CLAUDE.md](project/CLAUDE.md) | Agent 入口缺失/需补齐 | 合并现有入口，保留目录级规则 |
| [project/WORKFLOW.md](project/WORKFLOW.md) | 本地工具链规则缺失/需调整 | 项目已有工作流文件 |
| [project/gate.md](project/gate.md) | 验收检查不足 | 项目已有 Gate 或合适文档位置 |
| [project/context.md](project/context.md) | 确需短接续指针 | 优先用已有接续方式；不再建一份动态状态 |
| [task.md](task.md)、[quick-task.md](quick-task.md) | 需补任务字段 | 合并 Trellis 实际任务格式，不新建平行任务体系 |
| [adr.md](adr.md) | 重大稳定决策 | 项目既有 ADR 目录，普通任务不强制 |
| [retro.md](retro.md)、[feedback.md](feedback.md) | 有值得复用的教训 | 项目既有复盘记录/经授权的反馈 |
| [adoption-record.md](adoption-record.md) | 本轮流程适配开始 | 已有接入文档/流程任务，或 docs/workflow-adoption.md |

路径不是强制目录结构。生成文件时将入口、任务、Gate 和检查命令替换为项目真实值。
项目文件应自包含，不能只写“遵循 spine-kit”或必须跳到远端才能知道如何工作。
本仓库的 docs/tasks 是维护历史，不是业务项目需要复制的任务。

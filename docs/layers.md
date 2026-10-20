# 工具分工与阶段交接

这张表是 spine-kit 的核心：知道什么时候用哪个熟悉的工具，而非学习新的分层术语。

| 工具/环节 | 何时使用 | 输入 | 输出交给谁 |
|---|---|---|---|
| Product Spine | 项目启动或产品方向变化 | 用户问题、已有产品资料 | 产品目标、核心路径、non-goals → 所有后续环节 |
| Grill with Docs | 当前需求有重要未知或冲突 | Spine、相关文档和代码、需求 | 确认的范围/取舍/验收 → Trellis；稳定决策写 CONTEXT/必要 ADR |
| Trellis | 需求明确后至任务结束 | 已确认需求和项目规范 | 当前 task、实施上下文、状态 → 实现者和审查者 |
| Superpowers + 实现 Agent | 实现、出现 Bug、准备提交审查时 | 当前 Trellis task 和相关规范 | 代码、测试、自检证据 → 独立 Review |
| 独立 Review | 实现并自检后 | task、diff、契约、测试证据 | 阻塞项/建议 → 实现者修复；审查结论 → Trellis Check |
| Trellis Check | Review 修复完成后 | 最终 diff、task、审查记录 | 验收覆盖、检查结果、缺项 → Product Path Gate |
| Product Path Gate | 标记任务完成前 | Spine、验收结果、剩余风险 | PASS/FAIL/NOT-READY → Trellis 收尾 |
| Trellis 收尾 | 任务完成或会话中断 | 实际状态、证据、下一步 | task / Journal / 接续指针；通用经验反馈 spine-kit |

## Trellis 管执行记录，Superpowers 帮助执行

Trellis 负责 task、上下文、check 和 journal，不自行决定产品方向。
Superpowers 按需提供 `test-driven-development`、`systematic-debugging`、`verification-before-completion` 等执行纪律。
不要在已有 Trellis task 之外让 Superpowers 再维护一份同义任务状态。
它的完整计划/子代理执行模式不默认开启；如果项目明确选择，需指定谁拥有任务状态、执行控制和收尾。

需求澄清默认使用 Grill with Docs，已有结论不重复跑 Superpowers brainstorming。
Product Spine 是文档；Product Path Gate 是检查表；它们不需要安装 CLI。
Trellis 目录/手动模板不等于完整 Trellis CLI 与自动注入能力。实际安装与集成必须验证。

## 角色和扩展

可以保留 Claude Code 实现、Codex Review 的习惯，也可以互换；独立上下文不可由实现者自查冒充。
默认一个实现会话；有独立子任务和明确收益才并行，不因团队有 2–3 人就引入复杂代理团队。
`retro` / `handoff` 可辅助 Trellis 收尾，产物回到已有记录，不能新建另一份“最新进度”。
OpenSpec / Spec Kit 不在默认链路中；已有项目使用它们时先决定任务层映射/替换，不默认叠加。
Compound Engineering 借鉴经验回流，无需为复盘额外安装整套框架。

## 用户在哪些地方参与

确定产品方向；回答会改变产物的关键问题；判断验收结果是否有用；决定需要其授权的发布/不可逆动作。
常规实现、自检和记录由 Agent 在授权范围内推进，不要求用户手动指挥每个步骤。

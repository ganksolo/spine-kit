# 用熟悉的工具推进工作

以下是可直接交给 Agent 的自然语言指令，不假设不同版本的 slash command 完全一致。

## 1. 新项目开始

先确定 Product Spine，再做首个需求的 Grill with Docs，再由 Trellis 创建任务。

> 阅读已有资料，帮助我确认 Product Spine。已有答案不要重复询问。随后用 Grill with Docs
> 澄清首个功能的范围、non-goals 和验收条件；确认后交给 Trellis 建立任务，先不要实现。

完全没有资料时先访谈想法，得到最小 Product Spine，不强制生成大型 PRD。
安装/接入只需按 ADOPT 做一次；业务需求变化才更新相应文件。

## 2. 开发普通功能

> 用 Grill with Docs 阅读 Product Spine 和相关代码，只澄清这个需求尚未解决的问题。
> 将结果整理为当前 Trellis task：目标、不做什么、验收证据、验证方式。
> 按这个 task 实现，按需使用 Superpowers 的 TDD 和调试技能。
> 交 Review 前用 verification-before-completion 实际运行验证，逐条填写 Acceptance → Evidence；
> 本地能跑的检查必须跑通，已知失败先修；只能事后或在外部环境验证的条目写明原因和后续验证方式。
> 然后准备 task、diff 和证据供独立 Review；外部验证补齐前不标 done。

明确的需求直接从 Trellis task 开始，不必补一次访谈仪式。

## 3. 修一个范围明确的小 Bug

> 在 Trellis 当前任务或简短修复记录中写明症状和预期。
> 按 Superpowers systematic-debugging 的纪律先复现、取证、定位，再修复并验证。
> 能稳定复现时补回归测试；检查是否影响契约或生产，影响扩大时升级流程。

小修复可以省略完整 Grill/设计文档；独立 Review 可按风险省略并说明理由。

## 4. 独立 Review

在另一个会话、另一 Agent 或另一人处执行：

> 读取 Product Spine、当前 Trellis task 和相关契约，独立审查这份 diff（包括未提交新文件）。
> 检查任务匹配、隐藏扩张、错误路径、数据/API 合约和验收遗漏。
> 每项发现提供条件、影响、证据；区分阻塞项和建议。不要只复述实现者总结。

## 5. 检查与收尾

> Review 修复后运行 Trellis Check：核对最终 diff、验收条款、项目检查与已有证据。
> 再运行 Product Path Gate。缺少真实验证就保留 awaiting-validation，不标 Done。
> 通过后由 Trellis 更新任务和 Journal，记录合并/上线状态以及必要经验。

Trellis Check 不需要无变化地重跑所有检查，但需确认结果对应当前代码。

## 6. 换会话与复盘

> 从 Trellis 当前任务、接续指针和实际 Git 状态接续；不要从过时摘要猜测进度。
> 结束前更新现有接续位置，必要时用 handoff 辅助，不另建平行状态文档。

> 检查本任务是否有返工信号（因原验收未满足从 done 重开、独立 Review 第 3 轮仍有阻塞项、同类缺陷复发；需求变更重开不算）。有的话做 retro，
> 把预防措施写进测试/CI、Gate 或入口引用的规则，并在任务 Closeout 记录位置；不新增就写明理由。

没有返工信号时复盘可选，允许零新增规则。
通用经验脱敏后反馈 spine-kit，项目特例留在项目。

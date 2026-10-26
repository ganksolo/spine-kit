# 项目开发工作流

## 本地规则位置

- Product Spine：TODO
- Trellis 模式：CLI（版本、已验证能力）/ 手动模式（用户是否明确选择）：TODO
- Trellis 当前任务/任务创建、检查与收尾位置：TODO
- Journal / 接续方式：TODO
- Product Path Gate：TODO
- 技术栈与工作目录：TODO
- 开发分支/worktree、生产与发布边界：TODO

## 阶段与交接

1. **Product Spine**：项目启动或方向变化时确认目标、用户路径、non-goals，不每个任务重写。
2. **Grill with Docs**：当前需求存在关键未知时读取文档/代码并澄清，输出确认的范围、决策和验收条件。
3. **Trellis**：建立当前任务，至少包含 objective、non-goals、验收证据、验证计划；组织上下文并跟踪状态。
4. **实现 + Superpowers**：按任务实现；可测试行为按需 TDD，故障先复现与系统化调试。
   进入 Review 前（Standard/High-risk 必需）用 verification-before-completion 或手动等效步骤实际运行检查，逐条填写 Acceptance → Evidence；本地可运行的检查必须通过，外部验证缺项注明原因和后续方式后可交 Review，补齐前不标 Done。
5. **独立 Review**：交接任务、diff 范围、契约和证据到独立上下文；修复阻塞问题，不把建议自动扩成新需求。
6. **Trellis Check**：核对最终 diff、验收覆盖、项目规范和命令结果；已有有效证据可复用，缺项如实记录。
7. **Product Path Gate**：检查用户价值、产品边界、真实交接与剩余风险；新增能力须关联需求、问题证据或待验证假设，超出范围先经用户确认并更新验收；未满足条件不标 Done。
8. **Trellis 收尾**：更新任务/Journal/接续指针；发布按授权单独决定。
   出现返工信号（因原验收未满足从 done 重开、独立 Review 第 3 轮仍有阻塞项、同类缺陷复发；需求变更重开不算）时必须 retro，并把预防措施写进测试/CI、Gate、入口直接引用的规则或已启用的 Trellis spec，或写明不新增理由；只写 Journal 不算落实。
   回流规则存放位置：TODO（填入口文件实际引用的位置）

## 按风险裁剪

- Quick：明确、局部可逆、无契约/生产影响的小修复，简记任务 → 修复 → 验证 → diff 自查；可省独立 Review并写明原因。
- Standard：普通功能，任务 → 实现与自检 → 独立 Review → Check/Gate → 收尾。
- High-risk：架构、数据契约、鉴权、迁移、生产调度或高不确定性，额外澄清、必要 ADR、失败/恢复方案和真实验证。

## 项目检查与技能选择

实际检查命令、成功条件、工作目录、已有基线问题：TODO
所选技能/CLI 的触发条件、已验证能力、缺项和手动替代：TODO
实现者/独立审查者偏好（不必绑定品牌）：TODO
项目例外及原因（无则写无）：TODO

Trellis 是唯一任务状态来源；不让技能再次建平行任务。自动触发未验证则如实说明。
不同项目特例不自动升级为通用规则；有共性的问题经脱敏并获授权后反馈规范仓库。

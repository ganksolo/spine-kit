# 项目 Agent 入口

先读 `.spine/config.json` 指定的产品主线、工作流、接续指针和当前任务。
通用规则快照在 `.spine/vendor/WORKFLOW.md`；项目特定约束以本项目文件为准。
- 先核实实际 Git 状态与任务范围，保留用户未提交改动。
- 一个任务状态来源；按风险选择 Quick / Standard / High-risk。
- 授权范围内持续推进；缺少关键产品决定时才澄清。
- 完成声明对应实际证据；Standard/High-risk 需要独立 Review。
- 本项目具体命令见 `.spine/config.json`；执行前检查外部副作用。
- 接续时不要把旧摘要当事实，按任务、代码与证据确认。

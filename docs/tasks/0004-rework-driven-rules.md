# 0004 — 把自检、回流和扩张约束改为可触发的规则

Status: done（范围：规范文本；真实项目效果待试点观察）
Delivery: merged=yes（2026-10-20，ganksolo/spine-kit#1）；released=不适用

## Objective

依据对一个已使用该工作流项目的外部分析（review 轮次多、标 Done 后被打回、教训只记在 Journal、文档过期），
把三条原则改为有触发条件、可检查的规则：完成前自检门槛、返工信号触发强制回流、有依据且经确认的扩张规则。

## Non-goals

不处理文档体积预算、上游 GLOSSARY/to-tickets 映射、Trellis CLI 默认地位（已由 [0005](0005-trellis-adoption-decision.md) 处理）；
不安装工具、不修改使用方项目，不把文字走查当作真实试点。

## Acceptance / Evidence

- WORKFLOW §4 写明 Standard/High-risk 自检门槛：逐条记录证据、本地检查必须运行、已知失败不能改记为待验证、外部验证缺项注明后可交 Review 但不标 done。
- WORKFLOW §6 定义三种返工信号、强制 retro、预防措施落点（开工必读/自动执行）及“只写 Journal 不算”。
- WORKFLOW §5 与 Spine/Gate 模板包含扩张规则。
- layers、playbook、INSTALL、项目模板（AGENTS、WORKFLOW、PRODUCT_SPINE、gate、task、quick-task、retro）一致。
- VERSION 0.3.0、CHANGELOG、迁移说明已更新。

## Validation plan

相对链接检查；新规则关键词在活跃文档中一致出现的扫描；git diff --check；按典型“标 Done 后被打回”场景文字走查。

## Gate / Review

2026-10-20 用户 Review：指出自检门槛在主规范与模板冲突、扩张规则过窄、返工信号定义不一致且误含首轮 Review。已按建议统一（扩张规则额外要求假设写明验证方式、超范围由用户确认）。

实现者自查结果见 [验证记录](../validation.md)。独立 Review：由用户完成上述一轮，修正后用户确认提交并合并 PR #1。
独立 Agent Review 与真实项目试点未执行；规则能否减少返工需在使用方项目中观察。

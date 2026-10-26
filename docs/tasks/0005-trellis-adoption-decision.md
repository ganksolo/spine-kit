# 0005 — 明确 Trellis CLI 是否安装及手动模式

Status: In Review

## Objective

用户指出：文档虽说明“手搓目录 ≠ CLI”，但没有说明谁决定安装、何时问用户、不装时手动模式怎么做，
不同 Agent 适配时可能擅自运行初始化，也可能自造 `.trellis/`。本任务给出可执行的接入决策。

## Non-goals

不安装或运行 Trellis CLI，不写死上游安装命令，不迁移任何使用方项目，不处理文档体积预算与 GLOSSARY/to-tickets 映射。

## Acceptance / Evidence

- INSTALL 明确：职责必需、CLI 可选；CLI 多出的能力；盘点项；三种结果与适配状态；手动模式最小约定。
- ADOPT 明确全局安装与 `trellis init` 需用户在本次对话同意，未表态时手动模式且 partial。
- WORKFLOW、layers、项目 WORKFLOW 模板、适配记录模板与示例引用同一决策，无冲突表述。
- VERSION 0.4.0、CHANGELOG、迁移说明、验证记录已更新。

## Validation plan

相对链接与锚点检查；`git diff --check`；按“未装/同意安装/选择手动/已装”四种情况文字走查。

## Gate / Review

实现者自查见 [验证记录](../validation.md)。上游能力描述未经实际安装验证。独立 Review 与真实项目试点未执行，不标 Done。

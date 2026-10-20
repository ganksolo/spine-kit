# 适配记录示例

以下为说明性示例，不是真实项目执行结果。记录放在项目已有流程任务/接入文档中即可。

## 已有项目：沿用 Trellis

```text
参考：spine-kit 0.2.0；实际 commit=<读取时核实的 SHA>
目标：保留现有任务和技术栈，合并按需技能与验收规则。
状态：partial

规则映射：
- 产品主线：PRODUCT_SPINE.md
- 工作流：WORKFLOW.md
- 当前任务：沿用实际 Trellis task 路径（已核实）
- 检查：沿用 package.json 中已存在的 type-check / test 命令

步骤：
1. 读取已有 AGENTS/CLAUDE/Trellis 记录；记录未提交修改，未改动它们。
2. 合并 WORKFLOW：明确 Grill 使用条件、Superpowers 执行边界。
3. AGENTS 与 CLAUDE 已指向本地规则；链接核对通过。
4. Superpowers 技能可用性尚未核实；暂未决定手动替代，记为待处理。

下一步：核实必需能力或确认手动替代，再走查一个需求到验收的路径。
未做：业务代码修改、生产调用、独立新会话试用。
```

## 新项目：尚无业务代码

```text
参考：spine-kit 0.2.0；实际 commit=<读取时核实的 SHA>
状态：complete（仅指已约定范围的规则适配）
产品目标与边界已由用户确认并写入 Product Spine。
项目入口、本地工作流、任务约定与 Gate 已建立，路径核对和文本场景走查通过。
Trellis CLI 尚未安装：用户明确采用手动任务约定，未宣称自动注入能力。
Grill / Superpowers 尚未安装：以已记录的人工步骤替代；安装为后续可选增强。
尚无业务代码：测试命令不适用；首个实现任务负责配置技术栈检查。
未验证：技能自动触发、真实应用运行、新会话自动遵循效果。
```

complete 必须以实际核对和已明确的替代方式为依据，不能用这段示例文字代替执行。
模板见 [adoption-record.md](../templates/adoption-record.md)。

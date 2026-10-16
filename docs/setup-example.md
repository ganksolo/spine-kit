# 接入报告示例（说明性，非真实运行结果）

业务项目接入结束时，Agent 输出类似：

```text
来源：spine-kit 0.1.0，commit=<实际 SHA>，bundle=<实际摘要>
状态：needs-adaptation
已完成：固定规则快照；沿用 .trellis/tasks；保留原有 AGENTS.md。
未完成：AGENTS.md 尚未合并入口；真实测试命令尚未配置。
工具：Python/Git 已验证；Grill optional 未选择；不需要先安装完整 Trellis。
日志：.spine/setup/<实际 run-id>.jsonl
下一步：合并入口与配置检查 → validate → verify → 填写 report → finalize。
业务改动/部署：无。
```

示例 JSONL 事件（脚本实际输出含 UTC 时间与 run_id）：

```json
{"event":"apply-start","version":"0.1.0","bundle":"<hash>"}
{"event":"file-planned","path":"AGENTS.md","action":"preserve","sha256":"<candidate-hash>"}
{"event":"file-result","path":"AGENTS.md","action":"preserve","sha256":"<candidate-hash>"}
{"event":"apply-finished","status":"needs-adaptation"}
```

日志中的 preserve hash 是候选模板 hash，不代表原有文件已合并。Agent 必须核对实际内容。
finalize 完成后，报告应列出 skip 的检查及原因，不把“工作流就绪”说成“业务已验证”。

## 已有 Trellis 项目配置

从 templates/config.json 复制配置，只把 task_source 改为：

```json
{"kind":"local","location":".trellis/tasks"}
```

其余 paths 映射现有 Product Spine、工作流和接续位置；现有内容不会自动替换。
CLI 是否安装是另一件事，不能从 `.trellis/tasks` 目录存在推断。

## 工具版本记录建议

在 report 的 tool_inventory 记录 name、required、status、version、scope、evidence。
无法查证填写 unknown；必需能力缺失则 tools 项不能标 passed。选择 built-in 能力时无需安装同名 skill。

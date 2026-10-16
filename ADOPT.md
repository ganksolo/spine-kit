# Agent 接入协议

## 任务性质与授权范围

你正在将 spine-kit 的开发工作流适配到一个业务项目。你不是实现业务需求，也不是重写整个项目。
用户要求接入即授权必要的本地流程文件修改；遵循宿主文件权限。工具安装、外部写入、merge、部署仅在相应授权范围内执行。
不能因目录名像 Trellis 就认定 CLI 已安装，不能因模板存在就认定 setup 已完成。

## 先读取

1. 本仓库 README、WORKFLOW、docs/layers、tools/INSTALL。
2. 目标项目 AGENTS/CLAUDE/WORKFLOW、产品目标、相关 ADR、任务入口、包管理与 CI。
3. 实际 Git 分支、未提交修改、是否存在生产 checkout/自动任务；不读取或记录密钥正文。
4. 已安装 skills/CLI 和既有 workflow，能查则查；不能查的标 `unknown`。

## 执行顺序

### A. 盘点与版本定位

使用明确 tag/commit 的本地检出。记录 VERSION、Git commit（如果可用）和 bundle 内容摘要。
若源工作区有未提交改动，manifest 会记录 dirty；试验可用，正式复用应使用已提交版本。
阅读目标配置；已有 `.spine` 时先判断继续接入或升级，不把已有项目当空目录处理。

### B. 适配计划

确认项目类型、任务事实源、规范路径、角色偏好、检查命令、可选 skills、触及生产的边界。
默认模板路径可由 JSON 配置覆盖。已有 `.trellis/tasks` 或 issue 时映射过去，不搬历史。
复制 `templates/config.json` 到临时位置并按需修改，使用 `--config /path/to/config.json`。
任务类型 `local` 需要 task_root；`external` 需要 location（真实 issue 项目地址）；禁止创建第二个状态账本。

```bash
python3 /path/to/spine-kit/scripts/setup.py plan --target /path/to/project --config /path/to/config.json
```

plan 只输出将创建/保留的路径，不写目标；冲突说明附在任务或 setup 报告中。
简单可逆适配在授权内直接推进；产品边界不明或既有规则冲突时，只询问影响行为的具体决策。

### C. Apply 与手动适配

```bash
python3 /path/to/spine-kit/scripts/setup.py apply --target /path/to/project --config /path/to/config.json
```

脚本只创建缺失文件；已有不同内容会保留并记日志。已有 AGENTS/CLAUDE 须手动合并简短入口，
不要整份替换；候选内容来自 templates/project。配置接入后在 `.spine/config.json` 维护。
填写 Product Spine、项目 Gate、检查命令和当前任务指针。把任何不适用检查写明原因。
模板中的 `TODO` 不是有效项目决策，关键文件未填写不得完成。

### D. 验证

```bash
python3 /path/to/project/.spine/vendor/scripts/setup.py validate --target /path/to/project
python3 /path/to/project/.spine/vendor/scripts/verify.py --target /path/to/project
```

validate 检查结构、引用、占位符与快照完整性；verify 运行配置中的命令，默认不运行任何猜测的命令。
先审查命令再执行，不默认调用真实 agent、数据库迁移、生产接口或发送消息。
已有项目记录基线失败，不能修改测试来制造绿色；未通过时保留 `needs-adaptation`，解决或明确调整范围后再验证。
新项目尚无代码时允许检查项标 skip，必须写具体理由；这表示“工作流就绪、业务检查未建立”。

### E. 完成报告

填写 `.spine/setup/report.json`：每项状态与具体证据，人工判断和机器检查分开。
确认两种入口能找到规则、任务事实源只有一个、工具缺项有说明、已有文件已保留/合并、恢复方式明确。

```bash
python3 /path/to/project/.spine/vendor/scripts/setup.py finalize --target /path/to/project
```

finalize 再验证结构，要求 report 所有项 passed 且证据非空，要求 verify 结果对应当前配置和工作区指纹。
它记录 `complete`，不自动 commit，不代表业务代码完成、独立 Review 通过或已经上线。
Agent 必须报告：版本/摘要、setup 状态、日志路径、改动、跳过项、安装需求、未完成项和下一步。
项目指引和脱敏后的 setup 记录应进 Git；临时敏感输出不得提交。

## 中断恢复

查看 `.spine/setup/*.jsonl` 和 manifest；最后一次 apply 没结束时先核实已经写入的文件。
同一 source bundle 重跑 apply，只补缺失文件，保留已有修改，每次新建日志，不擦除旧记录。
不会自动撤销用户修改；依据 docs/maintenance 的 hash/Git 差异选择恢复。
不同 bundle 重跑会拒绝；升级走三方比较，不用 apply 覆盖。

## 只读或无脚本环境

可手动适配模板，但必须记录来源版本、改动和未运行检查，状态保持 `needs-adaptation`。
没有执行日志、检查输出或目标文件写入证据时，明确报告“方案已准备，接入未完成”。

# 自动化与 setup 日志

## 已实现的自动化

- `setup.py plan`：只读盘点目标路径和待创建文件。
- `setup.py apply`：复制固定工作流快照与缺失模板；保留冲突；写版本、摘要与逐步 JSONL 日志。
- `setup.py validate`：检查 manifest、配置、项目入口、关键模板填充和 vendor 完整性。
- `verify.py`：按显式配置执行 argv 命令（无 shell），记录成功/失败/跳过/超时与工作区指纹。
- `setup.py finalize`：结构检查 + Agent 报告 + 当前版本检查证据，才更新 setup 完成状态。

不自动安装插件、注册 hooks、调用云 API、推送 Git、部署或改写业务代码。

接入输出示例见 [setup-example.md](setup-example.md)。

## 文件约定

| 路径 | 用途 |
|---|---|
| `.spine/manifest.json` | schema、来源 URL、版本、Git commit/dirty、bundle hash、vendor hashes、setup 状态 |
| `.spine/config.json` | 项目路径映射、任务 adapter、机器检查命令与工具选择 |
| `.spine/vendor/` | 固定规则与脚本快照；不直接编辑，升级时三方比较 |
| `.spine/setup/<run-id>.jsonl` | UTC 时间、run id、动作、相对文件路径、hash、结果；保留中断过程 |
| `.spine/setup/report.json` | Agent 对适配完成条件的具名声明和证据；不是独立机器证明 |
| `.spine/setup/verification.json` | 最近一次检查结果；旧执行摘要也追加到 JSONL |

日志默认只含路径、hash 和状态，不含文件正文、密钥、远程请求或命令输出；人工填写 evidence 时也须脱敏。
检查子进程 stdout/stderr 只在当前终端显示，不持久保存。需要保存业务证据时由项目另行选择脱敏文件。
绝不能把 token 写进 argv/config；使用环境变量或宿主凭据系统。

`complete` 的含义是“该配置的工作流接入完成”；不代表插件都安装、所有业务检查可用或产品已经完成。
新项目检查可 skip，但必须有具体理由；finalize 输出会保留这些限制。
完成后改动配置/指引需重新 validate/verify/finalize，manifest 记录的是当时完成事实，不是永远有效。

## 检查配置

每项含 `name`，再二选一：`argv` 字符串数组，或 `skip_reason` 非空原因。
可配置 `timeout_seconds`（1–3600，默认 120）。命令在项目根目录运行。
例如 Node 项目可用 `["npm", "run", "type-check"]` 和 `["npm", "test"]`；Python 项目按实际工具配置。
检查应非交互、有限时、可重复，不含写入生产环境的动作。脚本不是沙盒，配置命令必须先审阅。

## 可选 CI / hooks

[CI 示例](../templates/ci/spine-checks.yml) 需接入后按项目运行时补安装步骤，再放入 `.github/workflows/`。
示例不由 setup 自动启用；不要并行重复已有 CI。CI 只读验证并执行检查，不自动 finalize。
宿主 hook 可以调用同一检查入口；先核对宿主文档，设置超时和有界重试，不全局拦截每个 Agent 回合。
当前版本不附带宿主特定 hook 配置，避免假设各宿主事件/API 一致。

## 已知限制

单个目标同时只运行一个 setup/verify。无跨进程事务、自动 rollback 或 upgrade 子命令。
逐文件独占创建 + 日志使中断可检测；不是整个项目的原子事务。
verify 指纹基于 Git HEAD、已跟踪文件与非忽略未跟踪文件的内容，排除 `.spine/setup`、manifest；
无 Git 时遍历常见源码文件树（排除常见缓存目录）。未追踪且被 Git 忽略的依赖/环境不在指纹内。
这是过期证据检测，不是不可伪造审计。真实环境仍需任务证据与审查。

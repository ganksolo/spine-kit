# Changelog

## 0.4.0 — 2026-10-26（Trellis 接入决策）

明确 Trellis 的职责必需、CLI 可选：
- tools/INSTALL.md 新增“Trellis 接入决策”：CLI 相对手动模式多出的能力、盘点项、三种结果及对应适配状态、手动模式最小约定。
- 全局安装和会写入项目的 `trellis init` 需用户在本次对话明确同意，不能由“适配流程”推定；用户未表态时采用手动模式，适配记为 partial。
- 手动模式不手工创建 `.trellis/`；WORKFLOW 中的 Trellis 步骤指职责，两种模式都执行。
同步 ADOPT、WORKFLOW、layers、项目 WORKFLOW 模板、适配记录模板与示例。
维护：README 当前版本说明更新（0.3.0 漏改）；任务模板新增 `superseded` 与 `closed` 状态；补记 0003/0004 状态与合并信息；任务记录不再出现具体业务项目名；仓库规范与模板明确采用 MIT License。
升级：见 docs/maintenance.md“从 0.3.0 更新到 0.4.0”。

## 0.3.0 — 2026-10-20（规则加严）

针对“标 Done 后被打回”“教训只进 Journal 不回流”“范围扩张”三类失败，把原则改为可触发的机制：
- 完成前自检成为进入 Review 的门槛：Standard/High-risk 须逐条记录 Acceptance → Evidence；本地检查必须运行，已知失败先修复；外部验证缺项注明原因与后续方式后可进入 Review，补齐前不标 done。
- 返工信号（因原验收未满足从 done 重开、独立 Review 第 3 轮仍有阻塞项、同类缺陷复发；需求变更重开不算）触发强制 retro：落实一项预防措施或写明理由；措施须放在开工必读或自动执行的位置，只写 Journal 不算。
- 扩张规则：新增能力须关联需求、问题证据或待验证假设；超出产品目标或任务范围先由用户确认并更新范围与验收；“以后可能用到”只进候选项。项目可收紧为“须由真实故障驱动”。
同步 WORKFLOW、docs/layers、playbook、安装清单与项目模板（AGENTS、WORKFLOW、PRODUCT_SPINE、gate、task、quick-task、retro）。
升级：见 docs/maintenance.md“从 0.2.0 更新到 0.3.0”；无文件结构变化，只需合并规则文本并填写回流规则位置。

## 0.2.0 — 2026-10-20（接入方式不兼容调整）

改为 Agent 可读的工作流配置源：盘点、合并本地规则、核对、记录；无本仓库运行时依赖。
保留熟悉工具链、按需技能、风险裁剪与经验回流；新增文字适配记录模板和模板选择指引。
移除 setup/verify 脚本、JSON 配置模板、专用 CI 示例/仓库脚本测试 CI、旧运行器测试。
项目规则模板自包含；安装清单不再要求为 spine-kit 安装 Python。
0.1.x 使用方需先依 docs/maintenance.md 提取规则/命令/证据并替换引用，不能直接删除旧目录。
旧版测试结果仅是历史；当前验证见 docs/validation.md。

## 0.1.1 — 2026-10-20

依据用户反馈纠正定位：以 Product Spine / Grill with Docs / Trellis / Superpowers 的阶段用法为主线；
明确 Trellis 贯穿任务、Superpowers 按需辅助执行；setup 自动化退回配套接入章节。
同步 README、工作流、分工、使用示例、安装清单与项目模板。脚本接口与配置 schema 不变。
升级：阅读定位修正，手动合并相关指引；已有 task 不搬迁，明确实际 Trellis 路径/能力。
本版本未新增自动编排或插件安装；独立 Review / 业务试点仍待完成。

## 0.1.0 — 2026-10-16

首个试用版本：整合产品主线、风险分级、单一任务来源、按需技能、独立 Review、证据验收和经验回流。
提供 Agent 接入协议、项目模板、工具清单、固定 vendor 快照、setup JSONL 日志和显式 finalize。
Python 标准库脚本支持 plan/apply/validate/verify/finalize；没有自动插件安装、自动升级或部署。
迁移：首次接入已有项目须先做只读 plan，保留既有文件，手动合并入口；详见 ADOPT.md。
验证范围与局限见 docs/validation.md。

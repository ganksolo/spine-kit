# spine-kit 仓库维护指引

本文件只约束维护 spine-kit。为另一个项目配置流程时读 ADOPT.md，不把本文件复制到业务项目。
先读 PRODUCT_SPINE.md、WORKFLOW.md、docs/layers.md 和相关 docs/tasks/ 维护任务。

- spine-kit 是 Agent 可读的工作流配置规范；不开发安装器、运行时、CLI 或新的任务控制器。
- 保持 Product Spine → Grill → Trellis → Superpowers 辅助实现 → Review → Check → Gate → 收尾的主线。
- 适配规则必须保留目标项目内容，说明必需项、可选项、冲突、缺项和实际完成证据。
- 模板是参考，项目生成物需自包含并使用实际路径；不能把日常运行依赖指向远端本仓库。
- 通用经验与项目特例分开；不强制每项任务新增规则，不复制未经许可的第三方 skills 源码。
- 文档维护检查：审查内部链接、术语/跨文档一致性、模板占位符使用说明，以及新旧项目的适配走查。
- 行为变化同步 VERSION、CHANGELOG 和迁移说明。维护记录是仓库自己的记录，不是消费者要复制的业务模板。
- 本仓库文档检查不代表项目测试、工具安装、独立 Review 或真实 Agent 试点通过；分别说明。

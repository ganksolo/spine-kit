# spine-kit 仓库维护指引

本文件适用于维护 spine-kit 本身。为业务项目接入时改读 ADOPT.md；不要把此文件复制到业务项目。

先读 PRODUCT_SPINE.md、WORKFLOW.md、docs/layers.md 和当前 docs/tasks/ 任务。
- 只支持 1–3 人；优先少量文件、明确证据和可替换工具。
- 保持 setup 可预览、保留已有内容、可恢复、可审计；不得让 apply 自动宣布完成。
- scripts/ 只依赖 Python 3.10+ 标准库；任何目标路径操作必须保持在目标根目录内。
- 改自动化须覆盖已有项目、重复执行、失败、中断、路径逃逸等边界。
- 维护检查：python3 -m unittest discover -s tests -v
- 本版本不绑定某品牌实现/审查角色，不强制多代理，不自动安装或发布。
- 改稳定行为时同步 VERSION、CHANGELOG 和迁移说明；不得将某业务项目的领域特例升为全局硬规则。
- 发布前确认实际验证证据；未做独立 Review / 真实试点应如实说明。

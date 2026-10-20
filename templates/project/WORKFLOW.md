# 项目工作流

遵循 `.spine/vendor/WORKFLOW.md`；分层说明见 `.spine/vendor/docs/layers.md`。
项目路径、任务事实源与检查命令以 `.spine/config.json` 为准。

默认主线：Product Spine → Grill with Docs（需要时）→ Trellis task → Superpowers 辅助实现
→ 独立 Review → Trellis Check → Product Path Gate → Trellis 收尾。
Trellis 贯穿任务执行；配置应映射实际任务位置。setup 只是初次接入配套。

## 项目适配

- 技术栈与运行方式：TODO
- 分支/worktree 与生产边界：TODO
- 实现/独立审查的偏好：TODO
- 外部调用和发布边界：TODO
- 通用规则例外及原因（没有则写无）：TODO

完成验收、合并、上线分别记录；不要自动升级快照或重复创建另一套任务系统。

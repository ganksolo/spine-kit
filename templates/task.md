# TASK-ID — 标题

- Owner:
- Path: Quick / Standard / High-risk（原因）
- Status: planned / in-progress / in-review / awaiting-validation / done
- Git scope: base / branch / head（含未提交文件）
- Delivery: merged=no; released=no（不适用写原因）

## Objective / User value

## Non-goals

## Acceptance → Evidence

| 条件 | 验证方法/预期 | 实际结果/证据位置 | 版本/输入 | 状态 |
|---|---|---|---|---|

进入 Review 前由实现者在当前代码上实际验证并逐条填写；本地可运行的检查必须运行，已知失败先修复。
只能在 Review 后或外部环境完成的验证，可注明原因和后续验证方式后进入 Review；补齐前不标 done。

## Validation plan

命令、真实场景、已有基线问题、外部副作用边界。

## Design / Contracts / Risks（按需）

模块边界、API/data 变化、失败场景；高风险补恢复策略。ADR 只链接不重复复制。

## Review / Product Path Gate

审查者/独立上下文、阻塞项处理、PASS/FAIL/NOT-READY、剩余局限。

## Closeout

完成项、下一步、合并/发布状态。
返工信号：无 / 因原验收未满足从 done 重开 / 独立 Review 第 3 轮仍有阻塞项 / 同类缺陷复发（需求变更重开不算）。
经验回流：无返工信号时允许无；有信号时写预防措施及其落实位置（测试/CI、Gate、入口规则、Trellis spec），或不新增的理由。

# 每日任务文档索引

这里维护依据 [Gemini V3.3 冻结路线图](../../ROADMAP.md) 执行的每日任务书索引。任务书应记录编号、授权范围、验收条件、依赖及对应 PR；不得借任务书修改冻结路线图。

| 任务 | 日期 | 范围 | 任务书来源 |
| --- | --- | --- | --- |
| LR-P0-01 | 2026-10-15 | GitHub 主仓库初始化：基础文档、Schema、校验器、测试及 CI | Human Maintainer 在本次执行会话提供的任务书；冻结基准见 ROADMAP.md |
| [LR-P0-02](LR-P0-02.md) | 2026-10-16 | 法律 Skills 发现规范、候选清单、独立检查与离线测试/CI | Human Maintainer 会话授权 AUTHORIZED_TO_EXECUTE；执行范围与 DoD 见任务记录 |
| [LR-P0-03](LR-P0-03.md) | 2026-10-17（目标）；2026-10-16 复核 | 10 条候选证据与授权审计、P1 准备清单、离线关联检查与正反测试/CI | Human Maintainer 会话授权 AUTHORIZED_TO_EXECUTE；工程交付与待决事项见任务记录和 PR |
| [LR-P0-04](LR-P0-04.md) | 2026-10-16 | 三轨收录政策、独立提案模型、10 条分流与 P1 选品计划、离线检查/测试 | Human Maintainer 会话授权 AUTHORIZED_TO_EXECUTE；后续托管、原创研发与正式入库须另审 |
| [LR-P0-05](LR-P0-05.md) | 2026-10-17（目标）；2026-10-16 整理 | 三个固定候选逐文件托管预审、专业交接、离线校验/CI 与 P0 实证验收准备 | AUTHORIZED_TO_EXECUTE；托管/法律批准与合并仍待人工；[PR #5](https://github.com/fitalex/LexRouter/pull/5) |
| [LR-P1-01](LR-P1-01.md) | 2026-10-17 执行；P1 窗口 10.20–10.28 不变 | 新增 10 条候选、联合 20 条、六类检索/人工去重、离线联合校验与 CI；新 A3/C7/B0 | 会话任务书 AUTHORIZED_TO_EXECUTE；[审核表](../P1_BATCH_01_REVIEW.md)，正式入库 0，不执行 P1-02 或合并 |
| LR-P1-02 | 2026-10-18 | 可复用法律 Skill 复核工作台 v1、独立 Schema、角色白名单、三个真实待核样本材料准备及 CLI | [PR #7](https://github.com/fitalex/LexRouter/pull/7)；详情见 [Review Workbench 说明](../review-workbench/README.md) |
| LR-P1-03 | 2026-10-18 | 配置 fitalex 审阅角色白名单（Legal/Rights/Engineering/Maintainer） | [PR #8](https://github.com/fitalex/LexRouter/pull/8)；配置位于 `data/reviews/reviewers.json` |
| LR-P1-04R | 2026-10-20 | Gate 1: Review Workbench v2 契约、专家短表、信任同步与迁移兼容性测试 | [PR #15](https://github.com/fitalex/LexRouter/pull/15)；详情见 [v2 工作台说明](../review-workbench/v2/EXPERT_SHORT_FORM.md) |
| LR-GOV-01 | 2026-10-27 | 多 Agent 协作规范 V2 与 DeepSeek Harness 自动化 Discovery 分工 | [PR #17](https://github.com/fitalex/LexRouter/pull/17)；确立五方分工与每周检索机制（待启用） |
| [LR-AG-INIT-01](LR-AG-INIT-01.md) | 2026-10-31 | Antigravity 工作区初始化、文档基线审计、建立维护基线手册与任务索引更新 | Human Maintainer 会话任务书；[基线手册](../ANTIGRAVITY_DOCS_BASELINE.md) 与 Draft PR |

本索引不代表任务已完成验收；交付与 CI 证据以对应 PR 为准。后续获授权的任务书在此追加链接，公开版本不得包含密钥、敏感卷宗或 Holdout 内容。

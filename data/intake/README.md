# P0 收录提案区

[p1-proposals.json](p1-proposals.json) 服务 LR-P0-04，当前为 10 条候选提案（A 3、C 7）与 4 项独立 B 原创机会。正式托管、专业复核、正式目录、测评及路由批准均为 0。原 7 条 blocked 不变。规则和逐条理由见 [收录政策](../../docs/SKILL_INTAKE_POLICY.md) 与 [P1 计划](../../docs/P1_SELECTION_PLAN.md)。

顶层为 `format_version: 1`、`task: LR-P0-04`、非空 `records` 与 `original_opportunities` 数组。对象均禁止额外字段。

| 字段 | 契约 |
| --- | --- |
| records.candidate_id | 与 candidates/readiness 恰好一对一关联，唯一、不遗漏，不重复许可、URL、法域、日期及阻塞证据 |
| readiness_snapshot_sha256 | 对该 Candidate ID 的完整 readiness 记录按已有 fingerprint 算法计算；审计变动必须重新审阅提案。不是签名、授权证明或专业结论 |
| proposed_track | 候选只允许 curated-hosting / external-reference；blocked/rejected 在本 P0 契约中只允许 C。B 只在独立机会记录中 |
| business_value_and_rationale | 独立撰写非空选择理由，分类及来源回查候选，不重复存储 |
| authorization_basis | 候选固定 reference=p1-readiness.authorization_review、proposed_use_review=not-performed；通过 Candidate ID 找到原审计许可依据。本任务没有针对全文或新用途批准 |
| approvals | proposal=proposed；authorization 按原审计为 pending/blocked；legal_professional=not-performed、hosting=not-approved、catalog=not-admitted、evaluation=not-performed、routing=not-assessed，互不替代 |
| permissions | copy=false、redistribute=false，必须为布尔值；C 不因索引而授予执行权限，整个提案不声明运行/测评许可 |
| required_gates | 非空唯一枚举，必须含模式决定、权利/原创性审查、专业法域时效审查、去重/Schema、维护者收录 PR；A 加全文托管范围审批，B 加独立需求/设计/测试 |
| next_actions | 非空 owner/action；必须安排 Human Maintainer、legal-professional、engineering-maintainer，可列 upstream-rightsholder；角色不等于人员已被联系或完成工作 |
| opportunity_id / related_candidate_ids | 独立 original-… ID，全局唯一、不与候选 ID 冲突；背景关联必须有效，不能作为授权或设计继承 |
| business_problem / expected_deliverables / independent_design_sources / independence_boundary | 独立业务问题、预期交付、来源计划和隔离边界；均非空，来源/交付数组非空唯一。计划不代表已读来源或完成研发 |
| 原创 authorization_basis / development_status | 固定 not-inherited / not-started；审批授权轴独立保持 pending，不继承背景候选的 verified/blocked；同样无复制/再分发许可 |

```sh
python scripts/validate_intake_plan.py
python scripts/validate_intake_plan.py tests/fixtures/intake/valid.json --candidates tests/fixtures/p1-readiness/candidates.json --readiness tests/fixtures/p1-readiness/valid.json
```

检查使用现有 Python/jsonschema，无新增依赖，复用 LR-P0-03 的来源审计检查。默认使用真实清单；可用 `--candidates` / `--readiness` 指定配对样本。成功 0、数据错误 1、参数错误 2，错误含文件及 JSON Pointer；拒绝非法 JSON、重复键、NaN/Infinity、非 UTF-8 及缺失文件。不联网、不下载或执行 Skills，不批准任何权利或法律事实。

本版本故意只接受提案状态，未来证据化审批记录和长期目录布局须另提设计/PR，不能改一个字段即授予权限。正式八字段不变，辅助 JSON 不得移到 `skills/`。历史证据与提案变化保留于 Git/PR，不静默升级原审计。

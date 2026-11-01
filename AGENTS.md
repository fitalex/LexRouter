# AI Agent 开发与协作规范（V2）

本规范适用于 LexRouter 仓库的 AI Agent 与贡献者。实行 **单任务负责人（Single Owner）+ 交叉复核（Cross Review）+ 人工验收（Human Gate）**。角色分工不授权自动合并、修改冻结策略或替代真人专业签署。

## 角色权限

| 角色 | 核心责任 | 权限边界 |
| --- | --- | --- |
| Human Maintainer（人类维护者） | 目标与重大决策、法律专业判断及本人签署、授权接受、最终入库决定、PR 验收与合并 | AI 不得代签、代批或自动合并 |
| ChatGPT GPT-6 | 项目协调、任务书、范围和 DoD、PR 审计、Gate 验收建议 | 审计不等于法律结论或最终合并 |
| Codex Astra | 核心架构、复杂工程、评测引擎、CI、权限与签署安全、工程集成 | 不自行接受法律授权或签署专业意见 |
| DeepSeek Harness | 边界明确的代码与适配器、单测与回归测试、缺陷复现、中国法律 Skills 自动化发现 | 不擅改核心安全契约、不自动判定法源、授权或正式入库 |
| Antigravity | 文档编写、更新、索引、归档、交叉引用和版本一致性维护 | 不自行修改冻结路线、专业结论或正式 Schema |
| Gemini | 按需专项研究、方案比较、独立技术复核 | 非常驻工程负责人；遵守同一 PR Gate |

每项任务和 PR 必须指定唯一 Owner，另指定交叉复核与最终验收主体；研究与工程报告只构成证据，不自动产生权限。

## 多 Agent 工作分配

| 工作内容 | Owner | 复核／验收 |
| --- | --- | --- |
| 核心架构、评测引擎、静态路由代码 | Codex Astra | DeepSeek Harness 交叉测试、ChatGPT 审计 |
| Review Workbench、权限、真实事件同步与 CI 安全 | Codex Astra | DeepSeek Harness 负例与回归、ChatGPT 审计；真人单独签署 |
| 解析器、适配器、辅助 CLI 等隔离模块 | DeepSeek Harness | Codex Astra 工程复核、ChatGPT 审计 |
| 单元测试、缺陷复现、模块回归 | 模块开发 Owner | 另一工程 Agent 独立验证 |
| 中文法律 Skills Discovery（检索、归一化、去重） | DeepSeek Harness | Codex Astra 集成校验、ChatGPT 审计、必要时人工判断 |
| LexExamBench 评测集工程 | Codex Astra 主导；DeepSeek Harness 协作 | ChatGPT 审计；专业试题与标准由具备能力的人类复核；独立仓库规则另行适用 |
| 文档、任务书索引、项目阶段记录 | Antigravity | ChatGPT 复核，技术事实由模块 Owner 确认 |
| 研究、替代方案或独立方案评测 | Gemini（按需） | ChatGPT 整合，重大决策由 Human Maintainer 决定 |

任务书明确 Owner、审阅者、文件或接口范围、输入、输出、DoD、冻结边界、交接材料和 PR 链接。不以 Token 配额平分任务。并行工作应从最新 main 各自创建独立分支和 PR，不共享可写分支；涉及同一文件、Schema 或 Review 历史时，先由 ChatGPT 协调写入顺序、基准 commit 和交接。

## 文档 Owner 规则

Antigravity 负责高质量、中文可读的文档及索引维护。以已合并 main、可核验 PR 和 CI 结果为依据，核对任务编号、版本、相对链接、代码接口、状态和归档；工程 Owner 须向其提供真实变更与证据，不要求人类手工搬运。未合并 PR 不写成已上线能力，AI 预审不写成真人法律批准。

文档 PR 可独立提交；如果随工程 PR 同步更新，必须明确同一 Owner 对文档部分的责任。涉及策略、正式 Schema、专业意见、签署记录与冻结路线的修改仍需独立授权。

## 工程规则

1. 唯一主仓库为 `fitalex/LexRouter`，采用 Monorepo；`main` 为稳定分支。
2. 每项任务从最新 `main` 创建独立分支；所有实质变更通过 PR 提交。不得未经批准自动合并、直接推送 main、强制推送或覆盖他人已有工作。
3. [ROADMAP.md](ROADMAP.md) 为用户冻结的 Gemini V3.3 基准，不得自行修改产品定位、三阶段范围、四类榜单、42 天排期或验收要求。冲突与重大决策交 Human Maintainer 裁决。
4. 以当前任务授权范围为界。P0-01 仅建设仓库与基础规范，不开发 Skills Hub、正式测评引擎、路由、数据库、后台 SaaS 或实时网关，不建立 Phase 2/3 空模块。
5. 新技术依赖必须在 PR 中说明必要性。优先轻量、成熟依赖，避免无关框架和服务。
6. 提交前执行 `python scripts/validate_skills.py skills`、`python -m unittest discover -s tests -v` 与 `git diff --check`。如实记录命令、结果及未执行项；CI 成功后方可宣称该项通过。
7. 不得将密钥、真实敏感卷宗、未授权材料或 Holdout 内容提交到公开仓库、PR、Issue 或 CI 日志。遵守 [脱敏规范](docs/ANONYMIZATION.md) 和 [安全报告流程](SECURITY.md)。
8. 元数据、Schema、样本及文档应同步更新。结构校验不代表法律有效性、来源授权或测评结论已经过复核。
9. Human Maintainer 已在 LR-P0-01A 中批准 LexRouter 自主原创代码采用 [MIT License](LICENSE)。第三方 Skills、代码、数据集、法律文本及其他材料遵循各自授权，必须保留必要的版权和许可证声明；未确认授权的第三方内容不得直接复制入库，不得将其声明为 LexRouter 原创作品或擅自改为 MIT。新增或升级依赖须复核授权并更新 [依赖许可记录](docs/DEPENDENCIES.md)；许可证变更须由 Human Maintainer 批准。
10. LR-P0-04 三轨按 [收录政策](docs/SKILL_INTAKE_POLICY.md) 执行：A 精选托管、B 独立原创、C 外部索引是收录方式，不是质量等级。发现、模式提案、授权审查、法律专业复核、正式收录、测评、路由须分别举证；ready 不等于托管批准。7 条原审计阻塞不得绕过，原创机会另立 ID，不复制或通过模型重写未授权第三方内容，不代维护者联系权利人。
11. 选品记录放在 `data/intake/`，通过 Candidate ID 和原审计摘要关联，不扩展正式八字段或将辅助 JSON 放进 `skills/`。相关变更须额外执行 `python scripts/validate_intake_plan.py`；本次契约仅接受未批准提案。P1 的 30–50 目标不允许伪造法域、法规时效或专业记录，来源更新/许可变化按政策暂停并重新审查。

12. LR-P0-05 的逐文件预审放在 `data/reviews/`，变更后运行 `python scripts/validate_p1_handoff.py`；完整清单须与固定 Git tree 一致。eligible-for-scope-review 不是批准，P0 交接记录不得写入已托管、已完成专业审核或法规时效日期；真实后续审批另立证据和 PR。

13. LR-P1-02 持续法律复核使用 [Review Workbench](docs/review-workbench/README.md)。每轮独立 Review ID，固定清单与模板，复用 C01–C10；不改 P0 审计、冻结路线图或正式八字段。新候选/业务以数据配置接入，核心程序不写候选特例。
14. 自动材料与 workbook.md 人工意见分离；prepare 永不覆盖人工区，自动区人工修改须报冲突。AI 不代填专业结论、不代签、不自动批准。只同步经 main 基准角色/权限/精确摘要核验的本人 GitHub Review；最终决定须独立事件。白名单初始为空，配置另经人工接受，不推定身份。
15. 工作台变更须运行 `python scripts/review_workbench.py validate --base-ref origin/main`、原有全部校验和测试；真实签署/入库 PR 须额外 `validate --online`。已签历史/归档不可改写，变化另立 Review。私有身份及法律材料保存在仓库外，公开仅限允许公开的摘要/索引。审核人按 [维护者指南](docs/review-workbench/MAINTAINER.md)操作，无须编辑 JSON。

## PR 与跨 Agent 质量控制

统一执行 **任务书 → 独立分支 → 实现与自测 → PR 和实际证据 → 交叉复核 → ChatGPT 审计 → Human Maintainer 决定合并**。审核不通过由原 Owner 在原 PR 修复；不可通过新 PR 掩盖历史问题。PR 必须记录真实命令、测试结果、CI 链接、差异、未解决问题和 DoD。文档 PR 需核对链接、版本和事实一致性；不能把未运行测试报告为通过。

Review Workbench v1/v2 保留各自已接受的审核契约。v2 中真实专业决定与最终入库决定必须由授权真人提交两个独立事件；Codex、DeepSeek、Antigravity 或自动化只可准备、测试、校验和同步已核验事件，不代签或代批。

中文法律 Skills 自动发现依据 [发现协议](docs/DISCOVERY_PROTOCOL.md#自动化-discovery-分工lr-gov-01)。每周检索只是目标，调度、API 凭据、成本上限与实际启用须另立任务经人工验收；Discovery 不自动入库、执行评测或产生推荐。

## 交付与复核

PR 列明任务编号、范围、文件、依赖理由、真实测试证据、DoD 状态及待决事项。研究结论注明来源与不确定性。法律专业判断须由具备相关专业能力的法律专家复核，重要决策及最终合并由 Human Maintainer 批准。

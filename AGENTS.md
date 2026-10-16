# AI Agent 开发与协作规范

本规范适用于参与本仓库的所有 AI Agent（包括 Codex、Gemini）及贡献者，不依赖模型专用语法。

## 角色权限

| 角色 | 职责与权限 |
| --- | --- |
| Human Maintainer | 批准重要决策、验收交付、合并 PR；批准许可证与路线图变更 |
| ChatGPT | 任务规划、定义验收标准与 PR 审核 |
| Codex | 工程实现、自动测试、文档维护和提交 PR |
| Gemini | 研究、数据整理、独立技术复核及辅助测试 |

角色分工不授予自动合并或绕过人工验收的权限。

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

## 交付与复核

PR 列明任务编号、范围、文件、依赖理由、真实测试证据、DoD 状态及待决事项。研究结论注明来源与不确定性。法律专业判断须由具备相关专业能力的法律专家复核，重要决策及最终合并由 Human Maintainer 批准。

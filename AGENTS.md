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
9. 许可证待人工批准；不得擅自加入 LICENSE 或声称已授予开源再分发授权。

## 交付与复核

PR 列明任务编号、范围、文件、依赖理由、真实测试证据、DoD 状态及待决事项。研究结论注明来源与不确定性。法律专业判断须由具备相关专业能力的法律专家复核，重要决策及最终合并由 Human Maintainer 批准。

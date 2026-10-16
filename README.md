# LexRouter
Open-source discovery, evaluation, and routing infrastructure for Legal AI

LexRouter 面向法律行业建设 AI 能力发现（Discovery）、测评（Evaluation）与路由（Routing）基础设施：先发现可追溯的能力，再以控制变量测评形成证据，最后支持基于证据的技术选型。项目采用单一主仓库、静态优先和法律专家把关的协作方式。

## 三阶段范围

| 阶段 | 正式名称 | 产品范围 |
| --- | --- | --- |
| Phase 1 | Lex-Skill-Router | 法律工作流与规则（Skills / Rules / Prompts）；固定底座模型测评，建设静态选型推荐与配置导出/CLI |
| Phase 2 | Lex-Data-Router | 法律数据与工具（法规/案例 API、MCP）；Phase 1 验收后启动 |
| Phase 3 | Lex-Model-Router | 通用与垂直大模型（LLMs）；前两阶段成熟后启动 |

当前处于 Phase 1 的 P0 仓库与规范建设。已提供工程骨架、元数据规范及校验、测评与合规基础协议，以及独立的发现候选清单和离线检查；尚无正式 Skills 条目、测评结果、榜单、站点或路由功能。不面向 C 端当事人提供法律咨询，不建设重度律所 SaaS 或实时流量代理网关。

## 文档入口

- [冻结路线图 Gemini V3.3](ROADMAP.md)
- [AI Agent 协作规范](AGENTS.md) · [社区贡献指南](CONTRIBUTING.md) · [安全报告](SECURITY.md)
- [能力元数据规范](docs/SCHEMA.md) · [JSON Schema](schemas/skill.schema.json)
- [法律 Skills 发现协议](docs/DISCOVERY_PROTOCOL.md) · [候选来源、统计与待核实事项](data/discovery/README.md)
- [P1 入库准备审计与专业复核交接](docs/P1_READINESS.md)（3 条具备提交条件、7 条阻塞，均未正式入库）
- [三轨收录政策](docs/SKILL_INTAKE_POLICY.md) · [P1 选品计划](docs/P1_SELECTION_PLAN.md)（3 条精选托管提案、7 条外部索引提案、4 项独立原创机会，均未批准执行后续内容工作）
- [控制变量测评协议](docs/EVAL_PROTOCOL.md) · [数据脱敏与合规](docs/ANONYMIZATION.md)
- [每日任务索引](docs/daily-specs/README.md) · [Skills 收录规范](skills/README.md)

## 本地检查

使用 Python 3.11 或更新版本：

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_skills.py skills
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
python scripts/validate_intake_plan.py data/intake/p1-proposals.json
python -m unittest discover -s tests -v
```

正式目录为空时，校验器明确报告 0 个文件；CI 仍须执行固定合法与非法样本测试，证明约束有效。

`data/discovery/` 记录真实来源线索及授权、法域和法规时效的核查状态，与正式 `skills/` 分离。候选检查通过只证明结构合法，未核实的时效使用显式状态与 null；不得据此生成正式时效日期、推荐或宣称测评通过。

## 社区与许可

欢迎通过 Issue 讨论及 Pull Request 贡献，实质变更由 Human Maintainer 审核合并。**Human Maintainer 已批准 LexRouter 自主原创代码采用 [MIT License](LICENSE)**（LR-P0-01A）。

第三方 Skills、代码、数据集、法律文本及其他材料遵循各自授权，不因进入本仓库而改为 MIT 或成为 LexRouter 原创作品。必须保留必要的版权和许可证声明；未确认授权的第三方内容不得直接复制入库。直接依赖的版本与许可证检查见 [依赖许可记录](docs/DEPENDENCIES.md)。

**测评与路由结果仅供技术选型参考，不构成执业法律意见。** 实际法律事务应由具备相应资质的专业人士结合具体事实、适用法域及现行法律独立判断。

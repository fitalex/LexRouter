# P0 最终验收准备报告

核查日期：2026-10-16（Asia/Shanghai）；基准为最新 main `8fcec1d2987233bc1ac5ac3f85c47297f07efb84`（PR #1–#4 已合并）。本报告是 LR-P0-05 的验收准备证据，最终验收/合并由 Human Maintainer 决定。P0 截止 2026-10-19，P1 自 2026-10-20 启动，未改变 [ROADMAP.md §04](../ROADMAP.md)。

**工程状态：READY_FOR_REVIEW — HUMAN_APPROVAL_PENDING。** 冻结 P0 的交付范围是 Monorepo 骨架、能力元数据 Schema、控制变量测评协议，明确 DoD 是 GitHub Actions 自动验证 Skill 元数据必填字段。下表中规范和测试核查是这些交付的证据；三个候选托管预审属于提前交接附加项。法律专业审核、完整托管批准、P1 的 30–50 正式条目和测评/路由均不是本次 P0 必须完成项。没有发现需要修改冻结验收口径的实质工程阻塞；CI 在 PR 实际运行前不声称通过。

状态含义：PASS=在注明的范围内有实查证据；FAIL=已检查但不满足要求；BLOCKED=所需证据/人类决定缺失，当前不能完成；NOT_APPLICABLE=不属于该阶段或当前不存在对应对象。结构 PASS 不代表法律、授权或产品功能已通过。

## 一、冻结 P0 必须交付与工程验收证据

| 检查项 | 状态 | 对应证据 | 实际检查方式 | 剩余风险 | 后续责任角色 |
| --- | --- | --- | --- | --- | --- |
| 单一主仓库 Monorepo 骨架 | PASS | [README](../README.md)、[AGENTS](../AGENTS.md)、[目录规范](../skills/README.md) | 核对 origin 为 fitalex/LexRouter；读取 Git 树及 README 三阶段范围；未建 Phase 2/3 或产品空模块 | 骨架不意味着发现站点/引擎可用 | 工程维护者 |
| README、AGENTS、CONTRIBUTING、安全/脱敏规范 | PASS | [CONTRIBUTING](../CONTRIBUTING.md)、[SECURITY](../SECURITY.md)、[ANONYMIZATION](ANONYMIZATION.md)、[PR 模板](../.github/pull_request_template.md) | 逐文档检查角色、分支/PR、人工合并、敏感材料、贡献与授权说明；核对本地链接 | 人员是否遵循规范仍需人工审核 | Human Maintainer |
| 原创代码 MIT 落地与第三方边界 | PASS | [LICENSE](../LICENSE)、AGENTS §工程规则 9、CONTRIBUTING 许可段、[依赖记录](DEPENDENCIES.md) | 检查 MIT 正文、Copyright (c) 2026 fitalex、LR-P0-01A 决定记录及第三方不继承 MIT 说明 | 不扩大为第三方全文权属鉴定或传递依赖全量审计 | Human Maintainer / 许可人员 |
| 正式八字段定义与文档一致 | PASS | [skill.schema.json](../schemas/skill.schema.json)、[SCHEMA](SCHEMA.md) | required/properties 均为 id、name、description、source_url、jurisdiction、business_categories、regulatory_as_of、runtime；additionalProperties=false；与 main 比较无变更 | 日期格式通过不代表该日期有法律依据 | 工程维护者 / 法律专业人员 |
| 必填/类型/枚举/非法值拒绝 | PASS | [validate_skills.py](../scripts/validate_skills.py)、[12 项元数据测试](../tests/test_validate_skills.py)、[固定反样本](../tests/fixtures/invalid/) | 运行合法 fixture CLI 及 unittest；缺必填、非法枚举/日期/类型、空分类、额外字段与非对象反例均按预期拒绝 | 测试验证结构，未验证法律任务效果 | 工程维护者 |
| 重复 ID 检查 | PASS | validate_skills.validate、test_duplicate_ids_across_nested_files | 运行跨目录同 ID 反例及输入重叠去重测试 | 业务功能重复仍需 P1 人工去重 | 工程维护者 / Human Maintainer |
| 正式目录为空时准确报告 | PASS | [skills/README](../skills/README.md)、validate_skills.main | 实际执行 `python scripts/validate_skills.py skills` 返回 0 文件、directory is empty；仍运行合法及非法样本 | 0 条正式 Skill，不应推断达到 P1 数量或质量目标 | Human Maintainer |
| 固定底座与单变量归因 | PASS | [EVAL_PROTOCOL](EVAL_PROTOCOL.md) 的固定底座与单变量段 | 人工核对供应方/精确快照、参数、工具、数据、超时重试与基线对照，只改变 Skill 的规定 | 精确模型选择和实际实验尚未执行，留待 P2 | 测评负责人 |
| Public / Holdout 隔离 | PASS | EVAL_PROTOCOL 的隔离段、ANONYMIZATION、AGENTS | 核对受控存储、污染/重叠、禁止公开内容/日志、禁止反复调优、fixture 非测评集的规定 | Holdout 完整公开复现与保密协调仍待后续协议决定，不是 P0 引擎缺陷 | Human Maintainer / 测评负责人 |
| 法律时效、引用真实性与专业复核规则 | PASS | EVAL_PROTOCOL 的法域/时效和专家复核段、[收录政策](SKILL_INTAKE_POLICY.md) | 核对废止/虚构引用 0 分、事实时间/过渡规则、证据追溯及专家复核；不将结构校验当法律判断 | 专家资质/人数、一致性统计及阈值未确定，按路线图在后续阶段执行 | 法律专业人员 / 测评负责人 |
| Run Artifacts 与合规边界 | PASS | EVAL_PROTOCOL 的快照段、README 免责声明、ANONYMIZATION | 核对版本/参数/环境/输入输出/计费/评分/证据字段、Public 可发布快照与 Holdout 受控留存；免责声明明确 | 仍需后续解决公开复现与保密细则；本次无真实运行快照或法律分数 | Human Maintainer / 测评负责人 |
| GitHub Actions 自动校验元数据必填（冻结 DoD） | BLOCKED | [validate-skills.yml](../.github/workflows/validate-skills.yml) | 配置含 pull_request、main push、workflow_dispatch；安装固定依赖、校验正式目录/合法样本并运行反例测试；本 PR 的实际 Actions 链接待创建后核实 | 本地成功不能冒充 GitHub Actions 成功；见后续 PR 验证记录 | Codex 核实运行；Human Maintainer 验收 |
| 现有工程校验、CLI、正反样本接口 | PASS | [scripts](../scripts/)、[tests](../tests/)、[tests README](../tests/README.md) | 原 52 项测试通过；加入交接后全套 66 项通过；候选/readiness/intake/handoff CLI 全通过；调用参数与 CI 对应 | 固定依赖环境亦 66 项通过，见下方记录；外部来源可用性不属于离线校验结论 | 工程维护者 |
| 依赖、文档链接及接口一致性 | PASS | [requirements](../requirements.txt)、DEPENDENCIES、README/CONTRIBUTING CLI、CI | 固定 jsonschema==4.25.1、rfc3986-validator==0.1.1，未新增依赖；171 个本地相对文件链接检查及 diff whitespace 检查；默认与合成 CLI 均测试 | 外部官方门户仅为线索未逐一检查；不是依赖树安全认证 | 工程维护者 |
| 候选不被解释为正式批准 | PASS | candidates/readiness/intake 原记录、[交接契约](../data/reviews/README.md)、README 及 CI 输出 | 与 main 比较三份旧数据零 diff；实际统计 4 candidate/6 needs-evidence、3 ready/7 blocked、3 A/7 C；测试拒绝批准/日期升级 | 文档使用者仍需理解 ready 与批准分轴 | Human Maintainer |

## 二、P1 提前准备的附加工程项

这些附加项不改变 P0 冻结 DoD，也不等于已完成 P1 目录整合。

| 检查项 | 状态 | 对应证据 | 实际检查方式 | 剩余风险 | 后续责任角色 |
| --- | --- | --- | --- | --- | --- |
| 三轨政策、10 条分流、4 个原创机会 | PASS | SKILL_INTAKE_POLICY、[P1_SELECTION_PLAN](P1_SELECTION_PLAN.md)、[p1-proposals](../data/intake/p1-proposals.json) | 原校验器通过；政策和数据与 main 零 diff；无原创研发启动 | 模式为提案，未赋权 | Human Maintainer |
| 3 个固定版本独立材料清单 | PASS | [三份说明](reviews/README.md)、[manifest 目录](../data/reviews/manifests/)、[handoff](../data/reviews/p1-handoff.json) | 只读 Git 对象；31+13+2339=2383 文件；原 blob 比对、完整 tree 重建、清单摘要/数量检查 | 二进制/知识库未逐件读；哈希只能证身份，不能证权属 | 工程维护者 / 许可人员 |
| 逐文件拟托管边界与依赖待办 | PASS | 三份说明、manifest 四类决定、unresolved_issues | 27/4/19 文件仅 eligible-for-scope-review；分别列额外授权/排除/未知项；静态扫描依赖、绝对路径和安装不一致 | 尚无完整包可运行结论；外部资料不继承根许可 | Human Maintainer / 工程维护者 |
| 具体法律专业交接材料 | PASS | [P1_LEGAL_REVIEW_HANDOFF](reviews/P1_LEGAL_REVIEW_HANDOFF.md) | 三候选分别定义固定版本/任务/法域、官方线索、时效与引用、高风险/人工决定、签署和不通过处理；原 required_checks 未丢失 | 无已指派专业人员，无专业结论 | 法律专业人员 / Human Maintainer |
| 最小交接记录、离线校验和 CI 接入 | PASS | [validate_p1_handoff](../scripts/validate_p1_handoff.py)、[14 项测试](../tests/test_validate_p1_handoff.py)、workflow | 复用 jsonschema/原 audit/intake；检查 A 类覆盖、摘要、路径及树完整、原待办；正反测试和 socket 禁用测试通过 | 数据状态仅限本次未批准快照，未来真实审批需独立契约 | 工程维护者 |
| 无第三方全文/执行/正式入库 | PASS | 本 PR 文件 diff、新增清单仅路径/哈希/原创描述；正式 skills 零 diff | 只读检查上游，不导入或运行；临时审计对象在仓库外；核对变更类型和 staged 文件 | 原路径也可能含上游命名信息，但无原文/图片/知识库内容入提交 | Codex / Human Maintainer |
| 未越界至产品或冻结变更 | PASS | ROADMAP、Schema、政策、skills、requirements 与 main 无差异 | Git diff 指定路径；无榜单/引擎/路由/前端/数据库新增；无原创完整研发 | 维护者审核本 PR 最终范围 | Human Maintainer |

## 三、依赖人类的 P1 门槛与后续资源

| 事项 | 状态 | 对应证据 | 实际检查方式 | 剩余风险与所需决定 | 后续责任角色 |
| --- | --- | --- | --- | --- | --- |
| 3 个候选具体用途/完整托管批准 | BLOCKED | manifest、unresolved_issues、收录政策 | 只具备预审材料，所有 hosting_status 为 not-approved | 确定复制/改编/公开分发/运行/测评/商用用途和文件范围；核权利人/贡献者；笔记、数据库、品牌、模板补证 | Human Maintainer / 许可人员 / 必要权利人 |
| 3 个候选法律专业复核及真实法规时效 | BLOCKED | handoff professional_todos、交接包 C01–C10 | professional_status 全 not-performed、时效未核实/null；未填写人员/结论/日期 | 指派有能力人员、预算和时间；官方文本/地方规则查核、签署、分歧复核和证据受控位置 | Human Maintainer / 法律专业人员 |
| 7 条既有授权/独立性阻塞 | BLOCKED | [原 readiness blocker](../data/discovery/p1-readiness.json)、[P1_READINESS 阻塞说明](P1_READINESS.md) | 七条原记录零 diff、原校验通过 | 见下表；没有新权利补证，不解除 | Human Maintainer / 相关权利人、许可人员、工程维护者 |
| 运行环境与维护资源 | BLOCKED | 三份材料说明依赖表、handoff unresolved_issues | 仅静态核查；未测试 officecli、Claude、Codex、OCR、商业数据库或上游脚本 | 指定适配负责人和环境；授予所需工具/数据使用权，解决路径、TLS 回退及无库失败；另开 P1 PR | 工程维护者 / Human Maintainer |
| 4 个原创机会立项 | BLOCKED | original_opportunities 的 not-started/未批准状态 | 原提案不变，本次未研发 | 独立需求、来源隔离、人员和预算另决策 | Human Maintainer |
| P1 30–50 正式 Skills、100% 法域/分类/时效 | NOT_APPLICABLE | ROADMAP §04、正式目录为空 | P1 尚未开始，不能据候选数量声称达成 | 由 P1 分批获授权/专业复核及去重，数量目标不能覆盖证据门槛 | Human Maintainer / P1 负责人 |
| 实际测评/四类榜单/静态路由与前端 | NOT_APPLICABLE | ROADMAP P2–P4 | 本轮无对应功能或运行结果 | 后续里程碑处理 | 各后续任务负责人 |

七条阻塞完整保留（事实及证据仍以原 readiness 为准）：

| Candidate ID | 未解事项 | 补证/决定角色 |
| --- | --- | --- |
| discovery-cn-law-hub | NOTICE 排除未明确授权贡献者组件，根 Apache 不覆盖整包 | Human Maintainer / 贡献者或权利人 / 许可人员 |
| discovery-litigation-hub | CC-NC-ND 及附加测评/机构等限制，套件编排独立性不明 | Human Maintainer / 许可人员 / 工程维护者 |
| discovery-litigation-prep-cn | 未找到明确许可 | Human Maintainer / 权利人 |
| discovery-law-ye | 未找到明确许可 | Human Maintainer / 权利人 |
| discovery-shuanglv | 自定义许可限制公开改编、产品集成等，品牌另审 | Human Maintainer / 权利人 / 许可人员 |
| discovery-antitrust-filing | 同版本 Proprietary 与 CC-BY-NC 声明冲突 | Human Maintainer / 权利人 / 许可人员 |
| discovery-gutachten-admin | CC-NC-ND 与附加限制及优先条款解释问题 | Human Maintainer / 权利人 / 许可人员 |

## 四、实际执行记录与可验证范围

本地初次全套：Python 3.12.14，66 tests，13.365s，OK（原 52 + 新 14）。原环境缺少 rfc3986-validator 发行元数据，不能将其当作 requirements 已按 CI 安装；已在仓库外干净 venv 安装固定 requirements（jsonschema 4.25.1、rfc3986-validator 0.1.1）复验：66 tests，14.599s，OK；六项 CLI 均通过。不修改依赖文件；CI 使用 Python 3.11，结果单独核实。

```sh
python scripts/validate_skills.py skills
python scripts/validate_skills.py tests/fixtures/valid
python scripts/validate_candidates.py
python scripts/validate_p1_readiness.py
python scripts/validate_intake_plan.py
python scripts/validate_p1_handoff.py
python -m unittest discover -s tests -v
git diff --check
```

各 CLI 实际返回 PASS：正式目录 0、合法样本 1、候选 10、readiness 10、提案 10、交接 3。坏样本由测试确认应失败，不将其退出 1 误报为工程失败。新增检查是离线结构/身份/状态检查，不访问来源网站、执行法律用例或认定许可有效。

本地文档链接检查限 Markdown 的相对文件目标（包含目录），外部 URL 和法律官方文本未经逐一验证。冻结文件和旧数据的比较命令：`git diff origin/main -- ROADMAP.md schemas/skill.schema.json docs/SKILL_INTAKE_POLICY.md data/discovery data/intake skills requirements.txt`，结果为空。

GitHub Actions：待本 PR 创建后查看实际运行，不以本地测试或配置审阅代替运行成功。最终运行 URL 和状态将记录于本报告及 PR；保持 PR 未合并，等待 ChatGPT 复审及 Human Maintainer 决定。

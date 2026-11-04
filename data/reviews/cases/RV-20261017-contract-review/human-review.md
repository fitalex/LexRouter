# LR-P1-04 Task A｜Contract Review 人工复核导航

Review ID：`RV-20261017-contract-review` · Human Reviewer：`fitalex` · 所有 15 项专业检查仍为 **pending**。

本导航是 Codex 整理的技术事实、阅读入口与待决问题，不填写人工工作表，不构成法律意见、本人签署或入库批准。实际分配状态和事件来源以 [record.json](record.json) 为准。

## 阅读与填写入口

1. 阅读 [packet.md](packet.md)、[完整问题矩阵 matrix.md](matrix.md)、[逐文件固定来源 evidence.md](evidence.md)。
2. 按下表进入原站固定版本和 [workbook.md](workbook.md) 的对应章节。仅在本 PR 分支填写工作表，未核实的项保持 pending。
3. 对照 [完整清单 inventory.json](inventory.json) 和 [原 P0 manifest](../../../../data/reviews/manifests/discovery-contract-review.json) 核实范围；本导航链接不会扩大审核范围。
4. 按 [维护者指南](../../../../docs/review-workbench/MAINTAINER.md) 完成受控身份、资质、利益冲突核验和本人签署。

## 已验证的技术事实

- 三个工作分支均从 main `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8` 创建；该基准含已由 fitalex 本人合并的 [PR #8](https://github.com/fitalex/LexRouter/pull/8)。GitHub 合并记录为 2026-10-18T03:21:08Z；这是配置合并时间，不是法律核验或签署时间。
- 授权只取该 main 基准的 [reviewers.json](https://github.com/fitalex/LexRouter/blob/a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8/data/reviews/reviewers.json)：fitalex 已配置 Legal Reviewer、Rights Reviewer、Engineering Reviewer、Human Maintainer。配置不证明自然人资质或完成专业复核。
- 固定来源 commit：`f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`；上游 Git tree：`15bdc91c1ad2b4a49d991e305d881847ad192446`。已只读在线核对完整 tree 的 path、blob SHA-1、mode 与原 manifest 一致；API 未截断。
- 清单共 31 项；本轮拟核 27 项，排除 4 项。清单规范化 SHA-256：`c5521b0cec2eba3adaa8023e6956a0cf1673b68fc47e091c87e4e8958150cde0`。
- 检查编号、来源定位及证据线索与固定 templates.json、matrix.md 和工作表一致：共 15 项，无新增检查或排除项转入。
- subject.json、inventory.json、templates.json、原工作表、自动材料、P0 审计及既有历史保持原样；start 仅追加分配历史并把本轮推进至 in-review。未运行上游代码、未复制第三方全文入库。

## 逐项导航与待决问题

以下问题来自固定问题矩阵，全部由 fitalex 独立判断。链接只验证固定版本定位与清单归属；不代表规则内容、现行性或引用支持性已确认。每项完整法规线索见 [matrix.md](matrix.md)，查证后才可填写 authority_refs、推理、结论和 check_status。

| 检查 / 工作表 | 固定来源或证据入口 | 待本人核实的问题 | 状态 |
| --- | --- | --- | --- |
| [C01](workbook.md#c01) | [精确文件及 blob](evidence.md)；[全清单](inventory.json) | 固定版本与范围：复核下列候选、commit、入口及拟用清单；记录实际审阅文件及 blob | pending |
| [C02](workbook.md#c02) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[README.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/README.md) | 法域与事实：确认 CN-Mainland 及案件/合同地点、主体、行业、行为时间、判断时点；识别港澳台/涉外分支 | pending |
| [C03](workbook.md#c03) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[固定证据](evidence.md)；[法规线索](matrix.md) | 官方法律文本：按候选表中的任务核实每一引用，查找官方发布机关、文号、条款、原文和来源 URL | pending |
| [C04](workbook.md#c04) | [来源版本](subject.json)；[时效及过渡线索](matrix.md) | 法律时效：对每项核对公布/施行/修订/废止、替代文件、地方规则和过渡/溯及适用 | pending |
| [C05](workbook.md#c05) | [引用核实问题](matrix.md)；[固定来源](evidence.md) | 引用真实性与支持性：查条号/名称/原文是否真实，引用是否支持具体结论，是否遗漏例外或冲突 | pending |
| [C06](workbook.md#c06) | [专项高风险问题](matrix.md)；[工作包已知疑点](packet.md) | 风险与升级：使用独立合成/获授权脱敏场景检查下面高风险项、缺失事实、工具失效和旧法陷阱 | pending |
| [C07](workbook.md#c07) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[专项问题](matrix.md) | 人工裁决：对效力、收费、期限、重大交易、数据出境等问题明确人类决定点 | pending |
| [C08](workbook.md#c08) | [LICENSE](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE)；[精确排除清单](inventory.json) | 权利与用途：与许可审核人员确认本轮审核的精确文件、引用材料、拟用场景和排除项 | pending |
| [C09](workbook.md#c09) | [本人填写与签署程序](../../../../docs/review-workbench/MAINTAINER.md)；[身份区](workbook.md#signature) | 签署：由具备相应能力的人员自行填写真实身份、资质/专业经验、独立性、复核日期、意见、限制、实际时效核查基准及证据位置并签署 | pending |
| [C10](workbook.md#c10) | [原历史和四轴](record.json)；[更新及暂停程序](../../../../docs/review-workbench/MAINTAINER.md) | 不通过/更新：缺证则补证，法律错误则单独修正/缩范围后重审；根本不适用则保留拒绝/暂停原因 | pending |
| [CR01](workbook.md#cr01) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[references/financial-amounts.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/financial-amounts.md)；[references/risk-matrix.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/risk-matrix.md) | SKILL Step 2、financial-amounts、risk-matrix：违约金占合同价 30%、LPR 四倍、保证金 20% 是否被泛化；待确认：分清损失基数与合同价、借贷类型、利率时点、定金与保证金；阈值是风险提示还是强制规则，专家逐项决定 | pending |
| [CR02](workbook.md#cr02) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[references/law-sources.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/law-sources.md) **（排除，仅边界线索）** | law-sources、Step 4 的旧《合同法司法解释一》示例与预录法条回退；待确认：新旧法过渡、事实时间和条号逐项核对；检索失败不能以模型记忆确认现行法 | pending |
| [CR03](workbook.md#cr03) | [references/contract-types/construction-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/construction-contract.md)；[references/contract-types/employment-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/employment-contract.md)；[references/contract-types/equity-investment.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/equity-investment.md) | construction-contract、employment-contract、equity-investment 等专项结论；待确认：无资质/许可与合同效力、劳动保护、出资/治理与回购适用条件；不能一概断言无效 | pending |
| [CR04](workbook.md#cr04) | [references/compliance-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/compliance-checklist.md) | compliance-checklist 的数据、竞争、贿赂、行业许可、关联交易条目；待确认：监管义务与合同无效区分；数据处理合法基础、例外、行业和地方要求逐条确认 | pending |
| [CR05](workbook.md#cr05) | [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)；[references/text-quality-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/text-quality-checklist.md)；[scripts/parse_contract.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/parse_contract.py)；[scripts/check_text_quality.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/check_text_quality.py)；[scripts/annotate_docx.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/annotate_docx.py)；[references/contract-type-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-type-detection.md) | Word 批注、OCR、未检索成功、合同类型混合/未知；待确认：立场未经确认、关键数字识别错误、双侧条款错位可形成相反建议，须人工停止/升级 | pending |

## 范围边界与额外待决事项

- **CR02 / C03–C05：** references/law-sources.md 是排除文件。原矩阵引用它只是旧法和回退风险线索，本轮不对该文件作通过或托管判断；须在范围内核实 SKILL Step 4 是否依赖它及依赖缺失的后果。
- **跨境贸易 / C02、C07、C08：** references/contract-types/cross-border-trade.md 及二进制模板均排除。本人须判断排除后可支持的场景、涉外升级和使用限制；需要纳入时另立有依据的新范围与 Review，不把跨境条款视为已获批准。
- **CR01、CR03、CR05：** 分别核清违约金基数、利率时点和借贷类型、定金与保证金；合同效力和监管义务的关系；OCR 数字、立场和双侧条款错位的人工停止点。上述均为待核问题。

排除项的事实定位如下；完整 path/blob/理由以 inventory.json 为准：

| 原排除文件 | 原理由 basis |
| --- | --- |
| [.gitignore](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/.gitignore) **（排除，仅边界线索）** | `outside-proposed-package` |
| [assets/contract-review-template.docx](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/assets/contract-review-template.docx) **（排除，仅边界线索）** | `binary-provenance-unverified` |
| [references/contract-types/cross-border-trade.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/cross-border-trade.md) **（排除，仅边界线索）** | `third-party-trade-terms` |
| [references/law-sources.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/law-sources.md) **（排除，仅边界线索）** | `compiled-source-rights` |

## 待核证据线索与专业判断边界

- [matrix.md](matrix.md) 内法规名称和官方机关属于检索线索，尚未核实条文、施行/废止/修订日期、过渡规则或对本事实的支持性。
- 官方检索入口：[国家法律法规数据库](https://flk.npc.gov.cn/)、[最高人民法院](https://www.court.gov.cn/)、[司法部](https://www.moj.gov.cn/)、[国家网信办](https://www.cac.gov.cn/)、[市场监管总局](https://www.samr.gov.cn/)、[中国人民银行](https://www.pbc.gov.cn/)。这些门户链接不是已核验的法规引用；本人须留具体版本、条款和可追溯证据。
- 待本人提供：实际场景、主体、行业、地点和行为日期；适用法域与规范版本；逐项推理/结论、风险、补正、限制；受控身份/资质索引和利益冲突声明。
- regulatory_as_of、next_review_date、finding、authority_refs 和签署时间不由 Codex 代填；当前无法据此宣称专业通过。

## 填写后计算摘要与本人签署

本人提交工作表后通知 Codex；Codex 对当时实际 PR head 的工作表与 record 计算 Binding-SHA256，在线核对该 PR 的 main 基准作为 Policy-Base。当前不预填签署摘要，后续改动会改变摘要。

本人核对摘要后，通过 Files changed → Review changes → Comment → Submit review 提交真实 GitHub Comment Review，明确 LexRouter-Review、Role、Decision、Binding-SHA256、Policy-Base、Reason。Decision 按实际结果选择，不能预设通过。普通对话评论不作为签署事件。

把真实 `#pullrequestreview-事件ID` URL 交给 Codex 后，才进行在线身份、main 角色、权限、PR head 和精确摘要核验与串行同步；随后执行 `validate --online`。没有本人事件时不执行 sync、不生成签署快照。

professional_review、rights_review、engineering_review、admission_decision 各用独立新事件；同一事件不得跨角色复用。同一 Review 的写入、摘要和事件同步串行执行。当前各轴仍 pending / not-admitted，不归档、不合并本 PR、不正式入库。

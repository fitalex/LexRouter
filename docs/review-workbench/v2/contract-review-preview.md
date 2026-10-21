# Gate1 简化预览：通用合同审查

**预审草稿 · not-verified · 0 真人签署 · 未批准托管/入库。** 五组阅读入口不减少逐项检查；Gate1只评估界面、映射和工程方案，不产生专业意见。

- Candidate `discovery-contract-review`；Review `RV-20261017-contract-review`；[固定来源入口](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)。
- 上游版本 `f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`；PR #9 预审head `a7c7d9541e0f6b84a30d5643890de59ed4673a7b`（Draft/open/in-review，0真人签署）。
- main基线 `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8` 的case仍evidence-ready。以上是任务固定快照，不声称实时状态。
- 原始[subject](../../../data/reviews/cases/RV-20261017-contract-review/subject.json)、[矩阵](../../../data/reviews/cases/RV-20261017-contract-review/matrix.md)、[完整manifest](../../../data/reviews/manifests/discovery-contract-review.json)均保持原状。
- 官方链接沿用原交接包入口，**本轮未逐一访问核实**；不是具体已核法条。官方文号/条款/版本/有效期间及受控授权链仍缺，全部 `not-verified`。支持与反例均为原创待验证场景，不是实际运行证据。

## 五组阅读入口

### G1 范围、事实与权利

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C01, C02, C08 |
| 待核问题 | 逐文件核对拟用场景、主体、地点、立场与授权链；大陆法域声明待专家确认。 27文件；跨境术语、law-sources及二进制模板不纳入。只读争议线索不授予复制许可。 |
| 官方来源/证据线索 | 固定manifest和受控授权链索引；[人大数据库](https://flk.npc.gov.cn/)：法域相关规则待查。 |
| 适用时点 | 成立、履行、争议发生及拟用时间均待提供。 |
| 支持与反例待验证 | 支持：事实齐全的境内场景；反例：涉外事项或排除材料被默认纳入。 |
| 待补正 | 补逐文件用途、事实与授权链，MIT/Apache标签不证明第三方材料权利。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G2 法源、时效与引用

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C03, C04, C05, CR02 |
| 待核问题 | 每项核实官方原文、条款、规范层级、版本与具体命题支持关系。 CR02：旧《合同法司法解释一》与预录法条回退需核新旧法。law-sources是排除文件，只作风险线索。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)：民法典；[最高法](https://www.court.gov.cn/)：民法典时间效力、合同编通则及旧司法解释废止文件。 |
| 适用时点 | 公布、施行、修订、废止、事实跨新旧法的过渡均待核。 |
| 支持与反例待验证 | 支持：条款版本与事实吻合；反例：真实旧条号用于新事实，或引用真实但不支持命题。 |
| 待补正 | 补具体官方URL、文号、条款、版本/哈希、过渡推理和反例；门户入口不能填作已核authority。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G3 业务法律判断

| 项目 | 内容 |
| --- | --- |
| 完整映射 | CR01, CR03 |
| 待核问题 | 逐项拆分业务前提、规则、例外和后果，由专家判断。 CR01：核30%、LPR四倍、20%阈值，区分损失/合同价、借贷类型、利率时点、定金/保证金；CR03：施工资质、劳动保护、出资治理分别判断。反例：保证金一律套定金或无许可一律无效。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)：民法典、建筑法、劳动合同法、公司法；[最高法](https://www.court.gov.cn/)：民间借贷、合同编通则、公司法时间效力等司法解释。 |
| 适用时点 | 合同、行为、履行或争议等事实时点分别匹配适用版本，当前均未核。 |
| 支持与反例待验证 | 支持：满足具体规则前提的独立合成情景；反例：省略例外、跨领域泛化或绝对效力判断。 |
| 待补正 | 补事实→官方条文→适用推理→结论/限制，每个专项分别留证。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G4 监管、输出与失败升级

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C06, CR04, CR05 |
| 待核问题 | 区分监管义务、法律效力和工程成功；用独立合成场景审查缺信息、工具失败及高风险输出。 CR04：数据、竞争、贿赂、许可、关联交易规则逐项；CR05：OCR漏小数点、混合劳动/技术合同、双侧批注错位。专业判断不由Word成功生成替代。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)、[网信办](https://www.cac.gov.cn/)、[市场监管总局](https://www.samr.gov.cn/)：数据、竞争、行业规则；OCR/原段落对照证据另备。 |
| 适用时点 | 业务发生时点、行业/地方规定及运行版本待核；本轮未运行上游。 |
| 支持与反例待验证 | 支持：证据可追溯且失败能停止；反例：检索失败、缺库或OCR错误后模型补全确定结论。 |
| 待补正 | 补停止/升级点、缺事实清单及另获授权的实际运行证据，不能把预想场景写作已通过测试。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G5 真人裁决、签署与更新

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C07, C09, C10 |
| 待核问题 | 专家作专业决定，维护者另作独立入库决定；保存补正、拒绝和变化记录。 重大交易、行业资质、劳动保护、涉外与数据/反垄断事项须真人裁决。 |
| 官方来源/证据线索 | main角色政策与受控能力/资质索引；法律依据使用各组实际核实结果。 |
| 适用时点 | 本人复核日、实际法规核查基准、下次复核日期由本人填写，当前未提供。 |
| 支持与反例待验证 | 支持：精确范围及未决项可追溯；反例：工程绿灯、输出文件或上游作者身份代替本人判断。 |
| 待补正 | 补能力/资质受控索引、利益冲突、逐组理由及更新安排；不预填通过、签署或法规日期。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

## 逐项无损映射

每项保留独立判断；组意见不得遮盖组内未核项。详细证据按检查项ID追加到附件。

| 检查项 | 组 | 原问题 | 当前状态 |
| --- | --- | --- | --- |
| C01 | G1 | 固定版本与范围：复核下列候选、commit、入口及拟用清单；记录实际审阅文件及 blob | not-verified |
| C02 | G1 | 法域与事实：确认 CN-Mainland 及案件/合同地点、主体、行业、行为时间、判断时点；识别港澳台/涉外分支 | not-verified |
| C03 | G2 | 官方法律文本：按候选表中的任务核实每一引用，查找官方发布机关、文号、条款、原文和来源 URL | not-verified |
| C04 | G2 | 法律时效：对每项核对公布/施行/修订/废止、替代文件、地方规则和过渡/溯及适用 | not-verified |
| C05 | G2 | 引用真实性与支持性：查条号/名称/原文是否真实，引用是否支持具体结论，是否遗漏例外或冲突 | not-verified |
| C06 | G4 | 风险与升级：使用独立合成/获授权脱敏场景检查下面高风险项、缺失事实、工具失效和旧法陷阱 | not-verified |
| C07 | G5 | 人工裁决：对效力、收费、期限、重大交易、数据出境等问题明确人类决定点 | not-verified |
| C08 | G1 | 权利与用途：与许可审核人员确认本轮审核的精确文件、引用材料、拟用场景和排除项 | not-verified |
| C09 | G5 | 签署：由具备相应能力的人员自行填写真实身份、资质/专业经验、独立性、复核日期、意见、限制、实际时效核查基准及证据位置并签署 | not-verified |
| C10 | G5 | 不通过/更新：缺证则补证，法律错误则单独修正/缩范围后重审；根本不适用则保留拒绝/暂停原因 | not-verified |
| CR01 | G3 | SKILL Step 2、financial-amounts、risk-matrix：违约金占合同价 30%、LPR 四倍、保证金 20% 是否被泛化；待确认：分清损失基数与合同价、借贷类型、利率时点、定金与保证金；阈值是风险提示还是强制规则，专家逐项决定 | not-verified |
| CR02 | G2 | law-sources、Step 4 的旧《合同法司法解释一》示例与预录法条回退；待确认：新旧法过渡、事实时间和条号逐项核对；检索失败不能以模型记忆确认现行法 | not-verified |
| CR03 | G3 | construction-contract、employment-contract、equity-investment 等专项结论；待确认：无资质/许可与合同效力、劳动保护、出资/治理与回购适用条件；不能一概断言无效 | not-verified |
| CR04 | G4 | compliance-checklist 的数据、竞争、贿赂、行业许可、关联交易条目；待确认：监管义务与合同无效区分；数据处理合法基础、例外、行业和地方要求逐条确认 | not-verified |
| CR05 | G4 | Word 批注、OCR、未检索成功、合同类型混合/未知；待确认：立场未经确认、关键数字识别错误、双侧条款错位可形成相反建议，须人工停止/升级 | not-verified |

## 固定文件范围：27项

仅表示拟审，不表示有权托管或运行；缩放范围须新Review。

| 路径 | 固定blob |
| --- | --- |
| `LICENSE` | `1c3ef4997530ff41a93fb627c8f6d31d85d7a2cd` |
| `README.md` | `ff190f543bc43ec46a066f421f844f90b505b58b` |
| `SKILL.md` | `b1e3ff93439c32bcc142a241ddf400b22e13ede1` |
| `references/clause-checklist.md` | `15f247b38551804b153f5be6e2a30c558b65ecea` |
| `references/clause-conflict-detection.md` | `22bc2abf55106a709d7db1e88da5ed9b5e62e3fc` |
| `references/compliance-checklist.md` | `145450bb3055d4a7330a664de7f902ef5c718cd4` |
| `references/contract-type-detection.md` | `325dd064c34dbe57474eccdb68fbdbfe57bedf96` |
| `references/contract-types/construction-contract.md` | `41af20f0adc57ad271662f1ac46fb544b323f37f` |
| `references/contract-types/employment-contract.md` | `a30eb80a0d854677e42171aaac80b3c8a444eb04` |
| `references/contract-types/equity-investment.md` | `16d9fdb8f2bc2c1e3caf4b1bfeb0d1cc93ff9fef` |
| `references/contract-types/lease-contract.md` | `dfd5559c077f95005d2e33e188e62e4969ca919d` |
| `references/contract-types/nda.md` | `b699c921e690c261703e0445e3684a905519ac8b` |
| `references/contract-types/oem-contract.md` | `19da12381d0d73b47475feaa862d65a88239cb88` |
| `references/contract-types/purchase-contract.md` | `2ba4532a0627799c199cb8186af4bc52fa15a2bb` |
| `references/contract-types/sales-contract.md` | `6b161e6fe9532488bb8680abc8ee2c4f5812edb0` |
| `references/contract-types/service-contract.md` | `8ea22053f06a0ba06f1d49bfdd4ef22c08d863f9` |
| `references/contract-types/tech-development-contract.md` | `3e5702b24e273060986ce0318c8803c223897bf8` |
| `references/financial-amounts.md` | `dfbfef2cb62d6efc2dbbef115d12504a091f1185` |
| `references/output-format.md` | `15aa409098c69e1307fb996953c08474326b27dd` |
| `references/risk-matrix.md` | `520fcb32d222d6a1f9b1d201adef46ac67c24544` |
| `references/terminology-glossary.md` | `da077d77f916cbe9d7d655c547c5ffd804e2d1b9` |
| `references/text-quality-checklist.md` | `a611562e4305932a90a9b8ce6c05b65cd23505f5` |
| `scripts/annotate_docx.py` | `f2208af68551d02ebcac2bd17a6665448d3d1d0b` |
| `scripts/check_text_quality.py` | `7695b6c3165c1c03085de46bdc91320b3ab2817f` |
| `scripts/detect_contract_type.py` | `ad683d1e51fc6470578c493079d9e3d84515d7ce` |
| `scripts/parse_contract.py` | `52eb35dd5b371b6dbbc6739c4eb815e1ba11348a` |
| `scripts/validate.py` | `dd3dfd8dde95dcf2fe6c69a923735961b66bc5d0` |

排除4项；只读风险线索不扩大审核/复制/运行范围。

| 排除路径 | 原决定 |
| --- | --- |
| `.gitignore` | `exclude-from-hosting` |
| `assets/contract-review-template.docx` | `unverified` |
| `references/contract-types/cross-border-trade.md` | `requires-authorization` |
| `references/law-sources.md` | `requires-authorization` |

## 实际填写

使用[四块专家短表](EXPERT_SHORT_FORM.md)。工程人员生成Review-ID、完整Scope和G1–G5；专家填组意见、总体理由/限制、利益冲突及实际时效基准，本人提交Comment Review。维护者另作独立入库事件，权利证据供其判断，不增加第三次rights签署。

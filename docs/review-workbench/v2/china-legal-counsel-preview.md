# Gate1 简化预览：企业法务组件

**预审草稿 · not-verified · 0 真人签署 · 未批准托管/入库。** 五组阅读入口不减少逐项检查；Gate1只评估界面、映射和工程方案，不产生专业意见。

- Candidate `discovery-china-legal-counsel`；Review `RV-20261017-china-legal-counsel`；[固定来源入口](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md)。
- 上游版本 `73ff53a857ffbdd91296bf41ed5bcc1294bc2042`；PR #11 预审head `844c9dd68b0061ea9f4451fd89e24cc10d73f3bb`（Draft/open/in-review，0真人签署）。
- main基线 `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8` 的case仍evidence-ready。以上是任务固定快照，不声称实时状态。
- 原始[subject](../../../data/reviews/cases/RV-20261017-china-legal-counsel/subject.json)、[矩阵](../../../data/reviews/cases/RV-20261017-china-legal-counsel/matrix.md)、[完整manifest](../../../data/reviews/manifests/discovery-china-legal-counsel.json)均保持原状。
- 官方链接沿用原交接包入口，**本轮未逐一访问核实**；不是具体已核法条。官方文号/条款/版本/有效期间及受控授权链仍缺，全部 `not-verified`。支持与反例均为原创待验证场景，不是实际运行证据。

## 五组阅读入口

### G1 范围、事实与权利

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C01, C02, C08 |
| 待核问题 | 逐文件核对拟用场景、主体、地点、立场与授权链；大陆法域声明待专家确认。 19组件；2320文件（含2316知识库文件）排除。补Suze与发布者/贡献者关系；库、商业数据库、律所文章、品牌图像不随MIT授权。 |
| 官方来源/证据线索 | 固定manifest和受控发布者/贡献者授权链索引；[人大数据库](https://flk.npc.gov.cn/)中各业务依据待查。 |
| 适用时点 | 成立、履行、争议发生及拟用时间均待提供。 |
| 支持与反例待验证 | 支持：事实齐全的境内场景；反例：涉外事项或排除材料被默认纳入。 |
| 待补正 | 补逐文件用途、事实与授权链，MIT/Apache标签不证明第三方材料权利。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G2 法源、时效与引用

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C03, C04, C05, CN05 |
| 待核问题 | 每项核实官方原文、条款、规范层级、版本与具体命题支持关系。 CN05：verify_citations.py字符串命中不证明引用真实、现行或支持结论；source-registry自述现行与日期均待核。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)、[中国政府网政策库](https://www.gov.cn/zhengce/)、[最高法](https://www.court.gov.cn/)、[人民法院案例库](https://rmfyalk.court.gov.cn/)：每条引用对应官方原文。 |
| 适用时点 | 公布、施行、修订、废止、事实跨新旧法的过渡均待核。 |
| 支持与反例待验证 | 支持：条款版本与事实吻合；反例：真实旧条号用于新事实，或引用真实但不支持命题。 |
| 待补正 | 补具体官方URL、文号、条款、版本/哈希、过渡推理和反例；门户入口不能填作已核authority。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G3 业务法律判断

| 项目 | 内容 |
| --- | --- |
| 完整映射 | CN01, CN04 |
| 待核问题 | 逐项拆分业务前提、规则、例外和后果，由专家判断。 CN01：合同效力、授权、格式条款、责任、出资/治理分别匹配时间；CN04：劳动及并购融资、刑事/监管/证券事项保留升级。反例：旧公司法事实一律套新法或知识库有材料便取消升级。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)：民法典、公司法、劳动合同法；[最高法](https://www.court.gov.cn/)：合同编通则与公司法时间效力解释；[人社部](https://www.mohrss.gov.cn/)及地方规则。 |
| 适用时点 | 合同、行为、履行或争议等事实时点分别匹配适用版本，当前均未核。 |
| 支持与反例待验证 | 支持：满足具体规则前提的独立合成情景；反例：省略例外、跨领域泛化或绝对效力判断。 |
| 待补正 | 补事实→官方条文→适用推理→结论/限制，每个专项分别留证。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G4 监管、输出与失败升级

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C06, CN02, CN03, CN06 |
| 待核问题 | 区分监管义务、法律效力和工程成功；用独立合成场景审查缺信息、工具失败及高风险输出。 CN02：数据角色/规模/流向、生成式AI、算法、标识各核生效/过渡；CN03：广告、医美、IP与许可分别核；CN06：缺库/陈旧/冲突/路径失效需无法判断。反例：敏感信息出境按一般处理、医疗宣传套普通模板、缺库后补全。TLS放宽回退另行工程审查，本轮不运行。 |
| 官方来源/证据线索 | [人大数据库](https://flk.npc.gov.cn/)、[政府政策库](https://www.gov.cn/zhengce/)、[网信办](https://www.cac.gov.cn/)、[市场监管总局](https://www.samr.gov.cn/)、[国家知识产权局](https://www.cnipa.gov.cn/)：数据/AI、广告、医疗宣传、IP及行业规则。 |
| 适用时点 | 业务发生时点、行业/地方规定及运行版本待核；本轮未运行上游。 |
| 支持与反例待验证 | 支持：证据可追溯且失败能停止；反例：检索失败、缺库或OCR错误后模型补全确定结论。 |
| 待补正 | 补停止/升级点、缺事实清单及另获授权的实际运行证据，不能把预想场景写作已通过测试。 |
| 当前状态 | not-verified；专业、授权及实际运行结论均未作出 |
| 专家填写 | 结论〈待填〉；事实→条文→推理〈待填〉；限制〈待填〉；支持/反例证据索引〈待填〉；未决和处理〈待填〉 |

### G5 真人裁决、签署与更新

| 项目 | 内容 |
| --- | --- |
| 完整映射 | C07, C09, C10 |
| 待核问题 | 专家作专业决定，维护者另作独立入库决定；保存补正、拒绝和变化记录。 签署必须明确19组件而非数据库；重大数据、监管、刑事、证券、并购和证据保全事项真人承接。 |
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
| CN01 | G3 | contract-review / contract-drafting playbooks；待确认：合同效力、授权、格式条款、违约责任、公司治理和出资义务，分别匹配事实时点 | not-verified |
| CN02 | G4 | compliance-check-playbook 的 AI、数据、广告流程；待确认：生效、修订及过渡逐条确认；区分公开内容生成、算法、数据角色/规模和境内外流向 | not-verified |
| CN03 | G4 | 广告、知识产权、医美与平台检查；待确认：广告功效/禁限语、内容标识、授权链、生成内容版权和行业准入不能用通用规则代替 | not-verified |
| CN04 | G3 | 劳动、公司与升级规则；待确认：劳动争议与并购融资、刑事/监管/证券等事项的人工边界；不因知识库有材料而取消升级 | not-verified |
| CN05 | G2 | citation-verification、source-registry、verify_citations.py；待确认：本地字符串命中不等于引用真实、有效或支持结论；库中自称“现行”或日期不作时效确认 | not-verified |
| CN06 | G4 | KB 缺失、陈旧或冲突；本机路径失效；待确认：无库/联网失败须标无法判断；明确缩范围后还能完成哪些任务，不把部分组件签署为完整工作流 | not-verified |

## 固定文件范围：19项

仅表示拟审，不表示有权托管或运行；缩放范围须新Review。

| 路径 | 固定blob |
| --- | --- |
| `LICENSE` | `135c200182eb6e3d75ca3ef618ab7af43e6d7e7e` |
| `README.md` | `a7cfca9e87278ee5ab789a53d55b462d89b862a0` |
| `SKILL.md` | `7cc17878ab5bca101ec178dd97e682134b0fd0eb` |
| `agents/openai.yaml` | `6bf57974d50df52c44ca9645a57b38ae8b772d85` |
| `references/citation-verification.md` | `3f1b74fbe7b556b84a8c738eddae1305d07d1477` |
| `references/compliance-check-playbook.md` | `030f86d67ff48251896a1264359c79cff7fe8807` |
| `references/contract-drafting-playbook.md` | `527550a67d884651f24155970093de9daa3f8ba4` |
| `references/contract-review-playbook.md` | `9af8dfc9be9365c3dea7facd1467199fc5282fd2` |
| `references/eval-plan.md` | `52c0e2c63cfd4f6b71500c783362ae691e145bdf` |
| `references/legal-consultation-playbook.md` | `45a2068c4a91847ab38cba27dd9343551b2bfe57` |
| `references/output-schemas.md` | `77b5bfcd7ab4d9e49a711a9905f3f9047e915527` |
| `references/risk-and-escalation.md` | `b176f4020b6c99be84660e987c07011952e27637` |
| `references/source-registry.md` | `ce6d721231ddc7a1dbc2533b9dd0e7180d718902` |
| `scripts/chunk_legal_doc.py` | `5ca2fbc5dd09e4e9bcf6531d1623657773ce44c0` |
| `scripts/fetch_official_sources.py` | `1ec5d83fe0cda2082a66cae256ba1b053ed55352` |
| `scripts/ingest_source_registry.py` | `30dd2b39c8f4ed02ae71d2844e60cb6aff1d8e59` |
| `scripts/kb_search.py` | `b2f9327efa38ebf5323c875b3cce40975001f68a` |
| `scripts/normalize_legal_doc.py` | `76cc45ee3b281c4137b3f24cdecb1a434d6628df` |
| `scripts/verify_citations.py` | `3c6ace00ea9e72fa99e1df9ce3376ac1ff8f4d87` |

排除2320项；只读风险线索不扩大审核/复制/运行范围。
其中知识库2316项；所有排除项由完整manifest持续保留，不能签成数据库已审。

## 实际填写

使用[四块专家短表](EXPERT_SHORT_FORM.md)。工程人员生成Review-ID、完整Scope和G1–G5；专家填组意见、总体理由/限制、利益冲突及实际时效基准，本人提交Comment Review。维护者另作独立入库事件，权利证据供其判断，不增加第三次rights签署。

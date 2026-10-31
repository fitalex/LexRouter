# Gate 2：通用合同审查

**材料适配／not-verified／0 真人事件；未批准托管、运行或入库。**

Review `RV-20261017-contract-review`；Candidate `discovery-contract-review`；[原PR #9](https://github.com/fitalex/LexRouter/pull/9)。固定上游 `f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`；main `d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`。本页五组保留全部 15 检查项，27 文件 × 15 = **405** 行；排除 4 文件。

[四块短表](expert-form.md) · [权利/工程预审与待确认](precheck.md) · [v1兼容性](compatibility.md) · [验证说明](VALIDATION.md) · [真实日志](TEST_OUTPUT.md) · [具体官方来源与时间问题](sources.md) · [专家指南](../EXPERT_GUIDE.md) · [完整bundle](../../../../../data/reviews/v2/RV-20261017-contract-review/bundle.json) · [空ledger](../../../../../data/reviews/v2/RV-20261017-contract-review/ledger.json)。

官方页面标题/文号/公布施行日期的检索记录是 **source_metadata**，不等于专业审核。逐行法律事实、适用、有效期间与过渡全部未核；本轮未执行上游，也未新读全部文件全文。原manifest的read/static-scan只描述原预审，不能升格为本轮专业核法。支持/反例是原创待验证问题，并非实测结果。

## G1 范围、事实与权利

| 项目 | 待本人核实 |
| --- | --- |
| 完整映射 | C01, C02, C08 |
| 待核问题 | 逐文件核对拟用场景、主体、地点、立场与授权链；大陆法域声明待专家确认。 27文件；跨境术语、law-sources及二进制模板不纳入。只读争议线索不授予复制许可。 |
| 适用时点 | 成立、履行、争议发生及拟用时间均待提供。 |
| 支持与反例待验证 | 支持：事实齐全的境内场景；反例：涉外事项或排除材料被默认纳入。 |
| 待补正 | 补逐文件用途、事实与授权链，MIT/Apache标签不证明第三方材料权利。 |
| 来源索引 | [CA01](sources.md#ca01)；[CA02](sources.md#ca02)；[CA03](sources.md#ca03)；[CA04](sources.md#ca04)；[CA05](sources.md#ca05)；[CA06](sources.md#ca06)；[CA07](sources.md#ca07)；[CA08](sources.md#ca08)；[CA09](sources.md#ca09)；[CA10](sources.md#ca10)；[CA11](sources.md#ca11)；[CA12](sources.md#ca12)；[CA13](sources.md#ca13)；[CA14](sources.md#ca14)；[CA15](sources.md#ca15)；[CA16](sources.md#ca16)；[CA17](sources.md#ca17)；[CA18](sources.md#ca18)；[CA19](sources.md#ca19)；[CA20](sources.md#ca20) |
| 时间与版本 | not-verified；逐法公布/施行/修订线索及待核过渡见sources；须与本组每条矩阵事实对应 |
| 当前状态 | 全部not-verified；本人组决定、理由和限制留空 |

本组逐检查项研究入口（全部为待验证问题；非充分法源清单）：

| check_id | 具体来源、条款与时间线索 | 支持／反例及未决 |
| --- | --- | --- |
| C01 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 固定manifest/文件blob由工程工作项核，本catalog不证明已逐文件审阅。 |
| C02 | [CA01 文号未取证](https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212250/content.html)；第153、154条；第496—498条；第502条；第584—588条；第680条；第791、793条；第919、923、928、933条；第1260条；公布2020-05-28／施行2021-01-01；第1260条同时废止合同法等旧法；须联读CA02，不能据审查日替代法律事实日。；[CA02 法释〔2020〕15号](https://www.court.gov.cn/shenpan/xiangqing/282051.html)；第1—5条；第8、9、20条；第28条；公布2020-12-29／施行2021-01-01；区分施行前、施行后及持续事实；第8、9条有具体溯及规则，第20条区分合同履行时段；已终审再审另核。 | CA01：待专家验证：20%针对定金；解除、损失、格式条款分别检验。 待验证反例：所有保证金限20%；随时解除等于全部退费；行业违规即合同无效。；CA02：支持场景待验证：分段识别跨2021年的履行。 反例待验证：2026审查便一律使用新法。；需主体身份、交易立场、地点、行业、行为/履行/争议时间及涉外因素 |
| C08 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 法源不是第三方Skill版权授权；排除材料仅风险线索。 |

## G2 法源、时效与引用

| 项目 | 待本人核实 |
| --- | --- |
| 完整映射 | C03, C04, C05, CR02 |
| 待核问题 | 每项核实官方原文、条款、规范层级、版本与具体命题支持关系。 CR02：旧《合同法司法解释一》与预录法条回退需核新旧法。law-sources是排除文件，只作风险线索。 |
| 适用时点 | 公布、施行、修订、废止、事实跨新旧法的过渡均待核。 |
| 支持与反例待验证 | 支持：条款版本与事实吻合；反例：真实旧条号用于新事实，或引用真实但不支持命题。 |
| 待补正 | 补具体官方URL、文号、条款、版本/哈希、过渡推理和反例；门户入口不能填作已核authority。 |
| 来源索引 | [CA01](sources.md#ca01)；[CA02](sources.md#ca02)；[CA03](sources.md#ca03)；[CA04](sources.md#ca04)；[CA05](sources.md#ca05)；[CA06](sources.md#ca06)；[CA07](sources.md#ca07)；[CA08](sources.md#ca08)；[CA09](sources.md#ca09)；[CA10](sources.md#ca10)；[CA11](sources.md#ca11)；[CA12](sources.md#ca12)；[CA13](sources.md#ca13)；[CA14](sources.md#ca14)；[CA15](sources.md#ca15)；[CA16](sources.md#ca16)；[CA17](sources.md#ca17)；[CA18](sources.md#ca18)；[CA19](sources.md#ca19)；[CA20](sources.md#ca20) |
| 时间与版本 | not-verified；逐法公布/施行/修订线索及待核过渡见sources；须与本组每条矩阵事实对应 |
| 当前状态 | 全部not-verified；本人组决定、理由和限制留空 |

本组逐检查项研究入口（全部为待验证问题；非充分法源清单）：

| check_id | 具体来源、条款与时间线索 | 支持／反例及未决 |
| --- | --- | --- |
| C03 | [CA01 文号未取证](https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212250/content.html)；第153、154条；第496—498条；第502条；第584—588条；第680条；第791、793条；第919、923、928、933条；第1260条；公布2020-05-28／施行2021-01-01；第1260条同时废止合同法等旧法；须联读CA02，不能据审查日替代法律事实日。；[CA03 法释〔2023〕13号](https://www.court.gov.cn/fabu/xiangqing/419382.html)；第1条；第9—10条；第16—17条；第64—69条；公布2023-12-04／施行2023-12-05；第69条指向民法典施行后的法律事实及本解释施行后尚未终审案件；解释施行前已终审再审不适用。 | CA01：待专家验证：20%针对定金；解除、损失、格式条款分别检验。 待验证反例：所有保证金限20%；随时解除等于全部退费；行业违规即合同无效。；CA03：待验证：第65条30%以损失为基数；第67条识别保证金与定金。 反例待验证：违约金超过合同价30%即无效；保证金自动适用定金罚则。；需本文件实际引用的完整命题、条号、规范层级及官方原文逐条对照 |
| C04 | [CA02 法释〔2020〕15号](https://www.court.gov.cn/shenpan/xiangqing/282051.html)；第1—5条；第8、9、20条；第28条；公布2020-12-29／施行2021-01-01；区分施行前、施行后及持续事实；第8、9条有具体溯及规则，第20条区分合同履行时段；已终审再审另核。；[CA03 法释〔2023〕13号](https://www.court.gov.cn/fabu/xiangqing/419382.html)；第1条；第9—10条；第16—17条；第64—69条；公布2023-12-04／施行2023-12-05；第69条指向民法典施行后的法律事实及本解释施行后尚未终审案件；解释施行前已终审再审不适用。；[CA13 法释〔2024〕7号](https://www.court.gov.cn/zixun/xiangqing/436481.html)；第1—8条；公布2024-06-29／施行2024-07-01；区分行为效力、合同履行、空白、细化及已终审；不能只按公司成立日选择整部法。 | CA02：支持场景待验证：分段识别跨2021年的履行。 反例待验证：2026审查便一律使用新法。；CA03：待验证：第65条30%以损失为基数；第67条识别保证金与定金。 反例待验证：违约金超过合同价30%即无效；保证金自动适用定金罚则。；CA13：待验证：按具体行为和争点选择过渡分支。 反例待验证：合同签订早于2024就排除所有新法规则。；需每条命题的事实发生时间、版本起止和新旧法衔接条件 |
| C05 | [CA03 法释〔2023〕13号](https://www.court.gov.cn/fabu/xiangqing/419382.html)；第1条；第9—10条；第16—17条；第64—69条；公布2023-12-04／施行2023-12-05；第69条指向民法典施行后的法律事实及本解释施行后尚未终审案件；解释施行前已终审再审不适用。；[CA06 2020年第二次修正；修正决定文号见CA07](https://cicc.court.gov.cn/html/1/218/62/84/12844.html)；第1、13、25、29、31条；公布未取证／施行2021-01-01；第31条涉及2020-08-20新受理一审及旧借款分段计息；不能把成立时LPR和起诉时特别过渡混同。 | CA03：待验证：第65条30%以损失为基数；第67条识别保证金与定金。 反例待验证：违约金超过合同价30%即无效；保证金自动适用定金罚则。；CA06：待验证：第25条成立时一年期LPR四倍，结合第29条费用合计及第31条。 反例待验证：所有商业合同一律四倍LPR；用今日LPR计算历史合同。；需本文件具体结论与引文的推理链、适用条件、例外和冲突证据 |
| CR02 | [CA02 法释〔2020〕15号](https://www.court.gov.cn/shenpan/xiangqing/282051.html)；第1—5条；第8、9、20条；第28条；公布2020-12-29／施行2021-01-01；区分施行前、施行后及持续事实；第8、9条有具体溯及规则，第20条区分合同履行时段；已终审再审另核。；[CA03 法释〔2023〕13号](https://www.court.gov.cn/fabu/xiangqing/419382.html)；第1条；第9—10条；第16—17条；第64—69条；公布2023-12-04／施行2023-12-05；第69条指向民法典施行后的法律事实及本解释施行后尚未终审案件；解释施行前已终审再审不适用。；[CA04 法释〔2020〕16号](https://www.court.gov.cn/fabu/xiangqing/282061.html)；决定正文；附件116件目录（图片未逐项转录）；公布2020-12-29／施行2021-01-01；合同法解释一、二的废止由CA05官方答问交叉支持；旧事实适用仍须CA02；附件序号未核。；[CA05 文号未取证](https://www.court.gov.cn/zixun/xiangqing/419402.html)；关于合同法解释一、二清理废止的答问；公布2023-12-05／施行未取证或无独立施行日；答问明确116件废止文件含合同法解释一、二；仍以决定和时间效力规则为准。 | CA02：支持场景待验证：分段识别跨2021年的履行。 反例待验证：2026审查便一律使用新法。；CA03：待验证：第65条30%以损失为基数；第67条识别保证金与定金。 反例待验证：违约金超过合同价30%即无效；保证金自动适用定金罚则。；CA04：待验证：对旧法引用加废止及时间适用检查。 反例待验证：官方旧页面可访问即现行。；CA05：待验证：用作识别废止链的辅助证据。 反例待验证：答记者问代替具体法条或裁判。；需合同成立/履行/争议日期及旧解释所支持的具体命题；检索失败不能补造现行法 |

## G3 业务法律判断

| 项目 | 待本人核实 |
| --- | --- |
| 完整映射 | CR01, CR03 |
| 待核问题 | 逐项拆分业务前提、规则、例外和后果，由专家判断。 CR01：核30%、LPR四倍、20%阈值，区分损失/合同价、借贷类型、利率时点、定金/保证金；CR03：施工资质、劳动保护、出资治理分别判断。反例：保证金一律套定金或无许可一律无效。 |
| 适用时点 | 合同、行为、履行或争议等事实时点分别匹配适用版本，当前均未核。 |
| 支持与反例待验证 | 支持：满足具体规则前提的独立合成情景；反例：省略例外、跨领域泛化或绝对效力判断。 |
| 待补正 | 补事实→官方条文→适用推理→结论/限制，每个专项分别留证。 |
| 来源索引 | [CA01](sources.md#ca01)；[CA03](sources.md#ca03)；[CA06](sources.md#ca06)；[CA07](sources.md#ca07)；[CA08](sources.md#ca08)；[CA09](sources.md#ca09)；[CA10](sources.md#ca10)；[CA11](sources.md#ca11)；[CA12](sources.md#ca12)；[CA13](sources.md#ca13)；[CA14](sources.md#ca14) |
| 时间与版本 | not-verified；逐法公布/施行/修订线索及待核过渡见sources；须与本组每条矩阵事实对应 |
| 当前状态 | 全部not-verified；本人组决定、理由和限制留空 |

本组逐检查项研究入口（全部为待验证问题；非充分法源清单）：

| check_id | 具体来源、条款与时间线索 | 支持／反例及未决 |
| --- | --- | --- |
| CR01 | [CA01 文号未取证](https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212250/content.html)；第153、154条；第496—498条；第502条；第584—588条；第680条；第791、793条；第919、923、928、933条；第1260条；公布2020-05-28／施行2021-01-01；第1260条同时废止合同法等旧法；须联读CA02，不能据审查日替代法律事实日。；[CA03 法释〔2023〕13号](https://www.court.gov.cn/fabu/xiangqing/419382.html)；第1条；第9—10条；第16—17条；第64—69条；公布2023-12-04／施行2023-12-05；第69条指向民法典施行后的法律事实及本解释施行后尚未终审案件；解释施行前已终审再审不适用。；[CA06 2020年第二次修正；修正决定文号见CA07](https://cicc.court.gov.cn/html/1/218/62/84/12844.html)；第1、13、25、29、31条；公布未取证／施行2021-01-01；第31条涉及2020-08-20新受理一审及旧借款分段计息；不能把成立时LPR和起诉时特别过渡混同。；[CA07 文号未取证](https://www.court.gov.cn/zixun/xiangqing/282621.html)；民间借贷规定修改及重新公布部分；公布未取证／施行2021-01-01；为CA06二次修正链线索，具体公告日期及文号待补正文取证。 | CA01：待专家验证：20%针对定金；解除、损失、格式条款分别检验。 待验证反例：所有保证金限20%；随时解除等于全部退费；行业违规即合同无效。；CA03：待验证：第65条30%以损失为基数；第67条识别保证金与定金。 反例待验证：违约金超过合同价30%即无效；保证金自动适用定金罚则。；CA06：待验证：第25条成立时一年期LPR四倍，结合第29条费用合计及第31条。 反例待验证：所有商业合同一律四倍LPR；用今日LPR计算历史合同。；CA07：待验证：回查二次修正及过渡条。 反例待验证：仅2015版仍支持2026结论。；需损失与合同价基数、借贷主体/性质、利率时点以及定金或保证金的真实约定 |
| CR03 | [CA08 法释〔2020〕25号](https://www.sdcourt.gov.cn/dzkfqfy/1758157/1758167/6789478/index.html)；第1、3—7、45条；公布2020-12-29／施行2021-01-01；与民法典时间效力及旧施工解释废止链联读；不能仅由本页状态认定历史案件适用。；[CA10 文号未取证](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)；第2、9、22—28、38、42、46、47、97条；公布2012-12-28／施行未取证或无独立施行日；区分原法2008施行、2012修正及2025解释二；本页不能自动证明所有条款同时在2013变更。；[CA11 法释〔2025〕12号](https://www.court.gov.cn/zixun/xiangqing/472691.html)；第1—3、13—15、19、21条；公布2025-07-31／施行2025-09-01；第21条同时废止法释2020 26号第32条第1款；具体存量劳动纠纷适用须专家结合案件阶段。；[CA12 文号未取证](https://liaoning.chinatax.gov.cn/art/2023/12/29/art_5869_7735.html)；第15、22、47—54、84、88、89、182、185、224—226、266条；公布2023-12-29／施行2024-07-01；第266条存量出资过渡须联CA13/CA14；具体条号对应命题仍由专家核。 | CA08：待验证：分别核无资质、超资质、规划许可和补正时点。 反例待验证：任何许可欠缺都一概无效且不付工程款。；CA10：待验证：违约金限制、无效部分和劳动报酬后果分别核。 反例待验证：把劳动合同当普通服务合同任意约定惩罚或押金。；CA11：待验证：加入2025更新核对竞业/社保/混同用工。 反例待验证：只查2020解释或把2023征求意见稿当现行。；CA12：待验证：出资、股权转让、公司回购及减资分开。 反例待验证：所有存量公司从2024统一五年缴清；回购条款一概可履行。；需施工资质/许可、劳动关系或投资出资治理事实；各领域分开判断效力与责任 |

## G4 监管、输出与失败升级

| 项目 | 待本人核实 |
| --- | --- |
| 完整映射 | C06, CR04, CR05 |
| 待核问题 | 区分监管义务、法律效力和工程成功；用独立合成场景审查缺信息、工具失败及高风险输出。 CR04：数据、竞争、贿赂、许可、关联交易规则逐项；CR05：OCR漏小数点、混合劳动/技术合同、双侧批注错位。专业判断不由Word成功生成替代。 |
| 适用时点 | 业务发生时点、行业/地方规定及运行版本待核；本轮未运行上游。 |
| 支持与反例待验证 | 支持：证据可追溯且失败能停止；反例：检索失败、缺库或OCR错误后模型补全确定结论。 |
| 待补正 | 补停止/升级点、缺事实清单及另获授权的实际运行证据，不能把预想场景写作已通过测试。 |
| 来源索引 | [CA01](sources.md#ca01)；[CA03](sources.md#ca03)；[CA12](sources.md#ca12)；[CA13](sources.md#ca13)；[CA15](sources.md#ca15)；[CA16](sources.md#ca16)；[CA17](sources.md#ca17)；[CA18](sources.md#ca18)；[CA19](sources.md#ca19)；[CA20](sources.md#ca20)；[CA10](sources.md#ca10)；[CA11](sources.md#ca11) |
| 时间与版本 | not-verified；逐法公布/施行/修订线索及待核过渡见sources；须与本组每条矩阵事实对应 |
| 当前状态 | 全部not-verified；本人组决定、理由和限制留空 |

本组逐检查项研究入口（全部为待验证问题；非充分法源清单）：

| check_id | 具体来源、条款与时间线索 | 支持／反例及未决 |
| --- | --- | --- |
| C06 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 缺合同、合成场景实际运行、OCR对照与失败停止证据；不作通过。 |
| CR04 | [CA15 文号未取证](https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm)；第3、13、17、21、23、28—29、38—40、55—56、74条；公布2021-08-20／施行2021-11-01；须联读2024出境规定、2025网络数据条例及行业/地方清单，不能只凭法条标题。；[CA17 国家互联网信息办公室令第16号](https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm)；第2—10、13—14条；公布2024-03-22／施行2024-03-22；第13条处理与2022评估办法、2023标准合同办法不一致之处；豁免机制不等于免除保护义务。；[CA19 修正决定主席令第116号](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2023/art_f0fae9eb3a684fc39e84d89eabfc2caa.html)；第2、16—20、22、25—26条；公布2022-06-24／施行2022-08-01；后续垄断协议/经营者集中细则、申报标准、2024民事司法解释尚需按交易补齐。；[CA20 主席令第50号（最高法469181公告交叉检索）](https://www.cnipa.gov.cn/art/2026/5/20/art_104_206437.html)；第7—10、13、40—41条；公布2025-06-27／施行2025-10-15；2025修订导致条号变化，商业贿赂现第8条；旧行为/跨期行为须补法律适用依据。 | CA15：待验证：委托处理、独立提供、敏感信息和出境分别检验。 反例待验证：任何处理一律以同意为唯一基础或合同一句授权即可出境。；CA17：待验证：先核豁免再核评估/标准合同/认证条件。 反例待验证：小于10万人无任何合规义务；旧阈值未更新。；CA19：待验证：识别协议限制及集中申报分支。 反例待验证：任何独家/转售价格条款一律有效或一律无效。；CA20：待验证：商业贿赂、折扣佣金、保密及数据竞争分别核。 反例待验证：将2019第7条不注明版本套2026；把所有佣金当贿赂。；需数据处理角色和流向、竞争行为、利益输送、行业许可及关联交易事实 |
| CR05 | [CA10 文号未取证](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)；第2、9、22—28、38、42、46、47、97条；公布2012-12-28／施行未取证或无独立施行日；区分原法2008施行、2012修正及2025解释二；本页不能自动证明所有条款同时在2013变更。；[CA11 法释〔2025〕12号](https://www.court.gov.cn/zixun/xiangqing/472691.html)；第1—3、13—15、19、21条；公布2025-07-31／施行2025-09-01；第21条同时废止法释2020 26号第32条第1款；具体存量劳动纠纷适用须专家结合案件阶段。；[CA15 文号未取证](https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm)；第3、13、17、21、23、28—29、38—40、55—56、74条；公布2021-08-20／施行2021-11-01；须联读2024出境规定、2025网络数据条例及行业/地方清单，不能只凭法条标题。；[CA18 国务院令第790号](https://www.cac.gov.cn/2024-09/30/c_1729384452307680.htm)；第2、9、12、19、21—29、35—38、64条；公布2024-09-24／施行2025-01-01；2025施行的新层级规则；须与部门办法、最新行业清单衔接，不能用2024快照覆盖2026。 | CA10：待验证：违约金限制、无效部分和劳动报酬后果分别核。 反例待验证：把劳动合同当普通服务合同任意约定惩罚或押金。；CA11：待验证：加入2025更新核对竞业/社保/混同用工。 反例待验证：只查2020解释或把2023征求意见稿当现行。；CA15：待验证：委托处理、独立提供、敏感信息和出境分别检验。 反例待验证：任何处理一律以同意为唯一基础或合同一句授权即可出境。；CA18：待验证：合同义务与安全措施及跨境条件关联。 反例待验证：仅写保密条款即履行全部数据保护义务。；OCR关键数字、双侧批注、混合类型及检索失败仅待验证场景；本轮未运行。 |

## G5 真人裁决、签署与更新

| 项目 | 待本人核实 |
| --- | --- |
| 完整映射 | C07, C09, C10 |
| 待核问题 | 专家作专业决定，维护者另作独立入库决定；保存补正、拒绝和变化记录。 重大交易、行业资质、劳动保护、涉外与数据/反垄断事项须真人裁决。 |
| 适用时点 | 本人复核日、实际法规核查基准、下次复核日期由本人填写，当前未提供。 |
| 支持与反例待验证 | 支持：精确范围及未决项可追溯；反例：工程绿灯、输出文件或上游作者身份代替本人判断。 |
| 待补正 | 补能力/资质受控索引、利益冲突、逐组理由及更新安排；不预填通过、签署或法规日期。 |
| 来源索引 | 固定manifest、main政策和受控事实/授权/能力证据；尚无本人可采纳结论 |
| 时间与版本 | not-verified；逐法公布/施行/修订线索及待核过渡见sources；须与本组每条矩阵事实对应 |
| 当前状态 | 全部not-verified；本人组决定、理由和限制留空 |

本组逐检查项研究入口（全部为待验证问题；非充分法源清单）：

| check_id | 具体来源、条款与时间线索 | 支持／反例及未决 |
| --- | --- | --- |
| C07 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 法律专家判断点与权限由main政策及本人事件核，本catalog不代裁决。 |
| C09 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 0真人签署；不收私有证件、不代填日期。 |
| C10 | [main政策](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/SKILL_INTAKE_POLICY.md)；[签署契约](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/docs/review-workbench/v2/CONTRACT.md)；非直接法律结论 | 需补事实、更新检索、角色证据与后续重审。 |

## 全检查项保留

| 检查项 | 组 | 原问题 |
| --- | --- | --- |
| C01 | G1 | 固定版本与范围：复核下列候选、commit、入口及拟用清单；记录实际审阅文件及 blob |
| C02 | G1 | 法域与事实：确认 CN-Mainland 及案件/合同地点、主体、行业、行为时间、判断时点；识别港澳台/涉外分支 |
| C03 | G2 | 官方法律文本：按候选表中的任务核实每一引用，查找官方发布机关、文号、条款、原文和来源 URL |
| C04 | G2 | 法律时效：对每项核对公布/施行/修订/废止、替代文件、地方规则和过渡/溯及适用 |
| C05 | G2 | 引用真实性与支持性：查条号/名称/原文是否真实，引用是否支持具体结论，是否遗漏例外或冲突 |
| C06 | G4 | 风险与升级：使用独立合成/获授权脱敏场景检查下面高风险项、缺失事实、工具失效和旧法陷阱 |
| C07 | G5 | 人工裁决：对效力、收费、期限、重大交易、数据出境等问题明确人类决定点 |
| C08 | G1 | 权利与用途：与许可审核人员确认本轮审核的精确文件、引用材料、拟用场景和排除项 |
| C09 | G5 | 签署：由具备相应能力的人员自行填写真实身份、资质/专业经验、独立性、复核日期、意见、限制、实际时效核查基准及证据位置并签署 |
| C10 | G5 | 不通过/更新：缺证则补证，法律错误则单独修正/缩范围后重审；根本不适用则保留拒绝/暂停原因 |
| CR01 | G3 | SKILL Step 2、financial-amounts、risk-matrix：违约金占合同价 30%、LPR 四倍、保证金 20% 是否被泛化；待确认：分清损失基数与合同价、借贷类型、利率时点、定金与保证金；阈值是风险提示还是强制规则，专家逐项决定 |
| CR02 | G2 | law-sources、Step 4 的旧《合同法司法解释一》示例与预录法条回退；待确认：新旧法过渡、事实时间和条号逐项核对；检索失败不能以模型记忆确认现行法 |
| CR03 | G3 | construction-contract、employment-contract、equity-investment 等专项结论；待确认：无资质/许可与合同效力、劳动保护、出资/治理与回购适用条件；不能一概断言无效 |
| CR04 | G4 | compliance-checklist 的数据、竞争、贿赂、行业许可、关联交易条目；待确认：监管义务与合同无效区分；数据处理合法基础、例外、行业和地方要求逐条确认 |
| CR05 | G4 | Word 批注、OCR、未检索成功、合同类型混合/未知；待确认：立场未经确认、关键数字识别错误、双侧条款错位可形成相反建议，须人工停止/升级 |

## 固定拟审文件

| 路径（只读固定链接） | blob SHA-1 | 原预审用途 |
| --- | --- | --- |
| [LICENSE](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE) | `1c3ef4997530ff41a93fb627c8f6d31d85d7a2cd` | 项目根许可及版权条件证据 |
| [README.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/README.md) | `ff190f543bc43ec46a066f421f844f90b505b58b` | 安装、能力、限制和来源声明 |
| [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md) | `b1e3ff93439c32bcc142a241ddf400b22e13ede1` | 宿主触发条件、法律任务与工作流入口 |
| [references/clause-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-checklist.md) | `15f247b38551804b153f5be6e2a30c558b65ecea` | 通用合同条款检查清单 |
| [references/clause-conflict-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-conflict-detection.md) | `22bc2abf55106a709d7db1e88da5ed9b5e62e3fc` | 交叉条款冲突识别规则 |
| [references/compliance-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/compliance-checklist.md) | `145450bb3055d4a7330a664de7f902ef5c718cd4` | 合同触发的行业和数据合规规则 |
| [references/contract-type-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-type-detection.md) | `325dd064c34dbe57474eccdb68fbdbfe57bedf96` | 合同类型分类参考规则 |
| [references/contract-types/construction-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/construction-contract.md) | `41af20f0adc57ad271662f1ac46fb544b323f37f` | 对应 construction-contract 类型的合同专项检查规则 |
| [references/contract-types/employment-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/employment-contract.md) | `a30eb80a0d854677e42171aaac80b3c8a444eb04` | 对应 employment-contract 类型的合同专项检查规则 |
| [references/contract-types/equity-investment.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/equity-investment.md) | `16d9fdb8f2bc2c1e3caf4b1bfeb0d1cc93ff9fef` | 对应 equity-investment 类型的合同专项检查规则 |
| [references/contract-types/lease-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/lease-contract.md) | `dfd5559c077f95005d2e33e188e62e4969ca919d` | 对应 lease-contract 类型的合同专项检查规则 |
| [references/contract-types/nda.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/nda.md) | `b699c921e690c261703e0445e3684a905519ac8b` | 对应 nda 类型的合同专项检查规则 |
| [references/contract-types/oem-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/oem-contract.md) | `19da12381d0d73b47475feaa862d65a88239cb88` | 对应 oem-contract 类型的合同专项检查规则 |
| [references/contract-types/purchase-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/purchase-contract.md) | `2ba4532a0627799c199cb8186af4bc52fa15a2bb` | 对应 purchase-contract 类型的合同专项检查规则 |
| [references/contract-types/sales-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/sales-contract.md) | `6b161e6fe9532488bb8680abc8ee2c4f5812edb0` | 对应 sales-contract 类型的合同专项检查规则 |
| [references/contract-types/service-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/service-contract.md) | `8ea22053f06a0ba06f1d49bfdd4ef22c08d863f9` | 对应 service-contract 类型的合同专项检查规则 |
| [references/contract-types/tech-development-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/tech-development-contract.md) | `3e5702b24e273060986ce0318c8803c223897bf8` | 对应 tech-development-contract 类型的合同专项检查规则 |
| [references/financial-amounts.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/financial-amounts.md) | `dfbfef2cb62d6efc2dbbef115d12504a091f1185` | 金额抽取、计算与经验阈值 |
| [references/output-format.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/output-format.md) | `15aa409098c69e1307fb996953c08474326b27dd` | Word 批注和附录输出格式 |
| [references/risk-matrix.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/risk-matrix.md) | `520fcb32d222d6a1f9b1d201adef46ac67c24544` | 风险分级与阈值参考 |
| [references/terminology-glossary.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/terminology-glossary.md) | `da077d77f916cbe9d7d655c547c5ffd804e2d1b9` | 法律术语检查参考 |
| [references/text-quality-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/text-quality-checklist.md) | `a611562e4305932a90a9b8ce6c05b65cd23505f5` | 文字和格式质量检查参考 |
| [scripts/annotate_docx.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/annotate_docx.py) | `f2208af68551d02ebcac2bd17a6665448d3d1d0b` | 调用 officecli 插入 Word 批注 |
| [scripts/check_text_quality.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/check_text_quality.py) | `7695b6c3165c1c03085de46bdc91320b3ab2817f` | 文本质量规则扫描及 Word 文本读取 |
| [scripts/detect_contract_type.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/detect_contract_type.py) | `ad683d1e51fc6470578c493079d9e3d84515d7ce` | 合同类型关键词识别 |
| [scripts/parse_contract.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/parse_contract.py) | `52eb35dd5b371b6dbbc6739c4eb815e1ba11348a` | 合同文件文本和段落提取 |
| [scripts/validate.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/validate.py) | `dd3dfd8dde95dcf2fe6c69a923735961b66bc5d0` | Word 批注输出自检 |

排除完整 4 路径已逐项保存在bundle.excluded_scope，与[原manifest](../../../../../data/reviews/manifests/discovery-contract-review.json)一致；知识库、案例、模板或排除资料的链接不扩大审核/复制/运行权限。

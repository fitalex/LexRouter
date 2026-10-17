# LR-P1-01｜P1 批次 01 候选审核表

执行日期：2026-10-17（Asia/Shanghai）。基线：`main` 的 `abfe489d92100bd5e186bb798c7b809f01387bf8`，执行时经 GitHub branches/main 确认与本地一致。开发分支：`codex/p1-01-expand-legal-skills`。依据已授权任务立即开展发现准备，不调整冻结的 P1 窗口（2026-10-20 至 2026-10-28）或 30–50 个正式入库里程碑。

建议阅读顺序（约 20 分钟）：先看本页统计和去重规则；抽查尽调、刑辩与公司决议的固定入口；查看许可及专业待办，再决定下一任务优先级。此文只记录来源筛选与工程证据，不是能力测评、托管批准或执业法律意见。

## 统计与状态边界

| 口径 | P0 保留基线 | 本批新增 | 联合 |
| --- | ---: | ---: | ---: |
| 候选记录（跨批次初筛后） | 10 | 10 | 20 |
| candidate / needs-evidence / rejected | 4 / 6 / 0 | 4 / 6 / 0 | 8 / 12 / 0 |
| A 精选托管建议 / C 外部索引建议 | 3 / 7 | 3 / 7 | 6 / 14 |
| 独立 B 原创机会（未立项） | 4 | 0 | 4 |
| 许可文本明确 / 受限 / 待核（缺失、范围、主体或冲突） | 4 / 3 / 3 | 4 / 1 / 5 | 8 / 4 / 8 |
| 已完成来源读取 | 10 | 10 | 20 |
| 待法律专业复核 | 10 | 10 | 20 |
| 已完成法律专业复核 / 法规时效核查 | 0 / 0 | 0 / 0 | 0 / 0 |
| 正式入库 / 托管批准 | 0 / 0 | 0 / 0 | 0 / 0 |

本批 10 条来自 7 个原仓库。A/C 均为建议；本批没有进入 P0 readiness 审计，不借用旧批的 ready 结论。原有 A3 待专业复核和进一步授权、C7 阻塞及 B4 未研发原样保留。许可明确数只计算本批实际核对的根许可声明，不等于文件权利链或目标用法全面审核。待核与受限合计本批 6、联合 12；缺失、冲突或主体占位的原因逐条保留。

20 是保留 P0 基线、经本次人工初筛未发现新增重复后的**候选记录总数**，不能称为 20 项已核实独立实体能力或正式 Skill。原 `litigation-hub` 导航边界仍阻塞。机器只验证 ID/同源入口唯一；人工去重意见需由 Human Maintainer 在本 PR 再核，不隐瞒语义判断的不确定性。

| 六类业务（多选，不可相加作总数） | P0 | 新增 | 联合 |
| --- | ---: | ---: | ---: |
| 合同审查 | 4 | 1 | 5 |
| 民商事诉讼 | 3 | 1 | 4 |
| 公司并购 | 1 | 2 | 3 |
| 企业合规 | 2 | 3 | 5 |
| 刑事/行政 | 3 | 3 | 6 |
| 法律检索 | 3 | 1 | 4 |

公司并购的新增对象为尽调底稿及决议文件；刑事/行政新增为刑辩、处罚和信息公开，各自不互相充数。运行载体按来源声明，`other` 不代表已实现任何宿主兼容。所有时效均 `not-checked / null`。

## 逐项审核总表

所有“独立”均为人工来源初筛，未做效果测评。下表法域“大陆声明”统一为 `CN-Mainland / source-declared`，不是专业验证。完整 40 位 SHA、blob、输入输出、授权边界和具名角色待办见后续各条及 [候选 JSON](../data/discovery/p1-batch-01.json)。

| Candidate ID / 名称 | 固定来源 | 业务分类 | 法域证据 | 运行载体 | 许可状态 | 建议 | 独立能力 | 专业复核 | 法规时效 | 阻塞与责任 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `discovery-contract-copilot`<br>Contract Copilot | [cat-xierluo/contract-copilot.skill@ba09c2a](https://github.com/cat-xierluo/contract-copilot.skill/blob/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6/SKILL.md) | 合同审查 | [大陆声明](https://github.com/cat-xierluo/contract-copilot.skill/blob/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6/references/contract-types/06-lending-gift/private-lending.md) | other | 受限；CC-BY-NC-4.0 | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |
| `discovery-systematic-legal-research`<br>Legal Research（系统性规范检索） | [Golden2002/legal-research-skill@f2f9932](https://github.com/Golden2002/legal-research-skill/blob/f2f99327708f095acc4a84bbe69158e85577f93b/legal-research/SKILL.md) | 法律检索 | [大陆声明](https://github.com/Golden2002/legal-research-skill/blob/f2f99327708f095acc4a84bbe69158e85577f93b/legal-research/SKILL.md) | other | 待核；MIT (copyright placeholder; scope pending) | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |
| `discovery-criminal-defense-practice`<br>刑事辩护实务 | [liudejun0306-cyber/codex-skills-archive@043f1b9](https://github.com/liudejun0306-cyber/codex-skills-archive/blob/043f1b999d33ab7f0c510d680b5d401e323f00fe/criminal-defense-practice/SKILL.md) | 刑事/行政 | [大陆声明](https://github.com/liudejun0306-cyber/codex-skills-archive/blob/043f1b999d33ab7f0c510d680b5d401e323f00fe/criminal-defense-practice/SKILL.md) | codex-skill | 明确（仅许可文本）；MIT | A | 独立工作流（初筛） | 未开展 | 未核查 / null | 拟用范围待审；维护者；专业/时效待法律人员 |
| `discovery-diligence-evidence-matrix`<br>尽调底稿证据矩阵 | [CSlawyer1985/claude-for-legal-ZH@59f37f1](https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/59f37f1c8851b8277e24f7a45f4e773bee97bab9/corporate-legal/skills/diligence-evidence-matrix/SKILL.md) | 公司并购 | [大陆声明](https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/59f37f1c8851b8277e24f7a45f4e773bee97bab9/corporate-legal/skills/diligence-evidence-matrix/SKILL.md) | claude-skill | 明确（仅许可文本）；Apache-2.0 | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 拟用范围待审；维护者；专业/时效待法律人员 |
| `discovery-administrative-penalty-response`<br>行政处罚应对 | [chouenchieh/china-law@f051d8e](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/administrative-penalty-response/SKILL.md) | 刑事/行政 | [大陆声明](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md) | claude-skill | 待核；MIT (README declaration only) | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |
| `discovery-government-information-disclosure`<br>政府信息公开法律事务 | [chouenchieh/china-law@f051d8e](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/government-information-disclosure/SKILL.md) | 刑事/行政 | [大陆声明](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md) | claude-skill | 待核；MIT (README declaration only) | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |
| `discovery-corporate-resolution`<br>公司决议起草与审查 | [chouenchieh/china-law@f051d8e](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/corporate-resolution/SKILL.md) | 公司并购、企业合规 | [大陆声明](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md) | claude-skill | 待核；MIT (README declaration only) | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |
| `discovery-food-label-compliance`<br>预包装食品标签合规 | [pa1nrui1/legal-skills@5e39b9c](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E9%A2%84%E5%8C%85%E8%A3%85%E9%A3%9F%E5%93%81%E6%A0%87%E7%AD%BE%E5%90%88%E8%A7%84/SKILL.md) | 企业合规 | [大陆声明](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E6%B3%95%E5%BE%8B%E5%B7%A5%E4%BD%9C%E6%80%BB%E6%8E%A7/references/practice-profile.md) | other | 明确（仅许可文本）；MIT | A | 独立工作流（初筛） | 未开展 | 未核查 / null | 拟用范围待审；维护者；专业/时效待法律人员 |
| `discovery-employer-labor-compliance`<br>用人单位劳动合规 | [pa1nrui1/legal-skills@5e39b9c](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E7%94%A8%E4%BA%BA%E5%8D%95%E4%BD%8D%E5%8A%B3%E5%8A%A8%E5%90%88%E8%A7%84/SKILL.md) | 企业合规 | [大陆声明](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E7%94%A8%E4%BA%BA%E5%8D%95%E4%BD%8D%E5%8A%B3%E5%8A%A8%E5%90%88%E8%A7%84/references/%E5%AE%8C%E6%95%B4%E6%B5%81%E7%A8%8B.md) | other | 明确（仅许可文本）；MIT | A | 独立工作流（初筛） | 未开展 | 未核查 / null | 拟用范围待审；维护者；专业/时效待法律人员 |
| `discovery-corporate-resolution-disputes`<br>公司决议纠纷问答 | [wesky820/china-law-case-analysis-skills@a119d25](https://github.com/wesky820/china-law-case-analysis-skills/blob/a119d25f9fe2163a99b614d0ac15c40c51d25aa5/%E5%85%AC%E5%8F%B8%E5%86%B3%E8%AE%AE%E7%BA%A0%E7%BA%B7/SKILL.md) | 民商事诉讼 | [大陆声明](https://github.com/wesky820/china-law-case-analysis-skills/blob/a119d25f9fe2163a99b614d0ac15c40c51d25aa5/%E5%85%AC%E5%8F%B8%E5%86%B3%E8%AE%AE%E7%BA%A0%E7%BA%B7/SKILL.md) | prompt | 待核；not-identified | C | 独立工作流（初筛） | 未开展 | 未核查 / null | 许可待补；权利人/维护者；专业/时效待法律人员 |

## 来源证据、独立性与逐项待办

共通门槛：所有条目均须由 Human Maintainer 选择使用场景和复核人员；工程维护者确认文件/依赖闭包与来源，许可人员核对权利链；相应法律专业人员核查固定版本及场景、官方文本、引用支持性、生效/修订/废止/过渡和事实时点，具名留证后才可在后续独立 PR 申请正式入库。未指派任何具体专家或代表维护者联系第三方。A 的材料清单/范围审查是下一任务建议，本任务不实施；C 也不能绕过时效和专业要求。

### discovery-contract-copilot｜Contract Copilot

- 原始维护账号：`cat-xierluo`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6`；[原始入口](https://github.com/cat-xierluo/contract-copilot.skill/blob/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6/SKILL.md)，blob `9320fb52291880f7962c030c30f7178a90e64019`。
- 实际核对证据：SKILL L16-L38 文件交付链、L54-L92 审查阶段；README 安装与许可段；独立审查计划驱动 DOCX。 [固定完整树](https://api.github.com/repos/cat-xierluo/contract-copilot.skill/git/trees/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6?recursive=1)：124 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据合同及当事人审查立场，形成条款处理计划、Word 修订批注稿及审查报告；仅作独立实现的来源发现，未运行。
- 分类：合同审查；法域：[来源依据](https://github.com/cat-xierluo/contract-copilot.skill/blob/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6/references/contract-types/06-lending-gift/private-lending.md)。该参考文件 L19-L61 明确采用中华人民共和国民法典及大陆民间借贷司法规则；仅支持该规则范围，不据中文推断全部合同类型的适用法。
- 运行/依赖与材料边界：README 安装段为支持 SKILL.md 的 Agent / Claude 环境，未限定专属宿主，故 other；Word 文件交付依赖本仓库 Python 脚本及 scripts/requirements.txt，未安装。
- 许可与 NOTICE 核查：LICENSE.txt 明确为 CC BY-NC 4.0 并列商业授权另议；入口声明 CC-BY-NC。保留非商业限制，未取得覆盖托管、产品集成或评测的额外授权。 [许可证据 1](https://github.com/cat-xierluo/contract-copilot.skill/blob/ba09c2a6e77ce6de2ceec0726ab776bd23f9a9d6/LICENSE.txt)
- 人工去重：与 discovery-contract-review、discovery-contract-review-zh 比较：前者依赖 officecli，后者专门审委托律师合同；本入口提供自身审查计划与 Python DOCX 执行链。不是前二者镜像或仅换宿主；与 pa1 的设计启发关系须保留，未将其多个合同类型另计。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：非商业范围、借贷综合费用和合同效力判断；不得将报告的可签提示作为律师意见。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：Human Maintainer 决定是否仅保留索引及是否需要额外授权；法律许可人员审 NC 的目标用途；工程维护者界定脚本和外部资料范围。

### discovery-systematic-legal-research｜Legal Research（系统性规范检索）

- 原始维护账号：`Golden2002`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`f2f99327708f095acc4a84bbe69158e85577f93b`；[原始入口](https://github.com/Golden2002/legal-research-skill/blob/f2f99327708f095acc4a84bbe69158e85577f93b/legal-research/SKILL.md)，blob `4074b035a4c408c6cfbebd46aa829563f8c1c200`。
- 实际核对证据：入口 L45-L66 法源与互引、后续检索和报告段；README 载体表；完整根 LICENSE 及树中 docx/LICENSE.txt。 [固定完整树](https://api.github.com/repos/Golden2002/legal-research-skill/git/trees/f2f99327708f095acc4a84bbe69158e85577f93b?recursive=1)：120 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：将具体法律问题转成规范检索、条文互引和规范层级整理，输出资料性检索报告；未核实引用正确性或运行效果。
- 分类：法律检索；法域：[来源依据](https://github.com/Golden2002/legal-research-skill/blob/f2f99327708f095acc4a84bbe69158e85577f93b/legal-research/SKILL.md)。入口 L45-L66 明示中华人民共和国立法法、民法典与最高法/最高检规范；为大陆成文规范检索声明，非专业确认。
- 运行/依赖与材料边界：README 列 Cursor、Claude Code、OpenCode 及将入口用作通用提示词；并非 Cursor Rule 文件，使用 other。依赖宿主联网检索，Word 扩展及其单独许可不在本次对象内。
- 许可与 NOTICE 核查：LICENSE 为 MIT 文本，但版权人仍为 Your Name；README 安装也保留 your-username 占位。可识别许可声明但授予主体/交付范围待核，未将占位视为权属证据；docx/LICENSE.txt 为另一材料边界，不推定全包 MIT。 [许可证据 1](https://github.com/Golden2002/legal-research-skill/blob/f2f99327708f095acc4a84bbe69158e85577f93b/LICENSE)
- 人工去重：与 discovery-cn-law-hub 比较：后者侧重官方站点查询与有效性核验，本入口编排多层规范及相互引用并交付系统检索报告；与法律顾问及爽律的通用检索能力有交集，但有单独入口和检索报告任务，不拆出其多个宿主或 docx 工具。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：旧条号、一般/特别规范关系及检索遗漏；作者的现行有效要求不是实际时效复核。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：Human Maintainer 决定是否要求上游澄清版权主体及保留边界；工程维护者核对占位安装路径、Word 依赖与检索宿主；法律专业人员审规范层级和引用。

### discovery-criminal-defense-practice｜刑事辩护实务

- 原始维护账号：`liudejun0306-cyber`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`043f1b999d33ab7f0c510d680b5d401e323f00fe`；[原始入口](https://github.com/liudejun0306-cyber/codex-skills-archive/blob/043f1b999d33ab7f0c510d680b5d401e323f00fe/criminal-defense-practice/SKILL.md)，blob `59f81a2bde2c94624981635d2a528e94c29cd12c`。
- 实际核对证据：SKILL L1-L24 分阶段及证据处理、L36-L68 知识库与模块边界；README Codex 声明；完整 LICENSE。 [固定完整树](https://api.github.com/repos/liudejun0306-cyber/codex-skills-archive/git/trees/043f1b999d33ab7f0c510d680b5d401e323f00fe?recursive=1)：107 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：从程序阶段和有限材料或完整卷宗出发，核对控辩证据、供述与量刑材料，形成分阶段辩护意见或文书草稿；未运行。
- 分类：刑事/行政；法域：[来源依据](https://github.com/liudejun0306-cyber/codex-skills-archive/blob/043f1b999d33ab7f0c510d680b5d401e323f00fe/criminal-defense-practice/SKILL.md)。入口 description 明确中国大陆刑事辩护；README 首段为 Mainland Chinese law。
- 运行/依赖与材料边界：README 明确 Codex 模块；依赖 chinese-writing-style、chinese-document-output-style、obsidian-case-workspace-sync 和作者的本地知识库。未核查完整依赖闭包或兼容性。
- 许可与 NOTICE 核查：根 MIT 署名 liudejun0306-cyber；完整递归树未发现独立 LICENSE/NOTICE。仅确认仓库声明；本地知识库、权威书籍、文章及真实卷宗不随根许可取得权利。 [许可证据 1](https://github.com/liudejun0306-cyber/codex-skills-archive/blob/043f1b999d33ab7f0c510d680b5d401e323f00fe/LICENSE)
- 人工去重：与 discovery-law-ye、discovery-shuanglv 比较：两者为宽域综合入口，本项是独立刑辩模块，明确区分阅卷前材料与阅卷后控方证明链；没有将各罪名、阶段及模块再计数。与本仓库其它 Codex 技能不同任务，未把整个仓库入口另计。
- 分流：**A 建议**。可优先考察具体模块的文件/授权边界与可维护性，暂不授予托管、复制或再分发权限。
- 法律专业复核：**未开展**。待核风险：证据合法性、证明标准、羁押和程序期限、罪名构成与量刑；不得把阅卷前陈述当客观事实。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：Human Maintainer 仅决定是否优先安排范围审查；工程维护者下一任务列模块/知识库及同步依赖；刑事法律专业人员逐项复核，不启动托管。

### discovery-diligence-evidence-matrix｜尽调底稿证据矩阵

- 原始维护账号：`CSlawyer1985`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`59f37f1c8851b8277e24f7a45f4e773bee97bab9`；[原始入口](https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/59f37f1c8851b8277e24f7a45f4e773bee97bab9/corporate-legal/skills/diligence-evidence-matrix/SKILL.md)，blob `e59692a7215515f0bbce12a464a9ee179cb98978`。
- 实际核对证据：入口完整 L1-L24：文件入账、证据矩阵与内部输出；corporate-legal/CLAUDE.md 配置/来源边界；根 Apache 许可和 README。 [固定完整树](https://api.github.com/repos/CSlawyer1985/claude-for-legal-ZH/git/trees/59f37f1c8851b8277e24f7a45f4e773bee97bab9?recursive=1)：834 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：把中国公司股权投资或收购底稿逐件登记并映射待证事实、材料冲突和资料缺口，输出尽调矩阵及内部问题备忘录；未验证。
- 分类：公司并购；法域：[来源依据](https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/59f37f1c8851b8277e24f7a45f4e773bee97bab9/corporate-legal/skills/diligence-evidence-matrix/SKILL.md)。入口 description 指向中国公司股权投资或收购，步骤要求公司法新旧衔接；配套 corporate-legal/CLAUDE.md 明示中国法边界。
- 运行/依赖与材料边界：README 支持 Claude Code 插件及其它安装适配，选主要 claude-skill；同名 .agents/.dsh/.workbuddy 是适配层，不另计。依赖 corporate-legal/CLAUDE.md、证据预处理、OCR 与可选企业/法律 MCP。
- 许可与 NOTICE 核查：根 LICENSE 为 Apache-2.0，README 同述；树未见另行许可或 NOTICE 文件（notice-watch.md 是任务名）。仅核仓库声明，客户底稿、OCR 和企业信息/法律 MCP 另需使用权限。 [许可证据 1](https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/59f37f1c8851b8277e24f7a45f4e773bee97bab9/LICENSE)
- 人工去重：与 discovery-antitrust-filing 的申报义务初筛不同，本项处理收购尽调底稿的事实证据。仓库确为 anthropics/claude-for-legal 的 fork，但所选 diligence-evidence-matrix 入口不在本次固定的上游树中，有独立中国公司任务；不收录上游共有技能、diligence-grid 导航或其它安装副本。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：全量文件入账不等于完整尽调；出资、控制权、交易后果、公司法过渡及信息截止日需专家确认。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：工程维护者保持 fork/来源追踪并界定依赖闭包；Human Maintainer 决定内部底稿场景和授权范围；并购法律专业人员核对事实认定与交易后果。

### discovery-administrative-penalty-response｜行政处罚应对

- 原始维护账号：`chouenchieh`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0`；[原始入口](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/administrative-penalty-response/SKILL.md)，blob `459eeb9cd4d57bc57fd6ce39181573d31ae10aa3`。
- 实际核对证据：SKILL L1-L52 阶段、输入与应对输出；CLAUDE L44 大陆边界；README 许可声明与完整树缺许可文件事实。 [固定完整树](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)：109 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据处罚阶段、执法文书和企业事实整理陈述申辩、听证、决定审查与救济路径，输出含期限提示的应对指南；未专业验证。
- 分类：刑事/行政；法域：[来源依据](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md)。CLAUDE.md L42-L44 明确默认中华人民共和国（中国大陆）；该入口引用行政处罚法等并按中国行政程序组织任务。
- 运行/依赖与材料边界：README 声明 Claude Code / Cowork 插件；入口依赖实践画像路径及北大法宝 MCP，README 自述 laws/ 本地库在固定树中未出现，交付完整性待核。
- 许可与 NOTICE 核查：README 有 MIT 徽章和 MIT License 声明，但固定完整树没有 LICENSE、COPYING 或 NOTICE 文件；未见具体授权主体及完整授予文本。插件生态许可和本地法律库不能由徽章推定，需补证。 [许可证据 1](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/README.md) [许可证据 2](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)
- 人工去重：与 discovery-gutachten-admin 的抽象行政合法性分析不同，聚焦处罚通知、听证及执行阶段材料；与本批信息公开入口的公开请求/第三方异议任务不同，不收录套件导航。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：听证条件、送达、救济期限及裁量适用；入口对修法年份的表述需专业复核，不据此填写时效。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：Human Maintainer 决定许可补证路径；权利人提供固定文件/版本许可；工程维护者确认依赖缺失；行政法专业人员逐项复核期限及程序。

### discovery-government-information-disclosure｜政府信息公开法律事务

- 原始维护账号：`chouenchieh`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0`；[原始入口](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/government-information-disclosure/SKILL.md)，blob `55a5953de6e699d601b9fa48004f560b094a0d5c`。
- 实际核对证据：SKILL L1-L56 明确信息公开申请/答复/异议输入、角色与分析报告；CLAUDE 大陆声明；README 和完整树许可核查。 [固定完整树](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)：109 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据公开申请、机关答复或第三方意见分析信息可获性、保密利益和答复争议，形成信息公开及救济策略报告；未验证法律结论。
- 分类：刑事/行政；法域：[来源依据](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md)。CLAUDE.md L44 明确大陆法域；入口 L1-L29 依政府信息公开条例组织申请、答复及行政救济。
- 运行/依赖与材料边界：Claude Code / Cowork 插件，依赖实践画像及北大法宝 MCP；本地 laws/ 数据库在 README 自述但不在该树中。入口部分文字有编码异常，未修写上游。
- 许可与 NOTICE 核查：根 README 仅有 MIT 声明/徽章，固定完整树未见许可/NOTICE 文本；实际文件授权范围待核。本地法律库及北大法宝服务权利不继承。 [许可证据 1](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/README.md) [许可证据 2](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)
- 人工去重：与本批处罚应对分别处理公开申请/拒绝公开和行政处罚文书；与 discovery-gutachten-admin 的泛用分析有方法交集，但具有特定申请/第三方商业秘密任务及独立输入输出。未将复议、诉讼分支另计。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：不予公开例外、第三方商业秘密/隐私、复议前置与答复期限，需核验实际法与事实；编码异常可能影响读取。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：权利人补许可；Human Maintainer 决定索引边界；工程维护者确认编码及缺失依赖；行政法专业人员审公开例外、救济路径与期限。

### discovery-corporate-resolution｜公司决议起草与审查

- 原始维护账号：`chouenchieh`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0`；[原始入口](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/skills/corporate-resolution/SKILL.md)，blob `f3b9cc0518d84678b766d1b4ff03ece24f11ded9`。
- 实际核对证据：SKILL L1-L21 公司/决议/事项输入，后续输出与程序核对；L43-L57 董事会及效力规则为待专业核查重点；README/CLAUDE。 [固定完整树](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)：109 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据公司类型、章程、决议事项和会议事实形成公司决议草稿及程序核对结果；未确认条号、表决或组织规则有效。
- 分类：公司并购、企业合规；法域：[来源依据](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/CLAUDE.md)。CLAUDE.md L44 明确大陆；入口以中国公司法和有限公司/股份公司决议为对象。
- 运行/依赖与材料边界：Claude 插件；使用公司章程、股东及会议资料和北大法宝检索，依赖同套件实践画像；未安装执行。
- 许可与 NOTICE 核查：README 宣称 MIT，但固定树缺完整许可、版权人与 NOTICE，不能推定整包公开托管；继续待补证据。 [许可证据 1](https://github.com/chouenchieh/china-law/blob/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0/README.md) [许可证据 2](https://api.github.com/repos/chouenchieh/china-law/git/trees/f051d8ebfb0fc5dfe0a5069f17b7e2ec7f8b17b0?recursive=1)
- 人工去重：与本批 wesky 公司决议纠纷问答区别在非诉决议制作及程序核对，而后者解释已发生争议及案例；与 antitrust-filing 申报筛查及尽调矩阵也不同，不将不同决议类型重复计数。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：董事会组成、表决和公司法条号有明显需核查的版本混用线索；这只是风险定位，不构成 AI 专业复核完成。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：权利人澄清许可，Human Maintainer 决定是否继续筛选；公司法专业人员优先核查组织规则/条号；工程维护者保留旧法风险，不托管或改写。

### discovery-food-label-compliance｜预包装食品标签合规

- 原始维护账号：`pa1nrui1`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`5e39b9c30cc66ece89ff64cdafbeddde80c6b507`；[原始入口](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E9%A2%84%E5%8C%85%E8%A3%85%E9%A3%9F%E5%93%81%E6%A0%87%E7%AD%BE%E5%90%88%E8%A7%84/SKILL.md)，blob `4662c1b495d9c6f0ab9309274cfc3f54a92d4e23`。
- 实际核对证据：SKILL L1-L57；references/完整流程.md L29-L65 显示四阶段与标准版本选择；共享 practice-profile 大陆范围；根 MIT。 [固定完整树](https://api.github.com/repos/pa1nrui1/legal-skills/git/trees/5e39b9c30cc66ece89ff64cdafbeddde80c6b507?recursive=1)：727 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：将食品标签照片、文本或文档按选定标准版本作一般标签与营养标签核对，输出缺项和风险报告；未确认标准时效与审核准确性。
- 分类：企业合规；法域：[来源依据](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E6%B3%95%E5%BE%8B%E5%B7%A5%E4%BD%9C%E6%80%BB%E6%8E%A7/references/practice-profile.md)。共享执业配置 L51-L54 明示中国大陆；专业入口及完整流程引用 GB 7718、GB 28050，未从标准编号推定现行适用版本。
- 运行/依赖与材料边界：通用 SKILL.md 与共享总控协议，README 可配置宿主/本地工作区，使用 other；需可读标签/OCR、完整流程、版本规则和法律检索接口；未执行。
- 许可与 NOTICE 核查：固定根 MIT 署名 Legal Skills Contributors；完整树无该子模块独立许可/NOTICE。仅核工作流许可声明，不自动覆盖国家标准全文、标签素材、外部模板或检索服务。 [许可证据 1](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/LICENSE)
- 人工去重：与本批劳动合规在对象、输入和输出上不同：标签/营养标识与企业用工制度。两者共享总控不等于同一任务；分别读取完整流程核对，不把轻量入口的同构包装当证据，也不另计总控。
- 分流：**A 建议**。可优先考察具体模块的文件/授权边界与可维护性，暂不授予托管、复制或再分发权限。
- 法律专业复核：**未开展**。待核风险：2011/2025 标准的施行与过渡、豁免、营养数值及图像误读，须食品合规专业复核。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：Human Maintainer 决定是否优先安排限定模块范围预审；工程维护者列共享协议和模板依赖；法律/食品合规人员逐条核时效与适用边界。

### discovery-employer-labor-compliance｜用人单位劳动合规

- 原始维护账号：`pa1nrui1`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`5e39b9c30cc66ece89ff64cdafbeddde80c6b507`；[原始入口](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E7%94%A8%E4%BA%BA%E5%8D%95%E4%BD%8D%E5%8A%B3%E5%8A%A8%E5%90%88%E8%A7%84/SKILL.md)，blob `10c1152e33423e9b0b1768ac6b6a4960f5f9f5d6`。
- 实际核对证据：SKILL L1-L57 的专业任务与外置索引；完整流程 L31-L50 区分公司端合规和已入诉讼；根 LICENSE。 [固定完整树](https://api.github.com/repos/pa1nrui1/legal-skills/git/trees/5e39b9c30cc66ece89ff64cdafbeddde80c6b507?recursive=1)：727 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据员工手册、劳动制度、薪酬工时及调整材料，梳理公司端劳动政策和争议前风险，输出政策草稿或风险报告；不代替仲裁诉讼。
- 分类：企业合规；法域：[来源依据](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/skills/legal/%E7%94%A8%E4%BA%BA%E5%8D%95%E4%BD%8D%E5%8A%B3%E5%8A%A8%E5%90%88%E8%A7%84/references/%E5%AE%8C%E6%95%B4%E6%B5%81%E7%A8%8B.md)。完整流程 L31-L39 明确中国大陆劳动法规、地方及特殊工时规则；共享配置也声明大陆范围。
- 运行/依赖与材料边界：通用 Agent Skill，other；依赖共享配置、材料读取/OCR、pkulaw 核验协议及可选飞书写入；缺私有目录或凭证时不能假定可交付，未运行。
- 许可与 NOTICE 核查：根 MIT 明确，子模块树无单独许可/NOTICE；不得将员工信息、地方规则全文、外部模板与商业检索服务视为同时获权。 [许可证据 1](https://github.com/pa1nrui1/legal-skills/blob/5e39b9c30cc66ece89ff64cdafbeddde80c6b507/LICENSE)
- 人工去重：与 discovery-china-legal-counsel 的广义合规入口有主题交集，但本项为用工制度生效和争议前处理的具体模块，明确将已入仲裁诉讼转出；与食品标签的标准审核任务独立。未拆工资、考勤或解除为多条。
- 分流：**A 建议**。可优先考察具体模块的文件/授权边界与可维护性，暂不授予托管、复制或再分发权限。
- 法律专业复核：**未开展**。待核风险：地方工资、工时、制度民主程序、调岗解除条件与个人信息；不得泛化用工金额或期限。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：工程维护者列单模块材料/共享依赖边界；Human Maintainer 仅决定审核优先级；劳动法专业人员核对地方规则和事实时点，不提前开发或托管。

### discovery-corporate-resolution-disputes｜公司决议纠纷问答

- 原始维护账号：`wesky820`；只核实公开账号，不认证真实身份、律师资质或全部权属。
- 版本：`a119d25f9fe2163a99b614d0ac15c40c51d25aa5`；[原始入口](https://github.com/wesky820/china-law-case-analysis-skills/blob/a119d25f9fe2163a99b614d0ac15c40c51d25aa5/%E5%85%AC%E5%8F%B8%E5%86%B3%E8%AE%AE%E7%BA%A0%E7%BA%B7/SKILL.md)，blob `fb4a73f4c181f74eb48eed24e1b587ecc784a1c1`。
- 实际核对证据：入口 L1-L60 问题/事实输入、澄清、争点与六步回答形态；README 用法；完整树未见许可。 [固定完整树](https://api.github.com/repos/wesky820/china-law-case-analysis-skills/git/trees/a119d25f9fe2163a99b614d0ac15c40c51d25aa5?recursive=1)：544 项，`truncated=false`；树证明文件位置而非全文件权属。
- 任务、输入与输出：根据已发生的公司决议争议事实、证据和问题，组织争点、类案线索、风险及下一步说明；来源面向普通人问答，目录仅供专业人员发现，未验证。
- 分类：民商事诉讼；法域：[来源依据](https://github.com/wesky820/china-law-case-analysis-skills/blob/a119d25f9fe2163a99b614d0ac15c40c51d25aa5/%E5%85%AC%E5%8F%B8%E5%86%B3%E8%AE%AE%E7%BA%A0%E7%BA%B7/SKILL.md)。入口 L1-L11 明确中国法下公司决议纠纷及人民法院案例库；属于大陆民商事争议来源声明，未核验所称九个案例。
- 运行/依赖与材料边界：README 允许作 system prompt、项目指令或知识文档；本项按独立提示词 prompt 记录，未据 SKILL.md 名称虚构 Claude/Codex 专属兼容。依赖案例规则与用户证据，未取用真实案例材料。
- 许可与 NOTICE 核查：固定完整树未见 LICENSE/COPYING/NOTICE，已读 README 没有明确分发许可；案例摘要、归纳与改编权均待核，公开可读不代表授权。 [许可证据 1](https://github.com/wesky820/china-law-case-analysis-skills/blob/a119d25f9fe2163a99b614d0ac15c40c51d25aa5/README.md) [许可证据 2](https://api.github.com/repos/wesky820/china-law-case-analysis-skills/git/trees/a119d25f9fe2163a99b614d0ac15c40c51d25aa5?recursive=1)
- 人工去重：只取公司决议纠纷这一可定位任务，不计根导航或其宣传的 264 模块。与本批公司决议制作分别为争议解释与事前决议交付；与原 litigation-hub/prep 的导览或一般诉前准备不同。本次未申请其它案由拆分。
- 分流：**C 建议**。保留固定外链和原创简述；许可、适配或业务边界待补时仅在候选区。
- 法律专业复核：**未开展**。待核风险：裁判规则摘录重复或截断、案例代表性、旧公司法时点及过度预测裁判；不采信维护者自述为专家审核。 法规时效：**未核查，as_of=null**。
- 阻塞、证据需求及负责角色：权利人补明确授权；Human Maintainer 决定普通人问答来源是否适合专业目录及保留范围；公司诉讼专业人员逐案回源并核对法律时点；工程维护者保留缺许可阻塞。

## 跨批次与套件去重依据

对全部新增 10 条与 P0 10 条的名称、原仓库/入口、任务输入输出及材料边界做人工比较；最接近的对象与判断逐条写在上述“人工去重”和 JSON `evidence_notes`，没有以主题标签不同替代能力判断。主题相近仍可有独立实现，但同一能力的镜像、改名/包装、宿主副本和导航不新增计数。

- P0 `litigation-hub` 不展开；原诉前准备及 law-ye 等重复检索命中均回指既有 Candidate ID，不新增。
- pa1 的两个轻量 SKILL 外壳相似；实际读取各自 `references/完整流程.md`，确认食品标签版本/营养标识检查与劳动制度/争议前风险属于不同任务。保留共享总控依赖和各自材料边界；不计总控和其它子技能。
- chouenchieh 三个入口分别具有处罚文书、信息公开申请/答复、公司章程/决议事项输入，交付不同；均单独定位入口和许可待核，不把套件宣传的 45 项转成目录数量。
- wesky 只核对公司决议纠纷一项，不计根导航及其宣传模块数；该任务面向既有纠纷解释，与本批决议制作不同。来源的 C 端定位是后续筛选疑点，不构建 C 端咨询产品。
- CSlawyer 仓库是 fork，记录其上游归属；只选择具有中国收购底稿证据任务的独立文件，不另计 `.agents/.dsh/.workbuddy` 适配、`diligence-grid` 路由或上游共同工作流。实际读取 [上游固定树](https://api.github.com/repos/anthropics/claude-for-legal/git/trees/4a6c651889c97cc9140580363c73e0eb17379c2b?recursive=1)，`truncated=false`；该树有 `diligence-issue-extraction`，没有所选 `diligence-evidence-matrix`。这支持入口差异，不能替代权利链审查或保证无语义相似。
- 发现 pa1 README 致谢 Contract Copilot 的文档交付设计启发；本批只选 pa1 的食品/劳动任务，不再收录其合同审查副本；Contract Copilot 只计一个独立原仓库入口，分层与文档计划证据见该条。

联合 CLI 检查同一原文件入口在不同提交、blob/raw URL、宿主或账号/仓库大小写包装下的重复，以及跨批 ID。它不能从文件 URL 检出其它仓库中的镜像、提示词副本或深层语义重复；本页人工比较是可复核的初筛意见，最终目录对象边界仍由维护者决定。没有自动确认“全部能力去重完成”。

## 六类检索与渠道日志

以下均于 2026-10-17 由本任务发起，Web 搜索只用于线索发现；批量查询的合并结果不能视作每个查询都返回了某一项目。候选事实来自随后实际读取的原始固定入口、README、必要引用、完整许可（存在时）及递归树，证据在上文；没有根据搜索摘要生成候选。

| 业务方向 | 实际检索词/补充核查 | 结果与处理 |
| --- | --- | --- |
| 合同审查 | `site:github.com "合同" "contract-copilot" "skill"` | 定位 Contract Copilot 原仓库；回源核查 CC-NC，未把聚合版或其它宿主再计数 |
| 民商事诉讼 | `github 中国 法律 skills 诉讼 尽职调查 刑事 行政`；`site:github.com "刑事" "行政" "SKILL.md"` | 新线索 wesky；已有 litigation-prep 回指原 ID；仅取公司决议纠纷入口 |
| 公司并购 | `github legal skills 尽调 行政复议 工作流`；`site:github.com "公司" "尽调" "diligence-evidence-matrix"` | 聚合与原项目检索结合，固定尽调矩阵入口及公司决议；不保证单个精确检索返回结果 |
| 企业合规 | `site:github.com "劳动合规" "食品标签" "legal-skills"` | 定位 pa1 两个不同任务，读取外置完整流程与共享大陆范围声明 |
| 刑事/行政 | 首行广义查询及 `github 法律 Dify 工作流 行政复议 起诉状` | 回源 Codex 刑辩、处罚和信息公开；既有 law-ye、gutachten-admin 不新增 |
| 法律检索 | `site:github.com "法律检索" "legal-research-skill"` | 固定 Golden2002 入口；发现根版权占位及独立 docx 许可，未推定完整授权 |

| 渠道 | 实际访问/查询 | 本次结论和覆盖限制 |
| --- | --- | --- |
| GitHub 原始项目 | 七仓库的默认分支 HEAD 经 commits API 固定完整 SHA，随后读取 blob/raw 与树；账户/仓库元数据核对 fork | 只对上文 10 项形成候选；未安装执行或运行法律用例 |
| Awesome 法律 AI 目录 | [awesome-legal-ai-zh 固定 README](https://github.com/lilialla/awesome-legal-ai-zh/blob/910dce525e9f39f1152315ec8e997b147c739a95/README.md)；`github awesome legal skills china Cursor Dify 法律` | 实际读取前者 README；awesome-legal-dsh 只作检索线索/版本定位，未把其星数/审查标签当证据 |
| skills.sh | 搜索 `skills.sh legal 中国 法律 cursor rules`、`site:skills.sh "legal" "中国" "公司"`；实际打开 [china-legal-skills 聚合入口](https://www.skills.sh/pa1nrui1/legal-skills/china-legal-skills) | 只作为 pa1 的来源线索；该总控路由未计数，选择原仓库已读的两个实体任务；安装量与站内审计不作为审核结论 |
| Claude/Codex Skills 生态 | 广义法律 skills 检索；原 README 与实际 SKILL 对照 | 记录实际声明的 claude-skill、codex-skill 或通用 other，不猜测兼容性 |
| Cursor Rules | `site:github.com "Cursor" "Rules" "法律" "中国"` | 命中 Dean202305/china-legal-advisor、规则适配等线索，本批未核完原始 Rule、许可及版本，不计候选；Golden 支持 Cursor 不等于 Cursor Rule |
| Dify 公开法律工作流 | `site:github.com Dify 法律 工作流 行政复议 尽职调查`；另一次广义 Dify 查询 | 本轮未核实新的独立 YAML/DSL 工作流；已有 Skill 可粘贴到 Dify 的说明不能据此升级为 dify-workflow。未覆盖不等于不存在，列为下一批目标 |
| 中国大陆法律开源社区 | 上述 GitHub/目录中文检索及公开原作者发布账号 | 未使用私群、未联系权利人，未把中文或作者所在地当法域证据；社区发现未穷尽 |

额外读取并暂不纳入：NEU-ZHA/legal-ai-skills 的证据目录与监管回复核查入口、LICENSE/NOTICE；前者有明确文档任务但本轮没有充分的独立大陆法域依据，后者还需厘清法域与组合子技能边界；不能凭中文和北大法宝名称推定法域。Codex archive 的打印遗嘱入口虽有独立任务，但属于非诉继承且本轮六类枚举适配未定，故不计数。其它搜索命中的纯模型/数据源、未经原始入口核查的项目和镜像均不进入本批；不把排除线索混入新增候选数。

## B 机会与下一任务

本批不重复提出 P0 四项 B 机会，不从受限材料抽取结构或交给模型改写。现有证据规划、并购资料采集、行政救济采集和引用追溯机会继续 `not-started`，需求访谈、官方法规和隔离设计来源仍待独立授权，不启动研发。

LR-P1-02 优先保持已有三个 A 的精确材料范围及法律交接顺序；Human Maintainer 可根据本批来源和依赖成本决定是否将刑辩、食品标签、劳动合规纳入后续审核队列。C7 新建议优先补许可主体、缺失许可与公司法旧规则风险；本 PR 不替代后续权限/专业审批。下一批优先查验 Cursor 真正规则入口、Dify DSL，以及更多具有独立文件与授权边界的诉讼证据/庭前和并购交易材料，仍不以套件数量凑数。

## 工程校验与验收证据

候选契约、正式八字段和既有 P0 审计绑定不变。新增 `validate_discovery_batches.py` 复用原候选校验与严格 JSON 解析；无需新增依赖，全部数据检查可离线运行。新增正反测试用临时合成数据，覆盖真实出错机制，不复制第三方法律样例。外部来源核查与 CI 分开；CI 不实时访问候选网站。

```sh
python scripts/validate_skills.py skills
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_candidates.py data/discovery/p1-batch-01.json
python scripts/validate_discovery_batches.py data/discovery/candidates.json data/discovery/p1-batch-01.json
python scripts/validate_p1_readiness.py
python scripts/validate_intake_plan.py
python scripts/validate_p1_handoff.py
python -m unittest discover -s tests -v
git diff --check
```

实际全量执行结果、Actions 运行链接及 D01–D10 状态见 [任务记录](daily-specs/LR-P1-01.md) 和本次 PR；未完成的远程检查不预填通过。结构通过不表示法律、许可或能力质量已审核。

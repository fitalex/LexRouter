# P1 入库准备与首批候选证据审计

本记录服务 [LR-P0-03](daily-specs/LR-P0-03.md)，审计日期为 **2026-10-16**，任务目标日期为 **2026-10-17**。审计基于 `main` 提交 `9e511e6b87f7d71abc7b7bf0a2603b6b538f86da` 中的 10 条发现记录，逐项重新读取各自原始仓库的固定提交。机器可读结果见 [p1-readiness.json](../data/discovery/p1-readiness.json)，原发现记录见 [candidates.json](../data/discovery/candidates.json)。

**准备状态只决定是否具备提交专业复核的工程和来源条件，不批准正式入库。** 当前为 3 条 `ready-for-professional-review`、7 条 `blocked`、0 条 `rejected`。正式 `skills/` 条目、完成法律专业审核数、完成法规时效核查数仍均为 **0**。这不是 P0 或 P1 验收通过声明，也不是选型推荐。

## 状态与使用范围

| 准备状态 | 含义 | 下一步 |
| --- | --- | --- |
| `ready-for-professional-review` | 固定来源、入口、独立工作流、分类和许可文本具备提交专业复核的工程条件；未发现阻断本轮交接的许可问题 | Human Maintainer 安排法律专业人员；不能自动复制、安装、测评或入库 |
| `blocked` | 授权、入口独立性或其他证据仍有明确未解决事项 | 按阻塞记录补证，保留待核状态后重新审计 |
| `rejected` | 有证据确认对象不符范围或禁止拟议用途等 | 保留拒绝依据，未经新证据与审核不得恢复 |

本次拟准备的对象是可追溯的法律工作流入口及其独立撰写的目录元数据。后续完整包复制、改编、公开分发、宿主运行、测评和商业使用均需按具体材料及用途另行核对。没有下载、安装或执行第三方 Skills，没有收录第三方 Skill 全文，没有调用付费模型开展法律测评。

## 审计方法及证据边界

对 10 个候选分别读取固定提交的入口有限片段、README（存在时）、完整 LICENSE（存在时）和完整递归文件树，并额外核对 CN Law Hub 的 NOTICE、爽律根目录与运行包许可及 NOTICE。每条 `audit_evidence` 保存固定 URL、读取/404 结果、文件 blob SHA、实际阅读范围及原创事实简述；文件树均返回 `truncated=false`。未把文件树检查当作已阅读全部代码或已完成权属鉴定。

核查原始入口只确认工作流结构，未运行验证效果。业务分类沿用原有六类枚举并逐项记录任务证据；法域均保留 `source-declared`，不从中文、账号所在地推断。运行载体沿用原记录，兼容性全部为 `source-declared-unexecuted`。维护者身份、执业资质、作者自述认证、项目热度与自身评分均未被认定为独立法律专业证据。

所有 `regulatory_currency.status` 保持 `not-checked`、`as_of: null`。来源核查日、版本日期、作者的时效监控记录和“现行有效”自述不能替代逐条现行法规及专业复核。每条记录的 `professional_review` 均为 `not-performed`，包含需核对的具体法律事项。

## 10 个候选的审计结论

下表版本链接指向实际入口的固定提交；完整 40 位 revision、分类与证据定位在 JSON 中逐项记录。原发现状态保持 4 条 `candidate`、6 条 `needs-evidence`，与本次准备状态分别统计。

| Candidate ID / 固定入口 | 原发现状态 | 业务分类 | 来源及工作流结论 | 授权与准备结论 |
| --- | --- | --- | --- | --- |
| [discovery-contract-review](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md) | candidate | 合同审查 | 入口存在；立场澄清、条款/金额/冲突审查与批注输出可辨识 | MIT，保留声明；**ready-for-professional-review** |
| [discovery-contract-review-zh](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/SKILL.md) | candidate | 合同审查 | 入口存在；委托律师合同七维审查与修改建议可辨识 | Apache-2.0，外部笔记权利不自动覆盖；**ready-for-professional-review** |
| [discovery-china-legal-counsel](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md) | candidate | 企业合规、合同审查、法律检索 | 入口存在；事实澄清、来源检索、风险分级与人工升级可辨识 | MIT，知识库和外部资料仍需按材料核对；**ready-for-professional-review** |
| [discovery-cn-law-hub](https://github.com/ZongziForu/cn-law-hub/blob/8a62d5cbec94489dcb7a661dd0df411742a2a1e2/SKILL.md) | candidate | 法律检索 | 入口存在；检索策略、法条查询和有效性规则可辨识 | 根 Apache-2.0 不能覆盖 NOTICE 排除的未明确授权贡献者组件；**blocked** |
| [discovery-litigation-hub](https://github.com/Youchu-lawhub/cn-litigation-toolkit/blob/b15b762105a9331c3cd32e5c72ef32a8a8e3f58f/skills/litigation-hub/SKILL.md) | needs-evidence | 民商事诉讼 | 入口存在；主要为套件导览与编排，独立实体法律能力仍待界定 | CC-BY-NC-ND-4.0 及附加限制；**blocked** |
| [discovery-litigation-prep-cn](https://github.com/yxk-lawyer/litigation-prep-skill-cn/blob/a8ce2f2490cd3ee688bbee8e41add39068468b67/skill/SKILL.md) | needs-evidence | 民商事诉讼 | 入口存在；案由、请求权基础、要件与证据清单工作流可辨识 | 未找到明确许可证；**blocked** |
| [discovery-law-ye](https://github.com/Jarvis-starcloud/law-ye-skill/blob/790b83f1464d58557d23da0392a90fcfc524dd34/SKILL.md) | needs-evidence | 刑事/行政 | 入口存在；问题定性、模块调用与实务输出可辨识 | 未找到明确许可证；**blocked** |
| [discovery-shuanglv](https://github.com/zj-ai-lab/shuanglv-legal-skills/blob/4a67c181e27ad1dfa59cb953396acc5e8ee1eb2f/runtime/shuanglv-legal-skills/SKILL.md) | needs-evidence | 刑事/行政、民商事诉讼、合同审查、法律检索 | 入口存在；专业任务与交付控制可辨识；作者专业头衔未独立认证 | ShuangLaw Professional Use License 1.0，公开改编与产品商业化受限；**blocked** |
| [discovery-antitrust-filing](https://github.com/ettajingruyang/PRC-merger-control-assessment/blob/bde8d130074696e776d70906c3f46e0b47ece5ee/SKILL.md) | needs-evidence | 公司并购、企业合规 | 入口存在；控制权和申报门槛筛查可辨识；自报 L3 不采信为认证 | 同版本 Proprietary / CC-BY-NC-4.0 冲突；**blocked** |
| [discovery-gutachten-admin](https://github.com/Youchu-lawhub/gutachten-admin-case/blob/49423c6e767ecd6d4e5c0b07fd3a0a8965f85178/SKILL.md) | needs-evidence | 刑事/行政中的行政方向 | 入口存在；W0–W4 行政法分析工作流可辨识；根 README 404 | CC-BY-NC-ND-4.0 及附加限制；**blocked** |

## 阻塞问题、影响与责任

每个 JSON 阻塞对象均包含证据、固定链接、影响、下一步动作和责任角色。没有取得权利人澄清，也没有代 Human Maintainer 向第三方发送消息。角色是待办责任类别，尚未指派或联系具体人员。

| 问题 | 证据与影响 | 后续责任及动作 |
| --- | --- | --- |
| CorpClaim CN、law-ye 缺少许可 | 根 LICENSE 404；完整递归树分别 8、72 项中未找到许可/NOTICE 文件；README 无明确分发授权。结论限于固定版本本次检查，不声称权利不存在 | **权利人**补该提交、规则库和资料的许可范围；**Human Maintainer**审阅，补证前保持 needs-evidence/blocked |
| 经营者集中同版本许可冲突 | SKILL.md L11 写 Proprietary，README/LICENSE 写 CC-BY-NC-4.0；CC 自身还有非商业限制。不得择宽作为复制依据 | **权利人**澄清适用许可、内部使用例外、商用、改编与分发；**Human Maintainer**决定补证是否充分 |
| 两个 Youchu 项目的限制与解释问题 | LICENSE 不仅是 CC-NC-ND 标签：含商业和演绎限制、AI evaluating/benchmarking、RAG/训练、收费平台及机构使用限制。基础 CC 优先和附加条款优先的表述也需解释；不自行判定效力 | **法律专业人员**审阅全文；**Human Maintainer**决定目标使用和是否取得覆盖改编、分发、评测与机构使用的书面许可 |
| litigation-hub 独立能力边界 | 入口主要路由至下游技能并组织序列；下游实体工作流没有逐项审计，不能按套件子技能数转成独立合格条目 | **工程维护者**补可分离的编排能力或单个下游证据；**Human Maintainer**决定目录对象边界 |
| 爽律自定义许可 | 正常收费法律服务明确允许，非商业测试也允许；对外商业集成及公开发布修改版受限，品牌另行约束。不能误写为全面禁止商用或沿用旧许可 | **Human Maintainer**确定收录形态；**法律专业人员**核对当前根与运行包许可；必要时取得**权利人**书面许可 |
| CN Law Hub 贡献者授权范围 | NOTICE L20–L39 明确根 Apache 仅及作者有权许可部分，贡献者未明确许可时不能由 NOTICE 代授。原发现仅确认根许可，不能据此推断整包授权完整 | **Human Maintainer**决定可分离入口范围或要求组件级补证；**权利人/贡献者**补文件、提交与许可对应关系，再重新审计 |

CN Law Hub README 还提示 v2.0.2 release 附旧临时竞赛许可，与本次固定提交不同。本次只认可实际读取版本的许可事实，不对历史许可届满或替换效力作法律裁断，不把旧压缩包当当前提交交付。

## 专业复核与工程交接

全部 10 条仍需具备相关专业能力的法律人员确认实际适用法域、任务边界、法规现行文本、废止/修订/生效和过渡规则，并留存具名、适用场景、版本与截至日期相对应的可追溯证据。专业重点逐条记录于 `professional_review.required_checks`，例如合同阈值、律师收费及解除、公司与数据合规、民事请求权、刑事/行政期限、经营者集中门槛，不能以来源更新日期补齐时效。

3 条 ready 记录仍有使用前工程交接事项：contract-review 的安装示例目录与根入口不一致，依赖 Windows officecli；china-legal-counsel 的入口包含作者本机知识库绝对路径；contract-review-zh 的外部笔记与可选工具不由项目根许可或宿主名称自动覆盖。它们不阻碍提交入口文档给专业人员阅读，但在任何后续安装、完整包分发前须分别解决。所有宿主兼容性均未实际测试，gutachten-admin-case 没有根 README 也不据此猜测宿主。

**Human Maintainer 待决事项**：安排专业复核人员、决定 7 条阻塞的补证路径及拟使用范围、决定 litigation-hub 是否应作为独立对象、决定 CN Law Hub 组件授权或可分离范围。解除阻塞后应重新审计；正式入库另开 P1 PR，满足正式 Schema、法域和时效要求，再由 Human Maintainer 批准合并。

## 数据契约与离线校验

顶层字段为 `format_version: 1`、`task: LR-P0-03`、`audited_at` 和非空 `records`。记录字段及所有嵌套对象都禁止额外属性。该版本是 P0 工程准备快照，**不接受法规时效 verified 或专业审核已完成**；后续专业核查需另建有证据的审核流程和 PR，不能在本清单直接改一个状态绕过门槛。

| 字段 | 要求 |
| --- | --- |
| `candidate_id` | 必须存在于原候选清单；恰好一条准备记录对应一条候选，不得遗漏、重复或引入未知 ID |
| `candidate_snapshot_sha256` | 对原候选全部字段按键排序、UTF-8、ensure_ascii=False、紧凑 JSON（separators 为逗号/冒号）计算 SHA-256；任一字段变化要求重新审计，不是签名或权属证明 |
| `source_url` / `revision` / `business_categories` | 与原候选保持一致，固定完整 40 位提交；`category_evidence` 独立说明分类依据 |
| `audit_evidence` | 固定版本 URL、kind、read/not-found、blob SHA/null、实际定位和原创 finding；仅使用该候选仓库/提交的文件及递归树 URL |
| `source_review` | 来源状态、入口存在、工作流类型和结论；入口存在声明须对应 read 的实际入口记录 |
| `authorization_review` | clear / missing-license / conflicting / restricted / scope-unclear / not-permitted；保留原许可标签，说明限制及结论；clear 不能绕过原 pending/restricted |
| `jurisdiction` / `regulatory_currency` | 与原记录完整一致；时效仅 not-checked/pending-verification，日期必须 null |
| `runtime_review` | 原载体、source-declared-unexecuted、证据及局限 |
| `professional_review` | not-performed、legal-professional、具体 required_checks |
| `blockers` | blocked/rejected 必须至少一条，含 code、evidence、evidence_urls、impact、next_action、owner；ready 不得含未解决阻塞 |
| `follow_up` | 明确 owner/action，必须同时安排 Human Maintainer 决策与 legal-professional 复核责任 |
| `p1_status` | 仅三个准备状态；ready 还要求原 candidate、已核对许可、clear、入口和独立工作流证据；已 rejected/not-permitted 不得静默恢复 |

```sh
python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
python scripts/validate_p1_readiness.py tests/fixtures/p1-readiness/valid.json --candidates tests/fixtures/p1-readiness/candidates.json
python scripts/validate_skills.py skills
python scripts/validate_candidates.py data/discovery/candidates.json
python -m unittest discover -s tests -v
git diff --check
```

校验器默认使用真实候选和准备清单，`--candidates` 可指定配对样本。退出码成功 0、数据错误 1、参数错误 2；错误报告文件和 JSON Pointer，JSON 语法错误含行列。拒绝重复 JSON 键、NaN/Infinity、非 UTF-8、缺失路径及无效候选输入。校验器不联网抓取来源、不执行候选，不把摘要匹配视为来源、授权或专业事实已验证。

正样本和所有反向变异均为合成工程数据。测试覆盖未知/遗漏/重复 ID、原字段与快照漂移、非法状态、无因阻塞、授权升级、日期冒充时效、同时篡改两份清单仍不能标时效 verified、证据未固定版本、伪造入口读取结果、责任遗漏和 JSON 异常；禁用 socket 的测试验证检查无需网络。

GitHub Actions 执行真实清单、合成正样本及全部正反测试，验证步骤不读取实时第三方来源或调用第三方服务。沿用现有 checkout、Python 与固定依赖安装基础设施，没有新增依赖。CI 成功仅证明工程检查通过，实际运行链接及结果以对应 PR 为准。

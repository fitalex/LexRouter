# 发现候选区

## P1 批次 01（2026-10-17）

[p1-batch-01.json](p1-batch-01.json) 新增 **10** 条独立入口候选（7 个原仓库），按既有契约记录；与原 10 条联合初筛后 **20** 条候选记录。机器检查 ID/同源入口，人工比较工作流；原套件导航的独立性阻塞仍保留，20 不是已核实独立能力或正式入库数量。逐项证据、许可、模式、责任和检索记录见 [审核表](../../docs/P1_BATCH_01_REVIEW.md)。

本批为 A 建议 **3**、C 建议 **7**，新增独立 B 机会 **0**。连同 P0 既有提案，累计 A 建议 **6**、C 建议 **14**、独立 B 机会 **4**（未研发）。新批次未做 readiness 审计或批准；本批许可明确 **4**、受限 **1**、待核 **5**；全部 **10** 项专业复核未开展、时效 `not-checked / null`。累计 **20** 条待专业复核，正式入库 **0**。以下 P0 统计保留原审计时间和口径，不覆盖历史记录。

| 业务分类（可多选） | P0 | 本批新增 | 联合 |
| --- | ---: | ---: | ---: |
| 合同审查 | 4 | 1 | 5 |
| 民商事诉讼 | 3 | 1 | 4 |
| 公司并购 | 1 | 2 | 3 |
| 企业合规 | 2 | 3 | 5 |
| 刑事/行政 | 3 | 3 | 6 |
| 法律检索 | 3 | 1 | 4 |

```sh
python scripts/validate_candidates.py data/discovery/p1-batch-01.json
python scripts/validate_discovery_batches.py data/discovery/candidates.json data/discovery/p1-batch-01.json
```

## P0 历史快照

[candidates.json](candidates.json) 是 LR-P0-02 的发现证据清单，不是正式 Skill 元数据目录、安装清单或推荐列表。契约、状态与进入 P1 的条件见 [发现协议](../../docs/DISCOVERY_PROTOCOL.md)。核查日期为 **2026-10-16**，证据链接固定到实际读取的 GitHub HEAD 提交；没有运行任何候选。

## 本次发现范围与统计

LR-P0-03 于 **2026-10-16** 对这 10 条记录逐项复核，结果见 [p1-readiness.json](p1-readiness.json) 与 [P1 准备审计说明](../../docs/P1_READINESS.md)。独立准备状态为 **3** 条 ready-for-professional-review、**7** 条 blocked、**0** 条 rejected；不修改下列 LR-P0-02 发现状态或把它们合并成正式 Skill 数。新发现 CN Law Hub 的 NOTICE 对贡献者组件授权作出保留，因此原 candidate 的该入口在本轮准备中仍被阻塞。

六个原 needs-evidence 均继续阻塞：2 个缺少许可、2 个 CC-NC-ND 加附加条款、1 个自定义许可、1 个 Proprietary/CC-BY-NC 冲突。两份 CC 许可还限制 AI 评估/基准测试、机构使用与收费平台分发；爽律则明确允许正常收费法律服务，限制的是 Skill 的对外商业化及公开修改版本。完整证据、影响、动作和责任方逐项记录于准备清单；尚未取得任何新增权利人授权。法域和法规时效的专业复核完成数仍均为 0。

公开 Web/GitHub 检索词包括 `github 法律 skills 合同审查 中国`、`github 法律 skills 民商事 诉讼 刑事 行政`、`site:github.com 法律 skill 公司 并购 尽职调查`、`site:github.com 法律 skill 行政 复议 刑事`。搜索摘要和聚合目录只作线索，再对原仓库执行 `git ls-remote … HEAD`，经 HTTPS 读取该提交 README、入口前部及 LICENSE（存在时）。未下载完整 Skill、安装依赖或执行上游指令。没有建设爬虫或搜索服务；此次为人工发起的有限公开检索，不代表穷尽公开生态或全部载体。

- 发现 **10** 个可追溯能力入口，来自 10 个原仓库；来源已读取 **10**，来源待核实 **0**。
- 判定：`candidate` **4**，`needs-evidence` **6**，`rejected` **0**。10 是已发现记录数，不能称作 10 个合格入库 Skill。
- 授权：固定版本许可文本已核对且无已知冲突 **4**，已识别限制但目标用法待审 **3**，缺失或冲突待核 **3**。
- 法域：来源声明指向中国大陆 **10**，专业复核完成 **0**。法规时效：`not-checked` **10**，完成核查 **0**。
- 正式 `skills/` 条目 **0**；法律测评、专家审核、评分、推荐均未开展。

| 业务分类 | 发现记录数（多选，不能相加作总数） |
| --- | --- |
| 合同审查 | 4 |
| 民商事诉讼 | 3 |
| 法律检索 | 3 |
| 企业合规 | 2 |
| 公司并购 | 1 |
| 刑事/行政 | 3 |

`litigation-hub` 只计一个套件入口，未将其声称的 23 项子技能展开计数。`shuanglv-legal-skills` 也只计一个入口，不推定独立企业合规模块或行政诉讼模块。`other` 载体记录通用 Agent Skills、WorkBuddy/OpenClaw 等原始形态，具体证据见每条 `runtime_evidence`。

## 未核实事项及许可边界

所有记录均待逐条核对法规及法律适用，所有维护者真实身份和专业资质均未独立核实。六个待补证据入口分别涉及两项许可缺失（CorpClaim CN、law-ye）、两项 CC BY-NC-ND 限制（litigation-hub、gutachten-admin-case）、一项自定义许可（爽律）、一项声明冲突（经营者集中评估）。

重要版本差异：爽律固定提交为 ShuangLaw Professional Use License 1.0，不能沿用搜索摘要的历史 CC BY-SA/Apache 声明；经营者集中入口写 Proprietary，而同一提交 README/LICENSE 写 CC BY-NC 4.0，需权利人澄清；CN Law Hub 当前提交为 Apache-2.0，但 README 提醒旧 release 附历史临时竞赛许可，后续须按实际使用版本保留 NOTICE 并复核。

清单只包含原始链接、许可名称和独立撰写的证据简述。第三方内容仍遵循各自授权，不因被发现而适用 LexRouter MIT。许可缺失路径的 404 只证明本次该路径不可用，不能证明整个仓库绝无授权。未核实的外部法律材料、数据源和品牌权利不包含在许可确认中。

```sh
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
```

该命令仅作结构检查，不联网确认来源、许可或法律有效性。新增记录不得写入 `skills/`，不得填造假的法规时效日期。扩充至 P1 批量整理已有工程基础，但正式入库仍依赖授权澄清及法域、法规时效的专业复核。

# 权利与工程预审：企业法务19组件

**agent-precheck；不是法律、权利或入库决定；全部权利门槛not-verified。**

## 固定基线及v1保护

- 原PR #11：https://github.com/fitalex/LexRouter/pull/11；原head `844c9dd68b0061ea9f4451fd89e24cc10d73f3bb`；原base `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8`。
- 材料准备时API current head：`844c9dd68b0061ea9f4451fd89e24cc10d73f3bb`（仅基线快照；合并main及发布后的head由PR提交历史显示）。
- 已接受main：`d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`（PR #15 squash merge）；上游 `73ff53a857ffbdd91296bf41ed5bcc1294bc2042`。
- v1材料保持原字节；未迁移/覆盖工作簿、generated、record、subject、inventory或human-review。v2沿用真实ID，仅新增独立bundle+empty_ledger；本轮无真人事件。

| v1文件（main固定版本） | 原字节SHA256 |
| --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/evidence.md) | `eeb3863115f01959e073fe40ae62a764e9cbd432a237b487cff5e62676663c21` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/generated.json) | `98f0449c78064a3a6584a3cf4fadab6bf44840e7148f7f378755b8b387c55ef3` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/inventory.json) | `08310a3b045d51756f68abca14f23cb69b019a3805e3f860f18ec1df542c4b0e` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/matrix.md) | `2edbc8165e8c52fe346bcec8681626199fe462984f817f3d85bab082a35234a4` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/packet.md) | `024bcac7e933bf97846d3c2a9dbba52db3ffa1ceda87455fc1df83ea3d3e4e73` |
| [record.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/record.json) | `ec991cfa87ede63bb64d7180956d8a51330aef3a940e4c1d333f632e301331a8` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/subject.json) | `a4fc8d81881d5c5f389c48160762aae17abe98a70db9d06df0486ce68fb5a164` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/templates.json) | `896bbd093e303607c01b890c1bc88f79add3396352039230ace762849ff37823` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-china-legal-counsel/workbook.md) | `ff95c3e6c281e20a4f2504b75dd55b1b00736cee9c47ad9f9df5e856d297ff76` |

原PR完整28文件摘要map的SHA256：`e21c1dfbeff7101f5116403c2ef370825f33c3c4fa6b6921ca3b4788bd584f98`；原head tree `783c67bb05a1eda3d0fdcd72da747b4faac27b8b`。原PR本case原字节索引如下，含原human-review及record，不能用main版本覆盖。

| 原PR文件 | Git blob | 原字节SHA256 |
| --- | --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/evidence.md) | `debfda51a8f5e7e0deeb26085ffb580807339e48` | `eeb3863115f01959e073fe40ae62a764e9cbd432a237b487cff5e62676663c21` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/generated.json) | `163aebc9ef99a93e8327b37417ac9ccec42a67aa` | `98f0449c78064a3a6584a3cf4fadab6bf44840e7148f7f378755b8b387c55ef3` |
| [human-review.md](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/human-review.md) | `261eb1929cc7857da667727c865261673d38f144` | `7c359751744e7d683844714b37b867c1419fa06dcef062b35abe7efdf7884c24` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/inventory.json) | `b99b06b6fa4b3db53a4310d557c78f9b4383b3db` | `08310a3b045d51756f68abca14f23cb69b019a3805e3f860f18ec1df542c4b0e` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/matrix.md) | `95c3162de85096b925ad978f36090ac2e9317af4` | `2edbc8165e8c52fe346bcec8681626199fe462984f817f3d85bab082a35234a4` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/packet.md) | `32dd9540b776970ffd3d7d20f6095d65fd0bcf93` | `024bcac7e933bf97846d3c2a9dbba52db3ffa1ceda87455fc1df83ea3d3e4e73` |
| [record.json](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/record.json) | `b21b8be8968c5bc5e51b3480aad1c4b27f4f1711` | `4c60371dad2fd20ac4cf3e491f4c446ef18dee3b614b2cb77672a3db33d1bfe5` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/subject.json) | `294098da2eea657c5ad3065bcb6a4c4600814a71` | `a4fc8d81881d5c5f389c48160762aae17abe98a70db9d06df0486ce68fb5a164` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/templates.json) | `8e11042db106037935db20464ad593ad3f19f22d` | `896bbd093e303607c01b890c1bc88f79add3396352039230ace762849ff37823` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/844c9dd68b0061ea9f4451fd89e24cc10d73f3bb/data/reviews/cases/RV-20261017-china-legal-counsel/workbook.md) | `85a088eba3f4c09923c4ca07458ab7d7f6f54b06` | `ff95c3e6c281e20a4f2504b75dd55b1b00736cee9c47ad9f9df5e856d297ff76` |

完整保护及逐分支比对见[compatibility.md](compatibility.md)；验证命令/限制见[VALIDATION.md](VALIDATION.md)，实际本地与CI证据见[TEST_OUTPUT.md](TEST_OUTPUT.md)。

## 权利预审

| 门槛 | 证据与缺口 | 状态 |
| --- | --- | --- |
| authorization-chain | 根LICENSE署名2026 Suze；与发布者Daknniel-0881及贡献者关系仍缺；公开根许可不证明完整第三方授权链。 [只读证据](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE) | not-verified |
| hosting-scope | 拟审19项；排除2320项。范围固定只是工程事实，逐文件复制/修改/再分发/托管权限及外部服务条件均待核。 [只读证据](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/manifests/discovery-china-legal-counsel.json) | not-verified |
| attribution-and-notices | 根MIT允许的使用/复制/修改/再分发须保留版权及许可通知；不覆盖无权授权的第三方内容；固定完整tree未见NOTICE文件，不证明没有第三方通知义务。 [只读证据](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE) | not-verified |

固定根许可证只读摘要：[LICENSE](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE)，blob `135c200182eb6e3d75ca3ef618ab7af43e6d7e7e`。根LICENSE署名2026 Suze；与发布者Daknniel-0881及贡献者关系仍缺。根MIT允许的使用/复制/修改/再分发须保留版权及许可通知；不覆盖无权授权的第三方内容。完整固定tree的NOTICE路径观察：[]（未见，不是不存在通知义务的法律结论）。本仓库仅记录原创摘要，不提交许可证全文抓取缓存。

| 文件 | 原manifest权利依据 | 未决用途/条件 |
| --- | --- | --- |
| [LICENSE](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [README.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/README.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [SKILL.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [agents/openai.yaml](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/agents/openai.yaml) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/citation-verification.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/citation-verification.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/compliance-check-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/compliance-check-playbook.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-drafting-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/contract-drafting-playbook.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-review-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/contract-review-playbook.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/eval-plan.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/eval-plan.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/legal-consultation-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/legal-consultation-playbook.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/output-schemas.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/output-schemas.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/risk-and-escalation.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/risk-and-escalation.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/source-registry.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/source-registry.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/chunk_legal_doc.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/chunk_legal_doc.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/fetch_official_sources.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/fetch_official_sources.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/ingest_source_registry.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/ingest_source_registry.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/kb_search.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/kb_search.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/normalize_legal_doc.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/normalize_legal_doc.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/verify_citations.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/verify_citations.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |

## 工程边界与阻塞

- 确认 Suze 与仓库发布者及贡献者关系；知识库原始/清洗/切片、商业数据库、律所文章、品牌图像和用户背景均不随 MIT 自动授权，本范围全部排除。
- 绝对路径须后续单独适配；Python 脚本默认相对 knowledge-base 并支持 --kb；不含知识库的组件不能声称完整可用。curl/pdftotext 与官方站点访问条件另审。
- fetch_official_sources.py 存在特定主机 curl TLS 放宽回退；上线前另审和修正，当前不运行。引用字符串存在检查不等于法律效力或结论校验。
- 确认实际适用法域、固定版本及目标使用场景；逐条核对官方现行文本、生效/废止/过渡规则，并留存具名专业复核证据。
- 逐项核验合同、广告、数据、劳动及公司治理规则的法域、现行文本与场景适用。
- 抽查知识库来源与引用是否真正支持结论，确认重大事项人工升级边界。

本轮仅生成和验证LexRouter材料，未下载入库上游全文、未运行脚本/安装依赖/打包Skill。固定Git tree比对由同轮基线报告留证；19+2320=2339文件清单完整。矩阵 304 行，五组涵盖 16 项；schema/coverage通过只证明结构。空ledger由主程序empty_ledger生成，其bundle_sha256绑定当前bundle。签署PR的程序/工作流/政策输入必须与main一致。

## 待人工确认清单

- [ ] 确认精确拟用场景、全部路径和排除边界；如缩放范围或修法改变实质附件另立Review。
- [ ] 对逐file/check补真实事实、官方条款与版本、支持/反例、有效期间、废止/替代/过渡和明确限制；任何not-verified不得转写通过。
- [ ] 权利人/贡献者链、第三方来源、托管权利与署名/NOTICE全部核实；需要许可时由维护者处理，不由AI联系或造证。
- [ ] 本人能力/资质、角色及credential_refs由维护者在main单独接受；公开仅经允许的不透明索引。
- [ ] 本人逐组决定、总体理由/限制、COI、实际核法日期；本稿不预填且未发Review。
- [ ] 专业通过后维护者审权利/工程/剩余阻塞，以第二个独立本人事件作入库决定；合并仍待维护者。
- [ ] 确认材料跟进提醒2026-11-20及法规/许可/来源变化立即复核安排；该提醒不等于法规有效期。

真实签署与入库属于后续Gate 3；本轮不把needs-changes占位或工程测试制造成真人意见。

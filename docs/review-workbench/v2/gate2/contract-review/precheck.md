# 权利与工程预审：通用合同审查

**agent-precheck；不是法律、权利或入库决定；全部权利门槛not-verified。**

## 固定基线及v1保护

- 原PR #9：https://github.com/fitalex/LexRouter/pull/9；原head `a7c7d9541e0f6b84a30d5643890de59ed4673a7b`；原base `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8`。
- 材料准备时API current head：`a7c7d9541e0f6b84a30d5643890de59ed4673a7b`（仅基线快照；合并main及发布后的head由PR提交历史显示）。
- 已接受main：`d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`（PR #15 squash merge）；上游 `f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`。
- v1材料保持原字节；未迁移/覆盖工作簿、generated、record、subject、inventory或human-review。v2沿用真实ID，仅新增独立bundle+empty_ledger；本轮无真人事件。

| v1文件（main固定版本） | 原字节SHA256 |
| --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/evidence.md) | `673870a7ac876f1e514b8d2291f2cf31f2b5d1e54f9185aefa500f0421406b1b` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/generated.json) | `f7fb16b5540de00f35719ca614aeb1dbd1e4c3ac12f423fbcfbccc87f0546a8c` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/inventory.json) | `d85149f120972ca1b9461d6bc9ab041fb2be3d6a6be7ff6323bd37c14dd09c65` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/matrix.md) | `e7906dd52adcb145eb28d8cfc6cf0f9d37cdefa94fed9a8966ebc3c4bfbc3123` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/packet.md) | `a324392a3da5c95d7e225878e89486107f2d4eecba6ce28c511864fb616c3dff` |
| [record.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/record.json) | `674531c32ea60c6a0c1b798b8fd45f9a0dec1a4be4f18ffb26b5eb0b680e1e75` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/subject.json) | `d3fd158e502a4db212d6302030d776296bb6694cfa251187aa784e398a5eb346` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/templates.json) | `28d06cfd7d4e439791ffe3c9e92f9fa8a6e34682ec3c1e70f103fd5125c30b37` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review/workbook.md) | `64e4dba20ff145d5791043b022b8709583fac65a3289ecb4d3489553cfdb0de4` |

原PR完整28文件摘要map的SHA256：`2d94697f2243f79e9410c812fb39b1262b3b86dcc9ee870ce720c6511e588596`；原head tree `447b6368c9506ca73013ac6767f7f9dbe444613b`。原PR本case原字节索引如下，含原human-review及record，不能用main版本覆盖。

| 原PR文件 | Git blob | 原字节SHA256 |
| --- | --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/evidence.md) | `539bcc57e9957d30d4e616403fc6592a596454e4` | `673870a7ac876f1e514b8d2291f2cf31f2b5d1e54f9185aefa500f0421406b1b` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/generated.json) | `6a0ac82f97e75a6e8d6a7e00199866131d3e53c1` | `f7fb16b5540de00f35719ca614aeb1dbd1e4c3ac12f423fbcfbccc87f0546a8c` |
| [human-review.md](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/human-review.md) | `9997bc9843e252fab5f6daaa5b4ab5f392f23058` | `c31050d05b0625125a8bc31eba5b72b1db130f197c501208fef99daaf4bb8207` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/inventory.json) | `ec17831f5eca745cb22bf45c4f22014cbcbe1c1c` | `d85149f120972ca1b9461d6bc9ab041fb2be3d6a6be7ff6323bd37c14dd09c65` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/matrix.md) | `e373f15bd50bb488cfce313a231e83c908ef5c9b` | `e7906dd52adcb145eb28d8cfc6cf0f9d37cdefa94fed9a8966ebc3c4bfbc3123` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/packet.md) | `64837da745326e5e7562d1d77ea76e67562c9f18` | `a324392a3da5c95d7e225878e89486107f2d4eecba6ce28c511864fb616c3dff` |
| [record.json](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/record.json) | `c2dc96234d315359e6f61a3d61df13ec3e1dcd78` | `e5cf8cb463ff767e687b6d24ec416a4d0d10c085a50e62aa407db469aeae3fdd` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/subject.json) | `831a6c4e242761296192ff4245e53f0a53d5cba9` | `d3fd158e502a4db212d6302030d776296bb6694cfa251187aa784e398a5eb346` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/templates.json) | `285b323758b63504db4793446a96a4235f72107b` | `28d06cfd7d4e439791ffe3c9e92f9fa8a6e34682ec3c1e70f103fd5125c30b37` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/a7c7d9541e0f6b84a30d5643890de59ed4673a7b/data/reviews/cases/RV-20261017-contract-review/workbook.md) | `999e0739e94bb42a4c92c6de5e6e54032f941884` | `64e4dba20ff145d5791043b022b8709583fac65a3289ecb4d3489553cfdb0de4` |

完整保护及逐分支比对见[compatibility.md](compatibility.md)；验证命令/限制见[VALIDATION.md](VALIDATION.md)，实际本地与CI证据见[TEST_OUTPUT.md](TEST_OUTPUT.md)。

## 权利预审

| 门槛 | 证据与缺口 | 状态 |
| --- | --- | --- |
| authorization-chain | 根LICENSE署名2026 NOMOREKKK；实际作者及贡献者权利链仍缺；公开根许可不证明完整第三方授权链。 [只读证据](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE) | not-verified |
| hosting-scope | 拟审27项；排除4项。范围固定只是工程事实，逐文件复制/修改/再分发/托管权限及外部服务条件均待核。 [只读证据](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/manifests/discovery-contract-review.json) | not-verified |
| attribution-and-notices | 根MIT允许的使用/复制/修改/再分发须保留版权及许可通知；不覆盖无权授权的第三方内容；固定完整tree未见NOTICE文件，不证明没有第三方通知义务。 [只读证据](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE) | not-verified |

固定根许可证只读摘要：[LICENSE](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE)，blob `1c3ef4997530ff41a93fb627c8f6d31d85d7a2cd`。根LICENSE署名2026 NOMOREKKK；实际作者及贡献者权利链仍缺。根MIT允许的使用/复制/修改/再分发须保留版权及许可通知；不覆盖无权授权的第三方内容。完整固定tree的NOTICE路径观察：[]（未见，不是不存在通知义务的法律结论）。本仓库仅记录原创摘要，不提交许可证全文抓取缓存。

| 文件 | 原manifest权利依据 | 未决用途/条件 |
| --- | --- | --- |
| [LICENSE](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [README.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/README.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/clause-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-checklist.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/clause-conflict-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-conflict-detection.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/compliance-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/compliance-checklist.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-type-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-type-detection.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/construction-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/construction-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/employment-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/employment-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/equity-investment.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/equity-investment.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/lease-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/lease-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/nda.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/nda.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/oem-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/oem-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/purchase-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/purchase-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/sales-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/sales-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/service-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/service-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/contract-types/tech-development-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/tech-development-contract.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/financial-amounts.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/financial-amounts.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/output-format.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/output-format.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/risk-matrix.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/risk-matrix.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/terminology-glossary.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/terminology-glossary.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [references/text-quality-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/text-quality-checklist.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/annotate_docx.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/annotate_docx.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/check_text_quality.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/check_text_quality.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/detect_contract_type.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/detect_contract_type.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/parse_contract.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/parse_contract.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [scripts/validate.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/validate.py) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |

## 工程边界与阻塞

- 确认 NOMOREKKK 及贡献者对拟用文档、规则、脚本的授权链；MIT 不覆盖外部服务；跨境贸易术语、法条汇编及二进制模板另行核实。
- 根入口与安装示例不一致；Python 3.10+、Windows officecli 版本/API/许可证、OCR 与检索连接器需单独确认；不执行上游。
- 确认实际适用法域、固定版本及目标使用场景；逐条核对官方现行文本、生效/废止/过渡规则，并留存具名专业复核证据。
- 核对违约金、利息及保证金阈值的适用条件，避免把经验阈值写成普遍强制规则。
- 逐条核验合同分类规则、民法典及司法解释的生效、废止与过渡规定。

本轮仅生成和验证LexRouter材料，未下载入库上游全文、未运行脚本/安装依赖/打包Skill。固定Git tree比对由同轮基线报告留证；27+4=31文件清单完整。矩阵 405 行，五组涵盖 15 项；schema/coverage通过只证明结构。空ledger由主程序empty_ledger生成，其bundle_sha256绑定当前bundle。签署PR的程序/工作流/政策输入必须与main一致。

## 待人工确认清单

- [ ] 确认精确拟用场景、全部路径和排除边界；如缩放范围或修法改变实质附件另立Review。
- [ ] 对逐file/check补真实事实、官方条款与版本、支持/反例、有效期间、废止/替代/过渡和明确限制；任何not-verified不得转写通过。
- [ ] 权利人/贡献者链、第三方来源、托管权利与署名/NOTICE全部核实；需要许可时由维护者处理，不由AI联系或造证。
- [ ] 本人能力/资质、角色及credential_refs由维护者在main单独接受；公开仅经允许的不透明索引。
- [ ] 本人逐组决定、总体理由/限制、COI、实际核法日期；本稿不预填且未发Review。
- [ ] 专业通过后维护者审权利/工程/剩余阻塞，以第二个独立本人事件作入库决定；合并仍待维护者。
- [ ] 确认材料跟进提醒2026-11-20及法规/许可/来源变化立即复核安排；该提醒不等于法规有效期。

真实签署与入库属于后续Gate 3；本轮不把needs-changes占位或工程测试制造成真人意见。

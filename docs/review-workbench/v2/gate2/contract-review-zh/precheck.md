# 权利与工程预审：律师服务合同审查

**agent-precheck；不是法律、权利或入库决定；全部权利门槛not-verified。**

## 固定基线及v1保护

- 原PR #10：https://github.com/fitalex/LexRouter/pull/10；原head `ed445c825a6f7d9ee6396b1a77a820a5a000ba58`；原base `a21484a36ca53f8ac9e009626b5f3a34a3e3b7b8`。
- 材料准备时API current head：`ed445c825a6f7d9ee6396b1a77a820a5a000ba58`（仅基线快照；合并main及发布后的head由PR提交历史显示）。
- 已接受main：`d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`（PR #15 squash merge）；上游 `b8382b59d2ba3157125a779a0abf251ec0c29717`。
- v1材料保持原字节；未迁移/覆盖工作簿、generated、record、subject、inventory或human-review。v2沿用真实ID，仅新增独立bundle+empty_ledger；本轮无真人事件。

| v1文件（main固定版本） | 原字节SHA256 |
| --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/evidence.md) | `1c25f01f3dc03b4e20e44796de4c0ec11550faab2ed086b03923e08e80e2fa85` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/generated.json) | `ea457ea049f0effb6be0ed6f48b675cdde60fe115279724d6033c23075ebb0e7` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/inventory.json) | `3366efdc0ec544b3618477fb18b70d8d31db57613ed23c06a67f4ab8c7029bff` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/matrix.md) | `4e397b95ac6c2ecfd6c3f4a6d94e06605083f2ff523a599e6837141510d9524e` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/packet.md) | `76c09d0cbf709e012903269b2d93136ae6def9f6ed034b9ba9cf5ee0ceea5b2e` |
| [record.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/record.json) | `db03fb017086a6b572502c253015f4b9ff75254260a840b58998b44666d24bff` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/subject.json) | `0e372898b60459e6ac3f5530f14edf6fd4309be1899b17ab45a7251c7b586b8a` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/templates.json) | `105aae8f066e766ba8e76452c651bc8ce0940b6ef86db485c92a5997599c2245` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/cases/RV-20261017-contract-review-zh/workbook.md) | `d07cbc071b2e97f1a94c50b6b301343360b3450ef00effb35bfa0ddeb245ab88` |

原PR完整28文件摘要map的SHA256：`a92e841ff59f85e4320be4612a6355912a087aae82eef8f81f567cc9286175df`；原head tree `af4048aa110e11a09ab8201d78bbfe499fe835fc`。原PR本case原字节索引如下，含原human-review及record，不能用main版本覆盖。

| 原PR文件 | Git blob | 原字节SHA256 |
| --- | --- | --- |
| [evidence.md](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/evidence.md) | `30a678ae94e533e66e43e2085f8b79334a882519` | `1c25f01f3dc03b4e20e44796de4c0ec11550faab2ed086b03923e08e80e2fa85` |
| [generated.json](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/generated.json) | `7107d1c9c7fcc9b8bae820207726c6c2e8507b04` | `ea457ea049f0effb6be0ed6f48b675cdde60fe115279724d6033c23075ebb0e7` |
| [human-review.md](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/human-review.md) | `bd9bd5570ef21ed83a669183afc14af79212bdcb` | `56ab76ec293e4d7f6828a6a7fa4573dbfcb00784b56023c898be756751b5fff1` |
| [inventory.json](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/inventory.json) | `6b34e589d84576f6f7704d8ccb73230482d6a2d6` | `3366efdc0ec544b3618477fb18b70d8d31db57613ed23c06a67f4ab8c7029bff` |
| [matrix.md](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/matrix.md) | `1db8708058defbc7cf16731fbc59ba0b91939cdc` | `4e397b95ac6c2ecfd6c3f4a6d94e06605083f2ff523a599e6837141510d9524e` |
| [packet.md](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/packet.md) | `2a6aec532ad834fe320ad5ebf420672b6e852389` | `76c09d0cbf709e012903269b2d93136ae6def9f6ed034b9ba9cf5ee0ceea5b2e` |
| [record.json](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/record.json) | `6a41cd3fec0247df2c32d01d8cf482bf581546c2` | `2039c2d34581b1f0c03e9e1f14b07886b9735b70a94b01a2e6bbe639ac1f8c76` |
| [subject.json](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/subject.json) | `eb4b3a05e0b64de217ed2524a4bffa2d921c2a7b` | `0e372898b60459e6ac3f5530f14edf6fd4309be1899b17ab45a7251c7b586b8a` |
| [templates.json](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/templates.json) | `50aff2a9ad62b000ea562f0cade71f69ad158cb9` | `105aae8f066e766ba8e76452c651bc8ce0940b6ef86db485c92a5997599c2245` |
| [workbook.md](https://github.com/fitalex/LexRouter/blob/ed445c825a6f7d9ee6396b1a77a820a5a000ba58/data/reviews/cases/RV-20261017-contract-review-zh/workbook.md) | `c1164cfe877db4d4338c54cf3fb0e1660335d83f` | `d07cbc071b2e97f1a94c50b6b301343360b3450ef00effb35bfa0ddeb245ab88` |

完整保护及逐分支比对见[compatibility.md](compatibility.md)；验证命令/限制见[VALIDATION.md](VALIDATION.md)，实际本地与CI证据见[TEST_OUTPUT.md](TEST_OUTPUT.md)。

## 权利预审

| 门槛 | 证据与缺口 | 状态 |
| --- | --- | --- |
| authorization-chain | 根Apache-2.0附录仍为未填写的年份/权利人占位；ThomasLiu是仓库路径，不能代替作者授权证据；公开根许可不证明完整第三方授权链。 [只读证据](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE) | not-verified |
| hosting-scope | 拟审4项；排除9项。范围固定只是工程事实，逐文件复制/修改/再分发/托管权限及外部服务条件均待核。 [只读证据](https://github.com/fitalex/LexRouter/blob/d1c7ebabd5c33d2e92c6916804adc4018c89e5a0/data/reviews/manifests/discovery-contract-review-zh.json) | not-verified |
| attribution-and-notices | 根Apache-2.0第4节要求随附许可、修改标识、保留相关通知及存在时的NOTICE；专利许可和商标边界须单核；固定完整tree未见NOTICE文件，不证明没有第三方通知义务。 [只读证据](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE) | not-verified |

固定根许可证只读摘要：[LICENSE](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE)，blob `d645695673349e3947e8e5ae42332d0ac3164cd7`。根Apache-2.0附录仍为未填写的年份/权利人占位；ThomasLiu是仓库路径，不能代替作者授权证据。根Apache-2.0第4节要求随附许可、修改标识、保留相关通知及存在时的NOTICE；专利许可和商标边界须单核。完整固定tree的NOTICE路径观察：[]（未见，不是不存在通知义务的法律结论）。本仓库仅记录原创摘要，不提交许可证全文抓取缓存。

| 文件 | 原manifest权利依据 | 未决用途/条件 |
| --- | --- | --- |
| [LICENSE](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [README.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/README.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [SKILL.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/SKILL.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |
| [docs/how-it-works.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/docs/how-it-works.md) | root-license-pending-chain | not-verified；作者/贡献者与第三方权利链、拟托管复制/修改/再分发、署名/NOTICE逐项补证 |

## 工程边界与阻塞

- Apache 附录版权占位符不能冒充作者声明；确认版权主体/贡献者链、笔记作者及案例/模板授权和必要 NOTICE；4 个 references 与示例暂不纳入可审核核心。
- Claude Code/Claude.ai 的 Read、Word/PDF/图像及 references 打包能力待验证；仅上传 SKILL.md 不证明子目录已上传。
- 与通用合同审查流程有重叠，委托律师合同收费/退费专项可区分；按一个独立候选复核，不按模式/资料拆分凑数。
- 确认实际适用法域、固定版本及目标使用场景；逐条核对官方现行文本、生效/废止/过渡规则，并留存具名专业复核证据。
- 重点核对律师收费、风险代理比例与禁止范围、委托解除和退费规则的现行依据与适用前提。
- 审查来源所称 70 篇笔记的证据可靠性及任何拟复制资料的第三方权利；自述调研与平台热度不作法律认证。

本轮仅生成和验证LexRouter材料，未下载入库上游全文、未运行脚本/安装依赖/打包Skill。固定Git tree比对由同轮基线报告留证；4+9=13文件清单完整。矩阵 60 行，五组涵盖 15 项；schema/coverage通过只证明结构。空ledger由主程序empty_ledger生成，其bundle_sha256绑定当前bundle。签署PR的程序/工作流/政策输入必须与main一致。

## 待人工确认清单

- [ ] 确认精确拟用场景、全部路径和排除边界；如缩放范围或修法改变实质附件另立Review。
- [ ] 对逐file/check补真实事实、官方条款与版本、支持/反例、有效期间、废止/替代/过渡和明确限制；任何not-verified不得转写通过。
- [ ] 权利人/贡献者链、第三方来源、托管权利与署名/NOTICE全部核实；需要许可时由维护者处理，不由AI联系或造证。
- [ ] 本人能力/资质、角色及credential_refs由维护者在main单独接受；公开仅经允许的不透明索引。
- [ ] 本人逐组决定、总体理由/限制、COI、实际核法日期；本稿不预填且未发Review。
- [ ] 专业通过后维护者审权利/工程/剩余阻塞，以第二个独立本人事件作入库决定；合并仍待维护者。
- [ ] 确认材料跟进提醒2026-11-20及法规/许可/来源变化立即复核安排；该提醒不等于法规有效期。

真实签署与入库属于后续Gate 3；本轮不把needs-changes占位或工程测试制造成真人意见。

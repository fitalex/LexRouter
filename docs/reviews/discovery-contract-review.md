# discovery-contract-review：固定版本材料清单

预审日期：2026-10-16；状态：**未批准托管、未专业复核、未入库**。中国大陆法域仅沿用来源声明；法规时效保持 `not-checked / null`。

- 原仓库：https://github.com/NOMOREKKK/contract-review-skill
- 固定 Commit：`f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`（[入口](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)）
- 固定 Tree：`15bdc91c1ad2b4a49d991e305d881847ad192446`；文件数：31。
- 独立逐文件清单：[discovery-contract-review.json](../../data/reviews/manifests/discovery-contract-review.json)，包含**每个文件**的路径、blob、mode、作用、阅读深度及四类拟议决策。
- [交接记录](../../data/reviews/p1-handoff.json) · [阅读方法与限制](README.md) · [专业复核待办](P1_LEGAL_REVIEW_HANDOFF.md#discovery-contract-review)。

## 许可与拟托管范围

根 LICENSE 为 MIT，版权 `2026 NOMOREKKK`；固定树无 NOTICE 或子目录许可文件。MIT 文字涉及软件及关联文档，README 也声明 MIT。没有逐一证明参考资料、模板的作者与贡献者链。根许可不覆盖商业数据库输出、OCR 服务、连接器、品牌或合同输入。

拟提交用途审核的 27 文件：入口、README、LICENSE、5 个 Python 脚本与其余 19 个参考规则；仍需贡献者来源和具体用途确认。`references/law-sources.md` 的预录引用/汇编来源、`references/contract-types/cross-border-trade.md` 中 Incoterms 2020 等第三方贸易术语材料标 `requires-authorization`，应明确哪些为原作者说明、哪些属于受第三方权利约束的摘编；不据名称认定侵权或自由使用。Word 模板标 `unverified`（未解析内容、元数据、嵌入资源或作者身份）。`.gitignore` 明确排除。本次不是可运行的完整包批准，删除参考后也不能宣称功能等价。

## 依赖与安装问题

| 依赖 | 必需性与证据 | 未解决问题 / 角色 |
| --- | --- | --- |
| Claude 类宿主、提问与文件工具 | 入口 Step 0 使用 AskUserQuestion；README 安装到 `~/.claude/skills/` | 宿主权限与工具映射未经运行验证 / 工程维护者 |
| Python 3.10+ | README 安装及依赖段；5 个脚本静态导入以标准库为主 | 未指定完整运行锁定环境 / 工程维护者 |
| Windows officecli | Word 解析、批注、自检所需；脚本 `get_officecli_path` 检索 LOCALAPPDATA、PATH 和 Windows 路径 | 版本、batch API、安装和分发许可单独核对；未包含其程序 / 工程维护者、许可人员 |
| textin-xparse | PDF/扫描件分支实际依赖 OCR；纯文本分支可跳过 | README 称可选，入口扫描件分支依赖；数据上传权限、收费及来源条款待审 / 工程维护者 |
| fyopen-lawsearch | 入口 Step 4 默认检索；可回退预录法条 | 连接器与检索结果权利另审；回退模型常识可能产生旧法引用 / 法律人员 |
| pkulaw、browser-skill、westock-data、计算工具 | 入口协同表；类案/临时查询为可选，上市关联交易场景强制 westock-data | 不随包授权，工具是否存在、查询许可和结果可再分发范围待确认 / 维护者 |

README 安装段 `cp -r contract-review/contract-review ...` 与实际根级 `SKILL.md` 不对应，固定树没有该子目录。根参考文件实际有 11 个 contract-types，而部分说明称 9 类；需独立工程修正 PR，不能静默改上游固定版本。`references/clause-conflict-detection.md` 的方法分类与入口表述也需适配验证。本轮未做安装或批注生成测试。

## 补充授权与不能确认事项

Human Maintainer/许可人员确认拟用文件的提供者与贡献者权利、对具体复制/改编/分发/测评及商用场景的覆盖；如现有 MIT 授权链已足够，不重复索取许可。外部规则摘编、贸易术语与模板补证不足时继续隔离。没有检查完整提交历史、模板内容和外部工具许可，也没有确认完整包可独立运行。法律人员另核“违约金 30%”“LPR 四倍”“保证金 20%”、旧合同法引用、建筑资质和数据合规等规则，不能将经验阈值当普遍法定上限。

## 文件证据索引

以下表格列出非知识库文件；每条链接均固定版本，完整 blob SHA 和逐件决定以 JSON 清单为准。`E`=eligible-for-scope-review，`R`=requires-authorization，`X`=exclude-from-hosting，`U`=unverified。E 仅允许提交用途授权审核。

| 原路径 / 类型 | 作用 | 决策 / 阅读 |
| --- | --- | --- |
| [.gitignore](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/.gitignore) / text | 开发排除规则 | X / static-scan |
| [LICENSE](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE) / text | 项目根许可及版权条件证据 | E / read |
| [README.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/README.md) / md | 安装、能力、限制和来源声明 | E / read |
| [SKILL.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md) / md | 宿主触发条件、法律任务与工作流入口 | E / read |
| [assets/contract-review-template.docx](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/assets/contract-review-template.docx) / docx | 上游声称的空白 Word 样式模板，未解析二进制 | U / not-read |
| [references/clause-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-checklist.md) / md | 通用合同条款检查清单 | E / static-scan |
| [references/clause-conflict-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/clause-conflict-detection.md) / md | 交叉条款冲突识别规则 | E / static-scan |
| [references/compliance-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/compliance-checklist.md) / md | 合同触发的行业和数据合规规则 | E / static-scan |
| [references/contract-type-detection.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-type-detection.md) / md | 合同类型分类参考规则 | E / static-scan |
| [references/contract-types/construction-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/construction-contract.md) / md | 对应 construction-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/cross-border-trade.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/cross-border-trade.md) / md | 对应 cross-border-trade 类型的合同专项检查规则 | R / static-scan |
| [references/contract-types/employment-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/employment-contract.md) / md | 对应 employment-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/equity-investment.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/equity-investment.md) / md | 对应 equity-investment 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/lease-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/lease-contract.md) / md | 对应 lease-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/nda.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/nda.md) / md | 对应 nda 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/oem-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/oem-contract.md) / md | 对应 oem-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/purchase-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/purchase-contract.md) / md | 对应 purchase-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/sales-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/sales-contract.md) / md | 对应 sales-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/service-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/service-contract.md) / md | 对应 service-contract 类型的合同专项检查规则 | E / static-scan |
| [references/contract-types/tech-development-contract.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/contract-types/tech-development-contract.md) / md | 对应 tech-development-contract 类型的合同专项检查规则 | E / static-scan |
| [references/financial-amounts.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/financial-amounts.md) / md | 金额抽取、计算与经验阈值 | E / static-scan |
| [references/law-sources.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/law-sources.md) / md | 法规索引、预录引用与检索入口 | R / static-scan |
| [references/output-format.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/output-format.md) / md | Word 批注和附录输出格式 | E / static-scan |
| [references/risk-matrix.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/risk-matrix.md) / md | 风险分级与阈值参考 | E / static-scan |
| [references/terminology-glossary.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/terminology-glossary.md) / md | 法律术语检查参考 | E / static-scan |
| [references/text-quality-checklist.md](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/references/text-quality-checklist.md) / md | 文字和格式质量检查参考 | E / static-scan |
| [scripts/annotate_docx.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/annotate_docx.py) / py | 调用 officecli 插入 Word 批注 | E / static-scan |
| [scripts/check_text_quality.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/check_text_quality.py) / py | 文本质量规则扫描及 Word 文本读取 | E / static-scan |
| [scripts/detect_contract_type.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/detect_contract_type.py) / py | 合同类型关键词识别 | E / static-scan |
| [scripts/parse_contract.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/parse_contract.py) / py | 合同文件文本和段落提取 | E / static-scan |
| [scripts/validate.py](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/scripts/validate.py) / py | Word 批注输出自检 | E / static-scan |

许可事实证据：[entry](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/SKILL.md)，blob `b1e3ff93439c32bcc142a241ddf400b22e13ede1`；[documentation](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/README.md)，blob `ff190f543bc43ec46a066f421f844f90b505b58b`；[license](https://github.com/NOMOREKKK/contract-review-skill/blob/f73f92b6341ef4e9f1765434bf348b1acb4fb1d3/LICENSE)，blob `1c3ef4997530ff41a93fb627c8f6d31d85d7a2cd`。NOTICE 缺失结论来自固定提交完整递归树，非只请求根文件后推断。

# discovery-contract-review-zh：固定版本材料清单

预审日期：2026-10-16；状态：**未批准托管、未专业复核、未入库**。中国大陆法域仅沿用来源声明；法规时效保持 `not-checked / null`。

- 原仓库：https://github.com/ThomasLiu/contract-review-zh
- 固定 Commit：`b8382b59d2ba3157125a779a0abf251ec0c29717`（[入口](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/SKILL.md)）
- 固定 Tree：`7554f16fc5e5e7b5abe1720e559193b283d7cf57`；文件数：13。
- 独立逐文件清单：[discovery-contract-review-zh.json](../../data/reviews/manifests/discovery-contract-review-zh.json)，包含**每个文件**的路径、blob、mode、作用、阅读深度及四类拟议决策。
- [交接记录](../../data/reviews/p1-handoff.json) · [阅读方法与限制](README.md) · [专业复核待办](P1_LEGAL_REVIEW_HANDOFF.md#discovery-contract-review-zh)。

## 许可与拟托管范围

根 LICENSE 是 Apache-2.0 完整标准文本；README 声明相同许可。固定树无 NOTICE、无单独贡献者许可。LICENSE 附录仍为 `Copyright [yyyy] [name of copyright owner]`，不能用作具体权利人的版权声明。需确认发布者/作者、贡献者提供权及现有文件版权标记；未发现 NOTICE 只说明该版本树中没有该文件，不免除未来新增适用 NOTICE 的义务。

拟提交用途审核的 4 文件：SKILL.md、README.md、LICENSE、docs/how-it-works.md。README 与入口承认基于 70 篇第三方笔记，核心工作流本身也须核查是否含受保护表达，`eligible-for-scope-review` 不保证独立原创。4 个 references 和 docs/examples.md 共 5 文件标 `requires-authorization`：笔记汇编有作者/标题/链接和抓取说明；风险规则、法条摘编、案例及示例来源交织，未获逐项授权。不能从 Apache 根许可推定笔记作者、案例当事人、模板提供者均已授权。

Apache-2.0 第 4 节要求提供许可副本、在修改文件显著标记改动、保留适用版权/专利/商标/署名声明，存在适用 NOTICE 时保留相关内容；商标授权不自动附带。若未来复制混合来源资料，要分别确认法条原文、解说/编排、案例/合同片段和平台内容的权利范围。CHANGELOG、贡献指南、.gitignore、evals/evals.json 本轮排除；README 自称用例来自真实场景，未核实权属/脱敏，不能沿用为 LexRouter 测评集。

## 依赖与安装问题

| 依赖 | 必需性与证据 | 未解决问题 / 角色 |
| --- | --- | --- |
| Claude Code / Claude.ai | README 安装说明和入口的 Read 工具，引用 references 相对路径 | 不属于纯文本跨宿主兼容证明；权限/上下文和包结构须验证 / 工程维护者 |
| 文件读取与格式转换 | PDF pages、Word 转换、图像识别由宿主工具承担 | README 自动转换声称未经运行验证；DOC/DOCX/PDF 支持及 OCR 准确率待定 / 工程维护者 |
| references 检查表、风险规则、法条材料 | 入口按需加载；核心审查依赖检查规则 | 当前均需补授权，四文件核心不能声称可独立提供完整功能 / 维护者、许可人员 |
| lawyer-due-diligence / humanizer-zh / deep-research | 入口联用段明示非必需 | 不包含在范围、不继承本项目授权 / 维护者 |
| opencli rednote adapter、平台笔记和案例公示服务 | source-notes-summary 来源声明，用于上游采集，不是本轮安装前提 | 抓取/复制/再分发权与用户内容权利须分别核对，未访问平台重抓 / 许可人员 |

README 声称 Claude.ai 只上传 SKILL.md 可自动读取子目录，这不证明 references 已打包或可访问；后续需以获授权包实际验证。无 Python 应用脚本或依赖锁文件，不因本仓库是 Python 校验项目就给其虚构 Python 运行要求。

## 重复度、补充授权与不能确认事项

与一般 contract-review 共同包含立场/事实识别、风险分级、法条和修改建议，不能按输出模式拆分计数。但本候选专注委托律师合同、风险代理收费、委托解除和退费，存在可提交专业复核的独立用途；尚无测评证据证明效果更优。由 Human Maintainer 决定是否保留此专项。

需要核实笔记作者和案例/模板权利、上游作者在规则和示例中使用材料的范围、贡献者链与版权主体。必要时取得覆盖指定文件/版本/用途的书面授权；证据不足可排除资料并重新审计功能范围，不以模型重写代替许可。法律人员重点核对 30% 风险代理比例声称、收费新旧文件及地方规则、任意解除与退费的适用前提、主体瑕疵与合同效力是否被过度简化。未完成任何法规现行性确认。

## 文件证据索引

以下表格列出非知识库文件；每条链接均固定版本，完整 blob SHA 和逐件决定以 JSON 清单为准。`E`=eligible-for-scope-review，`R`=requires-authorization，`X`=exclude-from-hosting，`U`=unverified。E 仅允许提交用途授权审核。

| 原路径 / 类型 | 作用 | 决策 / 阅读 |
| --- | --- | --- |
| [.gitignore](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/.gitignore) / text | 开发排除规则 | X / static-scan |
| [CHANGELOG.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/CHANGELOG.md) / md | 上游版本变更说明 | X / static-scan |
| [LICENSE](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE) / text | 项目根许可及版权条件证据 | E / read |
| [README.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/README.md) / md | 安装、能力、限制和来源声明 | E / read |
| [SKILL.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/SKILL.md) / md | 宿主触发条件、法律任务与工作流入口 | E / read |
| [docs/contributing.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/docs/contributing.md) / md | 上游贡献流程 | X / static-scan |
| [docs/examples.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/docs/examples.md) / md | 上游合同审查报告示例 | R / static-scan |
| [docs/how-it-works.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/docs/how-it-works.md) / md | 上游审查机制说明 | E / static-scan |
| [evals/evals.json](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/evals/evals.json) / json | 来源自称的三个真实场景用例，未核实脱敏和权属 | X / static-scan |
| [references/checklist.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/references/checklist.md) / md | 委托律师合同七维检查规则 | R / static-scan |
| [references/law-references.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/references/law-references.md) / md | 委托合同相关法条摘编和评论 | R / static-scan |
| [references/risk-clauses.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/references/risk-clauses.md) / md | 风险条款示例及修改建议 | R / static-scan |
| [references/source-notes-summary.md](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/references/source-notes-summary.md) / md | 第三方平台笔记汇编及来源链接 | R / static-scan |

许可事实证据：[entry](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/SKILL.md)，blob `bd7a4395c3104eb3f5fc2c5cbf8ae7568b56784d`；[documentation](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/README.md)，blob `57b2f9f6d3fc9207433db6d588977c6486382066`；[license](https://github.com/ThomasLiu/contract-review-zh/blob/b8382b59d2ba3157125a779a0abf251ec0c29717/LICENSE)，blob `d645695673349e3947e8e5ae42332d0ac3164cd7`。NOTICE 缺失结论来自固定提交完整递归树，非只请求根文件后推断。

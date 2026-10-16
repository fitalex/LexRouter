# discovery-china-legal-counsel：固定版本材料清单

预审日期：2026-10-16；状态：**未批准托管、未专业复核、未入库**。中国大陆法域仅沿用来源声明；法规时效保持 `not-checked / null`。

- 原仓库：https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill
- 固定 Commit：`73ff53a857ffbdd91296bf41ed5bcc1294bc2042`（[入口](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md)）
- 固定 Tree：`af1ea322f77f38cdd071272c673dcfe5f4c08106`；文件数：2339。
- 独立逐文件清单：[discovery-china-legal-counsel.json](../../data/reviews/manifests/discovery-china-legal-counsel.json)，包含**每个文件**的路径、blob、mode、作用、阅读深度及四类拟议决策。
- [交接记录](../../data/reviews/p1-handoff.json) · [阅读方法与限制](README.md) · [专业复核待办](P1_LEGAL_REVIEW_HANDOFF.md#discovery-china-legal-counsel)。

## 许可与拟托管范围

根 LICENSE 为 MIT，版权 `2026 Suze`；README 声明 MIT。固定树未见 NOTICE 或其他名为 LICENSE 的子许可文件。发布仓库账号与版权署名不同，尚未验证其关系与贡献者授权链。MIT 的软件/关联文档用语不能自动覆盖 2316 个知识库材料、作者业务背景或宣传图像。

拟提交用途审核的 19 文件：根入口、README、LICENSE、agents/openai.yaml、9 个通用 references 和 6 个 Python 脚本。它们只是可分离组件的审核范围，未经安装/运行或完整包批准。`references/user-business-context.md`、两张宣传图像、.gitignore 和全部 2316 个 knowledge-base 文件（合计 2320）明确 `exclude-from-hosting`。知识库按目录/类型区分为注册表、原始网页/PDF及元数据、清洗 Markdown/JSON、按条切片/索引、评测材料；每个实际路径和哈希均在独立 JSON，而非用目录通配符代替文件决策。

知识库只核对完整树，未逐件阅读全文，也未推定抓取说明可靠。法律规范原文、网页页面元素、编辑解说、汇编/数据库组织、案例/合同模板、清洗和切片产物的权利须分别确认。即使文本来自官方网页，也不能据此将整份下载页面或数据库输出宣布为 MIT。知识库更新日志/抓取时间和文件名年份不构成法规有效性证据。若 P1 希望扩大范围，须另做逐材料来源与权利审计，取得所需授权并单独提交，不能解除本轮排除。

## 依赖与安装问题

| 依赖 | 必需性与证据 | 未解决问题 / 角色 |
| --- | --- | --- |
| Codex 宿主及本地文件能力 | README 安装 `~/.codex/skills/china-legal-counsel`；agents 配置 | 宿主加载、上下文和配置兼容未经运行验证 / 工程维护者 |
| Python 3 / 标准库 | 6 脚本静态导入，部分使用现代类型语法；无锁定 Python 小版本 | 最低可用版本及系统行为需后续锁定，不能声称任何 Python 3 都可用 / 工程维护者 |
| 本地 knowledge-base 与 registry | SKILL.md、source-registry.md；6 脚本默认相对脚本根定位，提供 `--kb` | 入口仍有 `/Users/suze/.codex/skills/china-legal-counsel/knowledge-base` 绝对路径；跨机器适配待做 / 工程维护者 |
| curl、urllib、联网访问 | fetch_official_sources.py | curl 回退含特定主机 TLS 放宽逻辑；上线前另行安全/工程审核，不执行或推荐该回退 / 工程维护者 |
| pdftotext | normalize_legal_doc.py 的 PDF 分支 | 系统二进制及其许可未随 MIT 确认；非 PDF 分支可不使用 / 工程维护者 |
| 官方法规/案例网站 | source-registry.md 列人大、政府、法院、网信、市场监管、知识产权等 | 访问条件/网页权利及现行性分别核实 / 许可人员、法律人员 |
| 已授权商业数据库、律所文章、内部模板及用户事实 | README 来源原则和入口 Source Priority | 可选补充；本地订阅不当然赋予再分发/公开测评权 / Human Maintainer |

19 个组件在材料层面可单独讨论分发，但未附知识库意味着检索、抓取注册、引用核验并不完整。若外供独立组件，后续 PR 需明确输入 KB 接口、空库失败行为、相对路径适配和适用声明；本轮不改写上游，也不宣称运行成立。verify_citations.py 检查引用字符串是否存在，不能证明来源权威、现行性或结论支持关系。

## 补充授权与不能确认事项

Human Maintainer/许可人员核对 Suze 的权利与发布授权、贡献者来源和拟用的复制/改编/再分发/运行/测评/商用范围；需要外部数据库、文章或知识库时另取具体授权。作者品牌和业务背景本轮不使用。没有验证知识库 24 份原文、2189 切片等自述规模或法律正确性，也未核对所有外部链接可用性。

专业复核须覆盖合同、公司治理、广告、数据/AI、知识产权、劳动规则及引用支持性，高风险数据出境、并购、刑事/监管事项必须人工决定。知识库排除不会使这些风险自动消失。

## 文件证据索引

以下表格列出非知识库文件；每条链接均固定版本，完整 blob SHA 和逐件决定以 JSON 清单为准。`E`=eligible-for-scope-review，`R`=requires-authorization，`X`=exclude-from-hosting，`U`=unverified。E 仅允许提交用途授权审核。

| 原路径 / 类型 | 作用 | 决策 / 阅读 |
| --- | --- | --- |
| [.gitignore](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/.gitignore) / text | 开发排除规则 | X / static-scan |
| [LICENSE](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE) / text | 项目根许可及版权条件证据 | E / read |
| [README.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/README.md) / md | 安装、能力、限制和来源声明 | E / read |
| [SKILL.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md) / md | 宿主触发条件、法律任务与工作流入口 | E / read |
| [agents/openai.yaml](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/agents/openai.yaml) / yaml | Codex 展示名称和调用配置 | E / static-scan |
| [assets/poster.png](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/assets/poster.png) / png | 作者宣传图像；未解析二进制 | X / not-read |
| [assets/qulv/qulv-ai-business-poster-readme.png](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/assets/qulv/qulv-ai-business-poster-readme.png) / png | 作者宣传图像；未解析二进制 | X / not-read |
| [references/citation-verification.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/citation-verification.md) / md | 引用支持性检查流程 | E / static-scan |
| [references/compliance-check-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/compliance-check-playbook.md) / md | AI、数据、广告和劳动等合规检查流程 | E / static-scan |
| [references/contract-drafting-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/contract-drafting-playbook.md) / md | 合同起草输入和条款流程 | E / static-scan |
| [references/contract-review-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/contract-review-playbook.md) / md | 合同审阅与修改流程 | E / static-scan |
| [references/eval-plan.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/eval-plan.md) / md | 上游测评任务和评分计划，非 LexRouter 测评 | E / static-scan |
| [references/legal-consultation-playbook.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/legal-consultation-playbook.md) / md | 事实拆解、法律研究与输出流程 | E / static-scan |
| [references/output-schemas.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/output-schemas.md) / md | 各法律任务输出结构 | E / static-scan |
| [references/risk-and-escalation.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/risk-and-escalation.md) / md | 风险分级和人工升级边界 | E / static-scan |
| [references/source-registry.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/source-registry.md) / md | 信息源优先级与本机知识库位置 | E / static-scan |
| [references/user-business-context.md](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/references/user-business-context.md) / md | 作者业务背景与本地场景偏好 | X / static-scan |
| [scripts/chunk_legal_doc.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/chunk_legal_doc.py) / py | 法规、案例和合同文档分片 | E / static-scan |
| [scripts/fetch_official_sources.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/fetch_official_sources.py) / py | 依注册表抓取官方网页或文件 | E / static-scan |
| [scripts/ingest_source_registry.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/ingest_source_registry.py) / py | 读取简化 YAML 注册表 | E / static-scan |
| [scripts/kb_search.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/kb_search.py) / py | 本地片段词匹配检索 | E / static-scan |
| [scripts/normalize_legal_doc.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/normalize_legal_doc.py) / py | 网页或 PDF 文本清洗 | E / static-scan |
| [scripts/verify_citations.py](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/scripts/verify_citations.py) / py | 引用字符串在本地知识库中的存在检查 | E / static-scan |

许可事实证据：[entry](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/SKILL.md)，blob `7cc17878ab5bca101ec178dd97e682134b0fd0eb`；[documentation](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/README.md)，blob `a7cfca9e87278ee5ab789a53d55b462d89b862a0`；[license](https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill/blob/73ff53a857ffbdd91296bf41ed5bcc1294bc2042/LICENSE)，blob `135c200182eb6e3d75ca3ef618ab7af43e6d7e7e`。NOTICE 缺失结论来自固定提交完整递归树，非只请求根文件后推断。

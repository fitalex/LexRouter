# Human Maintainer 操作指南

你负责法律专业判断和最终项目决定。Codex 负责创建材料、解释字段、计算摘要、同步记录和工程检查。**你无须编辑 JSON、理解 Python 或运行校验程序。当前三个样本没有任何专业意见或签署。**

## 一次性启用本人账号

告诉 Codex：“为我的公开 GitHub login 准备审核角色配置 PR，由我承担 Legal Reviewer、Rights Reviewer、Engineering Reviewer 和 Human Maintainer。”可按实际需要另指派角色，不要求多人。

Codex 只准备 `data/reviews/reviewers.json` 的 login→角色变更。你核实账号归属、专业能力、受控资质及权限后，审阅并自行合并该配置 PR。当前白名单为空；同步只信任已进入 main 的政策，工作分支不能自授权。建议 main 启用所需检查及人工合并保护；工具不能替代仓库管理员治理。

真实身份、资质证明和敏感签署资料留在你控制的位置，公开只用公开账号和 `controlled://reviewer/credential-index` 一类不透明索引。你核实实际材料及访问授权；软件不读取私有材料，也不认证律师资格。

## 每次专业复核

1. 在[工作包列表](README.md#三个真实待核样本)打开 packet.md，核对对象、commit、文件、法域、场景和排除范围。不正确时让 Codex 新建 Review，不直接改已固定清单。
2. 阅读 evidence.md 的固定来源、matrix.md 的 C01–C10 及专项问题。官方入口只是检索线索，本人须核实具体文本版本、规范层级、生效/废止/过渡及事实时间。只读争议材料不授予复制或运行许可。
3. 请 Codex 将本轮分配给你的公开 login，提交人工复核。状态进入 in-review，不产生专业决定。
4. 在 GitHub 打开本轮 workbook.md，点击铅笔，逐项填写并提交到本轮 PR 分支。保留 `## C01` 等标题和字段名，填写冒号后内容，可换行续写；多项引用用英文分号分隔。未核保持 pending。只写允许公开的摘要，禁止上传卷宗、证件、签名图片、私信和第三方全文。
5. 填写 signature、maintenance 区，让 Codex 检查缺项并提供当前 **Binding-SHA256 和 Policy-Base**，确认对应你实际看过的范围和工作表。任何意见或前序决定改变都须重新计算摘要。
6. 你本人在 PR 的 **Files changed → Review changes → Comment → Submit review** 提交下面六行，替换为真实值。普通 PR/Issue 对话评论不符合签署格式，不要让 AI/机器人代提交。GitHub 不允许作者批准自己的 PR，因此使用 Comment Review 即可；专用内容表达你的决定，不依赖绿色 Approved 标签。

```text
LexRouter-Review: RV-20261017-contract-review
Role: professional_review
Decision: approved-scope
Binding-SHA256: <Codex 提供、经你核对的 64 位摘要>
Policy-Base: <该 PR main 基准的完整 commit>
Reason: <你独立判断的依据、适用范围和限制>
```

这是专业通过的**语法示例，不是当前决定**。补正用 `needs-changes`，不通过用 `rejected`，在逐项 finding、required_changes、limitations 中记录实际理由。不得照抄合成测试结论。

7. 将你本人刚提交的 Review 事件链接交给 Codex：`https://github.com/fitalex/LexRouter/pull/号码#pullrequestreview-事件ID`。Codex 在线核对 User、已授权角色、写权限、当前 PR head 和精确摘要，再同步结构化记录及意见快照。事件提交后、同步前 head 若变化，须核对并重新签署；同步记录提交后，历史核验使用原签署 head、政策和意见快照。

## 字段填写参考

| 工作表字段 | 你应填写的内容 |
| --- | --- |
| source_locator / legal_issue | 实际规则位置和法律问题；已有文本只是准备线索 |
| fact_context | 时间、主体、行业、必要事实和缺失信息；使用允许公开的合成/脱敏摘要 |
| authority_refs | 已核验官方条文/案例链接或受控版本索引，不能只填门户入口 |
| legal_effective_period / transitional_rule | 生效、修订、废止、替代及过渡/溯及规则；无过渡也须说明核对依据 |
| applicability_reasoning / finding | 事实→适用版本→推理→专业结论及依据 |
| risk_level | unassessed、low、medium、high、critical；说明实际风险和人工升级界限 |
| required_changes / limitations | 待修正内容及使用限制；通过时不能有未完成补正。缩小文件范围须另建 Review |
| evidence_refs | 官方版本、脱敏核查输出或受控证据索引，多项用英文分号 |
| check_status | pending 未核；pass 通过；needs-changes 补正；fail 不通过；not-applicable 不适用（仍须理由和证据） |
| signature.credential_evidence_ref | 经维护者核实的资质/身份索引，不是私有文件路径或证件正文 |
| signature.conflict_declaration | 本人的独立性、利益冲突声明和处置 |
| signature.regulatory_as_of | 本人实际核对法规适用的 YYYY-MM-DD；不能用抓取日、提交日或模型日期代替 |
| maintenance.next_review_date / risk_level | 人工指定下次复核日期（可空）和总体风险；status 显示到期，由维护者安排新 Review |

专业通过要求每项 pass 或有理由/证据的 not-applicable、完整事实/推理/时效/过渡/限制/证据，无未完成补正。软件检查完整性，不替你判断法律正确性。补正后请本人再次判断：Codex 重新 start，你用新 Review 事件签署；旧意见不覆盖。

## 独立授权、工程和最终决定

前三轴可并行；专业通过不代替授权。你填写工作表对应区，再分别让 Codex 提供最新摘要，本人逐个提交**独立事件**；每次同步会改变摘要，不能一次事件承担两个角色。

| Role / Decision | 需核对的内容 |
| --- | --- |
| rights_review / approved-scope、needs-changes、rejected | A：授权主体/贡献者链、精确托管范围、署名与 NOTICE；B：独立需求、原创设计、代码/依赖来源、合成测试；C：独立索引描述、不复制全文、元数据/去重；逐格填公开/受控证据链接 |
| engineering_review / passed、needs-changes、rejected | metadata-schema、dedup、engineering-checks，填写对应校验和 CI 链接 |
| admission_decision / admitted、declined、suspended | scope-and-purpose：维护者对精确范围和用途的独立决定。前三轴都通过才可 admitted；正式文件仍经单独入库 PR 和人工合并 |

同一人可分别作法律决定与最终决定，角色、时间和依据分别保存。新角色可在 signature 区改填自己的受控资质索引，已签法律字段和快照不能改。终局专业意见变动、来源或范围变化须新 Review。

可信重大风险使用 admission_decision / suspended，同时填写 suspension.affected_scope（精确文件名，用英文分号分隔）和 reason；维护者执行暂停复制、分发等实际处置。归档后须新建 risk-reassessment 记录，不删除旧证据；恢复须新证据、复核和独立 PR。

### 已签证据与后续填写

已签署终局决定的工作表区必须和当前签署记录一致：专业 approved-scope/rejected 保护逐项法律判断及 maintenance；权利 approved-scope/rejected 保护 rights_review；工程 passed/rejected 保护 engineering_review；最终 admitted/declined/suspended 保护 admission_decision，suspended 还保护受影响文件和暂停原因。普通编辑不会更新旧签名，不一致时 validate 和 archive 都拒绝；重复同步旧事件也不能豁免。

尚未签署的维度可以继续独立填写。共用 signature 区用于下一位签署人，可更新其身份/资质索引，不改写旧事件中的签署身份。needs-changes 仍可补正；专业补正后重新 start 再本人签署。权利、工程或最终决定的同版本/同范围证据确需修订时，先填写拟修订内容，再由该角色本人提交新摘要绑定的新有效 Review 事件，由 Codex 同步；在该事件被核验/导入前，当前工作表暂不与旧签署一致，不能归档。新事件只允许更新该角色自己的证据，不能替其他角色接受改动。专业终局修改、版本/范围扩展，以及已入库后的权利/工程变化仍需新 Review。

### 归档门槛

- **专业通过：** rights_review、engineering_review 和 admission_decision 都必须已经本人签署终局决定，工作表与所有签署一致才可归档。pending、not-admitted、needs-changes 均未完成；只有专业通过不够。
- **专业拒绝：** 可独立作为拒绝终局归档，无须继续完成其他尚未开展的维度；已有签署证据仍须一致。
- 最终 admitted、declined、suspended 可以形成各自终局记录；后两者不表示批准入库。专业通过时，即使维护者已经 declined/suspended，其他必要维度仍须完成签署才能归档。

请 Codex 在满足上述条件后归档。归档条件不满足或正常写入出错时，原记录和历史保留，不留下半份归档；已归档后重复执行也会先校验证据，不能以旧归档掩盖工作表改动。新版本、法规/许可/范围变化、风险或期限到达时，告诉 Codex 触发类型和前次 Review，生成新 ID 的全新待核工作包。

## 当前人工待办

确认账号角色及受控身份/资质证据；确定实际场景；本人逐项核查三个样本的 C01–C10、CR/ZH/CN；核清权利、依赖和范围；签署专业意见及独立各轴决定；设置复核期限；审查后续正式入库 PR。本次工程交付未代办这些事项。

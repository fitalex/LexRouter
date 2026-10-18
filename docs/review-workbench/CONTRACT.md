# 工程契约与 CLI

## 文件和摘要

[review-record.schema.json](../../schemas/review-record.schema.json) 是独立闭合的 Draft 2020-12 契约，不改变正式八字段。每轮 `data/reviews/cases/<Review ID>/` 包含：

| 文件 | 作用 |
| --- | --- |
| subject.json / inventory.json / templates.json | 固定来源元数据、完整 path/blob/排除清单、去重问题快照；不含第三方全文 |
| record.json | 核心字段、法律判断、四轴、签署、状态历史、风险/期限及归档标记 |
| packet.md / matrix.md / evidence.md | 自动工作包、问题矩阵、固定链接及逐文件范围 |
| workbook.md | 人工意见和角色决定证据区；prepare 永不覆盖 |
| generated.json | 自动文件的已知摘要，人工修改自动区后 prepare 报冲突 |
| history/<序号>.json | 每个本人事件的 before/after、原工作表和核验定位 |
| archive.json | 签署终局 record+workbook 的原始版本，保留不覆盖 |

SHA-256 采用 UTF-8 JSON 的 `sort_keys=True, ensure_ascii=False, separators=(',', ':')` 规范化，Git commit/blob 仍为 SHA-1。**source_snapshot_sha256 绑定来源元数据描述，不声称下载/逐字节散列上游全文**；实际内容版本由完整 commit 和逐文件 Git blob 绑定。scope_manifest_sha256 绑定完整清单，review_scope 只列显式拟核文件。P0 原清单仍由既有 validator 复原固定 Git tree。

旧 manifest/模板不可原地覆盖；新版本另立文件及新 Review。每轮快照保存旧版，CI 与 PR base 比较固定输入、历史前缀、旧签署快照和归档，防止删除/覆盖。Git/摘要提供可追溯性，不是防管理员篡改的独立公证系统。

## 新 Skill 输入（合成示例）

工程人员准备公开描述和文件清单，无须改核心程序；维护者无需手写这些 JSON。

```json
{
  "subject_id": "synthetic-new-skill",
  "subject_type": "skill",
  "source_url": "https://github.com/example/legal-skill/blob/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/SKILL.md",
  "source_revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "scope_manifest_ref": "data/reviews/manifests/synthetic-v1.json",
  "templates": ["data/reviews/templates/common-v1.json"],
  "jurisdiction": "CN-Mainland",
  "track": "external-reference",
  "review_scope": ["SKILL.md"],
  "excluded_scope": ["清单其余文件全部排除"],
  "public_summary_only": true,
  "known_issues": ["合成待核问题，不是真实结论"]
}
```

除 known_issues 外上列字段必填；可选 baseline_refs 提供既有仓库证据。非 GitHub 来源可配置 source_file_url_template，例如 `https://gitlab.example.invalid/skill/-/blob/{revision}/{path}`；必须包含固定版本和文件路径占位符，文件名自动 URL 编码。subject_type 为 candidate、skill 或 original-opportunity；track 为三轨机器值。public_summary_only 是准备人声明，不是隐私认证。

manifest 至少含 revision 与 files，每项有显式 path、完整 blob_sha、decision。只有 eligible-for-scope-review 文件能被选中；扩大范围先准备新的有依据清单再新建 Review。原 P0 清单的 mode、type、role、purpose、basis 等事实不改。C 轨 eligible 表示提交其索引用途核查，不授予复制全文权；B 轨必须有独立原创 ID、来源和证据，不将第三方候选改名消除阻塞。

## 模板扩充

模板格式为 template_id、version、source_ref、checks。每项有 check_id、issue_key、legal_issue、source_locator、authority_hints。通用模板复用 P0-05 C01–C10；CR/ZH/CN 从既有自写交接导入为初始实例。源定位、法规线索与人工核实后的 authority_refs 分离。

对象可加载多个专项。相同 issue_key/定义只计一次；定义冲突或 check_id 指向不同 issue_key 时拒绝合并，由人统一问题。新版本另建模板文件。legal-research、corporate-compliance、corporate-ma、civil-commercial-litigation、criminal-administrative 等均可按相同格式扩展，本次不填造全部业务细则。

## CLI

从仓库根使用 Python 3.11+ 和原 requirements.txt；工程人员执行。初始记录、全部合成测试可离线运行；真实签署核验使用只读 `gh api` 和 GH_TOKEN。

```sh
python scripts/review_workbench.py --help
python scripts/review_workbench.py init --help
# 对于尚无 Review 的新对象：
python scripts/review_workbench.py init --subject data/reviews/subjects/NEW-SKILL.json
# 已存在的实际样本可重复准备/查看，不会覆盖人工意见：
python scripts/review_workbench.py prepare RV-20261017-contract-review
python scripts/review_workbench.py status --as-of 2026-10-17
python scripts/review_workbench.py validate --base-ref origin/main
# 人工指定的定期复核示例（执行会新增未审记录）：
python scripts/review_workbench.py init --subject data/reviews/subjects/discovery-contract-review.json --trigger scheduled-review --parent RV-20261017-contract-review
```

init 自动 prepare 为 evidence-ready；ID 默认 UTC 日期+随机数。重复 ID 拒绝覆盖，同对象后续轮必须 parent；有有效专业批准时关联有效记录。所有新检查和签署重置，不继承通过。七类触发：initial-intake、source-update、regulatory-change、license-change、scope-change、risk-reassessment、scheduled-review；后六种必须 parent。期限由维护者指定，status 报到期；不建设自动法规监控。

```sh
# 替换实际公开 login 和提交定位，仅分配/提交，不授予资格或批准：
python scripts/review_workbench.py start RV-20261017-contract-review --reviewer PUBLIC-LOGIN --reason '材料已准备，提交本人判断' --source https://github.com/fitalex/LexRouter/pull/NUMBER
# 本人填写并提交 workbook 后计算精确意见/范围/前序决定摘要：
python scripts/review_workbench.py digest RV-20261017-contract-review
# 本人按维护者指南提交六行 GitHub Review 后：
python scripts/review_workbench.py sync RV-20261017-contract-review --event-url https://github.com/fitalex/LexRouter/pull/NUMBER#pullrequestreview-ID
python scripts/review_workbench.py validate --online --base-ref origin/main
# 本轮其他轴决定完成，再保留签署原版；归档不意味着入库：
python scripts/review_workbench.py archive RV-20261017-contract-review
```

NUMBER、ID、PUBLIC-LOGIN 是待替换占位，不可给真实样本伪造事件。全局 `--root PATH` 放子命令前，用于隔离仓库/合成测试。

```sh
# 新来源/清单另立路径后，新建全新待核记录：
python scripts/review_workbench.py init --subject data/reviews/subjects/NEW-VERSION.json --trigger source-update --parent OLD-REVIEW-ID
python scripts/review_workbench.py diff OLD-REVIEW-ID NEW-REVIEW-ID
python scripts/review_workbench.py diff OLD-REVIEW-ID NEW-REVIEW-ID --authority 民法典
```

diff 比较 path/blob、增减范围；来源变更无法从散文定位证明无影响时保守列全部。法规查询匹配原 authority_refs 和问题/线索，无命中也保守列全部；固定保持 pending-professional-confirmation，不把字符串检索当成法律影响判断。未受影响的旧证据只返回参考索引，不复制旧结论。

## 状态、判断与签署

法律字段覆盖问题/事实/依据、时效/过渡、适用推理、结论、风险、补正、限制和证据。专业通过须每项 pass 或有理由/证据的 not-applicable，事实/推理/时间分析/限制齐备，无未完成 required_changes；pass 需核实 authority_refs；实际 regulatory_as_of 不可晚于本人复核时间。高风险不自动等于法律错误，由本人判断并控制；程序不能判断意见法律正确性。

needs-changes 保留合法补正路径：专业补正后必须再次 start、本人再次签署；权利/工程补正后通过本角色的新有效事件重签。approved-scope/rejected 的法律判断终局修改须新 Review。其他维度分别填写/签署，不能共用一个事件。先签权利/工程后再 start 专业复核，与先专业后其他角色一样合法；无论顺序如何，状态历史、已签证据与未签维度均独立校验。

签署快照确定性重放并核对当前工作表各角色实际拥有的证据，而不是要求整份工作表永不变化：

| 维度 | 已签署终局状态 | 必须保持一致的当前工作表 |
| --- | --- | --- |
| professional_review | approved-scope、rejected | 全部逐项法律判断及 maintenance（下次复核日期、风险） |
| rights_review | approved-scope、rejected | rights_review 的全部 gate_evidence |
| engineering_review | passed、rejected | engineering_review 的全部 gate_evidence |
| admission_decision | admitted、declined、suspended | admission_decision 的 gate_evidence；suspended 还包括 suspension 的受影响范围与原因 |

共用 signature 是下一位签署人的填写区，不拿它与每位旧签署人强行比较；旧身份/决定/摘要继续由不可改签署快照保留。未签维度可自由填写，needs-changes 可继续补正。终局证据改动必须先有新 Review，或符合现有权限/状态限制的同角色新复核事件。默认 validate 不豁免不一致；sync 先验证新事件本人、角色、权限、精确摘要等，才允许该角色更新自己的工作表区。其他角色的终局证据、专业终局、历史与范围不得借此绕过；apply_event 在正常导入和历史重放中执行同一限制。没有 CLI 豁免参数。重复同步旧事件仍先校验，不产生新决定，也不能解除证据保护。已入库后的权利/工程变化仍须新 Review。

状态、父记录/循环、固定边界、模板及历史保护保持原有规则。重复 prepare 保留工作表，自动区有人工改动则报冲突。

sync 仅读取真实 GitHub Review 事件并核对：仓库/main、ID/URL、已提交且未 dismissed、User 类型（拒绝 Bot）、当前 PR head、精确 Review ID/摘要/Policy-Base/决定/依据、PR 可信 main 基准的角色白名单及当前 write/maintain/admin 权限。Comment Review 可由作者本人提交。普通评论、机器人提交、文本签名字段或合法 JSON 不作可靠签署。

Policy-Base 写在本人事件中，历史验证确认其已进入 main，重查原事件和原 reviewed commit，不要求 PR head 永不变化；原意见、范围和前序决定由绑定摘要及快照重放验证。事件编辑、dismissed 或权限撤销使在线验证失败，维护者须保留历史并另立风险重审。网络/API失败拒绝导入，不降级信任本地文件。

**默认 validate 只证明离线结构/一致性，不认证身份**；真实签署/入库 PR 必须通过 validate --online（CI 已接入）。政策白名单初始为空，配置经单独人工接受；本分支不能自授角色。证据证明公开账号的可追溯操作和已授角色，不证明自然人身份、专业资质、密码未共享或法律正确性；由维护者在受控位置核实。GitHub 的 User 类型本身无法区分本人网页操作与使用同一账号令牌的自动化；AI 被明确禁止创建法律签署事件，若账号被自动化共用或本人操作有疑问，维护者必须以受控签署记录补证，不能仅凭 User 字段认定本人签署。

admission_decision 只在相应轨权利/原创性、专业和工程轴齐备后接受独立 admitted 事件。工程证据覆盖八字段、去重和 CI；既有正式目录校验继续执行。记录审批不复制 Skill、不生成法律日期、不合并 main。重大风险由维护者签署 suspension（精确文件+原因）并执行处置；恢复须新记录和新证据。

archive 必须先校验当前工作表和全部签署证据一致，包括已经归档后的重复调用。专业 rejected 且有签署时，可独立归档拒绝终局。专业 approved-scope 时，rights_review、engineering_review、admission_decision 也须全部已签署终局决定；pending/not-admitted/needs-changes 均不能归档。admitted 继续要求原三轨全部通过门槛；declined/suspended 可以归档为拒绝/暂停的项目决定，但不授予入库资格，也不免除专业通过记录其他维度的完成条件。已归档记录的 validate 也检查该终局门槛。

条件检查均在写入前完成，失败不修改记录/历史。归档 record 和 workbook 完整包及新状态先在私有临时目录准备，再以单文件原子替换提交；如果记录替换发生正常 I/O 异常，移除本轮新建的归档文件，原 record/history 不变。两阶段的写入异常均有故障注入测试。归档后只读，后续变化新建子记录。

这仍不是跨文件持久化事务：进程强制终止/主机故障可能打断两次替换，或保留临时目录；现有 archive/marker 一致性校验会拒绝把不完整状态认作有效归档。此时由工程人员保留并排查，不修改签署历史来“修复”。

## 隐私边界

不导入附件、证件、卷宗、私信、第三方全文，不读取 controlled://。证据只接受无凭据/查询串 HTTPS 或不透明受控索引；拒绝越界/符号链接。验证/同步前作有限敏感模式检查，错误只打印固定说明/字段路径，不打印输入值、响应或 stderr。

模式检查不能识别全部隐私、商业秘密或授权问题；公开前必须按 ANONYMIZATION.md/SECURITY.md 人工审阅 Git diff，不能先提交敏感资料再依赖 CI 消除泄漏。原始身份/案卷材料始终在仓库外受控保存；CI 不处理私有正文。合成测试中的用户/依据/事件全部为虚构工程数据，不得作为真实签署证据。

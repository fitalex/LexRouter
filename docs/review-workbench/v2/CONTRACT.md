# Review Workbench v2 工程契约

Gate 1 新增独立 `format_version: 2`，不迁移三个真实候选，不修改 v1 四轴契约。法律、权利和工程材料由 Codex Astra 整理；只有经验证的本人 GitHub Comment Review 可以生成专业或维护者决定。

## 数据与映射

- `data/reviews/v2/<Review ID>/bundle.json`：固定 subject、上游仓库/commit、完整文件 blob 清单和排除范围、main 已接受的模板及摘要、逐文件/逐检查项矩阵、议题分组、权利证据、时点/过渡、限制和更新要求。机器状态只使用 `not-verified / agent-precheck / ci-verified`，不表示真人批准。
- 同目录 `ledger.json`：事件序号、前序账本摘要、bundle 摘要、GitHub Review ID/URL、原始事件摘要、本人账号、reviewed commit、main 政策快照、短表意见及本条摘要。SHA256 使用排序键的规范 JSON；Git commit/blob 仍为 Git SHA。任何决定都追加，不覆盖旧条目。
- [独立 Schema](../../../schemas/review-record-v2.schema.json)拒绝未知字段；[核心程序](../../../scripts/review_workbench_v2.py)校验完整映射、来源/模板锚点、历史重放和本人授权。C01–C10 及 subject 指定的全部专项项必须保留，分组数量不设硬上限。

短表只绑定机器已经整理的附件，不以短表摘要替代实质核法。全部组均须有明确决定、理由及限制；未实际核法的补正/拒绝意见可用 `not-verified`，通过必须实际日期。通过仍需解决适用事实、时效与过渡、法源/证据缺失以及相应轨的权利门槛。程序验证留证完整性，不能自动判定法律观点、许可证解释或受控材料真实性。

对于总体 `approved-scope` 或 `admitted`，全部文件×检查项映射均检查 `authority_refs`、`evidence_refs`、`facts`、`effective_period`、`transitional_rule` 和 `applicability`。组决定为 `not-applicable` 不豁免这些字段，且其每条矩阵必须提供非空、非待核的 `not_applicable_reason`，结合本条事实及引用说明不适用条件。该字段属于受摘要绑定的附件，由准备者整理、本人审阅；组级一句理由不能覆盖缺证行。完整结构化不适用依据可以被专家采纳，但程序不判断其法律正确性。补正/拒绝路径仍可保留缺证状态，不能转为通过。

## 从本人事件到自动同步

1. `pull_request_review` 的 submitted/edited/dismissed 只触发无权限 signal 工作流，不检出 PR、不使用凭据、不上传可执行产物。
2. `workflow_run` 接收器仅从 default branch 的 `github.workflow_sha` 检出可信程序。通过 GitHub API重新获取 signal run、PR、Review、main 角色和 v2 政策，绝不执行 PR 中脚本或读取通知产物作为授权。
3. 验证同仓库 main PR、`User`、角色、当前写权限、已接受的资质索引、Comment Review、本人 reviewed head、全部附件、历史事件和独立决定。没有身份/事件可信证据即拒绝。普通评论、机器人、工作分支自行添加的角色或工程报告都不能签署。
4. 验证器按每次签署时的实际附件与前序账本重放，重新检查法源/权利/CI及专业先于入库的门槛。已签内容变动须新 Review。对未合并 PR 也追查先前 commit 中的账本，拒绝删除和强推丢历史；分页不完整或历史过长则停止。
5. 用 Git tree/commit API生成只改一个 ledger 的提交，写前再次核对事件、权限、head 和 main；ref 更新 `force:false`，并发更新拒绝。失败时可能留下不可达 Git 对象，不会把失败决定发布到分支。
6. 因 `GITHUB_TOKEN` 写入不自动触发 PR CI，成功写回后显式 dispatch 既有 Validate Skills 工作流；新 head 完成 CI 后，维护者才能作第二个独立事件。同步器不提交 Review，不合并、不复制第三方 Skill、不改变正式目录。

接收器的 `contents:write` 仅用于账本提交，`actions:write` 用于读取通知和显式启动新 head CI，`checks:read`、`pull-requests:read` 用于核验。禁用 checkout 凭据持久化。签署 PR 的可执行输入必须与已接受 main 一致；不能靠修改校验器或添加同名 GitHub Actions job 伪造工程通过。改工程代码的 Gate 1 PR 本身没有真人签署数据，正常接受代码审查及单测。

若 GitHub 未提供唯一 PR 关联、API失败、并发两次决定、签署时 CI尚未完成或事件被修改/撤销，处理器失败且不导入新决定。工程人员排查后可以重跑真实事件的同步；不能修改历史以消除失败。没有从事件推导身份的离线回退。

## 命令与启用

```sh
# 工程人员生成可复制的短表，本人不运行命令/编辑JSON：
python scripts/review_workbench_v2.py form --bundle data/reviews/v2/RV-ID/bundle.json
python scripts/review_workbench_v2.py form --bundle data/reviews/v2/RV-ID/bundle.json --axis admission_decision
# 保留v1验证，同时验证v2；真实事件必须在线核验：
python scripts/review_workbench.py validate --online --base-ref origin/main
python scripts/review_workbench_v2.py validate --online --base-ref origin/main
# 下列入口由可信workflow调用；run ID来自GitHub事件，无须本人复制URL/SHA：
python scripts/review_workbench_v2_sync_run.py --run-id RUN_ID --write
```

Gate 1 合并后工作流才进入可信 default branch。Gate 2另由本人接受真实 `credential_refs`，当前空表故意阻断真实签署；四角色授权仍从已接受的 `reviewers.json` 读取。90日是供验收的可配置工程上限，不是法规有效性声明。

网络结构/身份核验依赖 GitHub，无法提供管理员不可篡改的外部公证或区分“本人网页操作”与“使用本人令牌的自动化”。AI禁止代签；共享账号或受控资质疑问交维护者核实。真实 Review 演练属于 Gate 3，Gate 1 的正反事件全部是合成测试。

## GitHub 接口依据

首次同步前也必须检测编辑：REST Review 用于取得身份、状态和commit，固定只读 GraphQL 查询核对同一 Review 的 `fullDatabaseId`、`lastEditedAt`、commit与所属PR；`lastEditedAt` 非空、字段缺失、节点不符或查询失败均拒绝导入。编辑后须本人提交新的 Comment Review，不能修改原事件来续签。[GitHub PullRequestReview 字段](https://docs.github.com/en/graphql/reference/pulls#pullrequestreview)

`workflow_run` 接收任务使用默认分支工作流；代码、事件及权限必须分别核验，不能把前序任务成功当作授权。[GitHub workflow_run 事件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run)

账本提交后的显式 CI dispatch 避免依赖令牌提交自动触发；工作流需先存在于默认分支。[GitHub 手动/API触发工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

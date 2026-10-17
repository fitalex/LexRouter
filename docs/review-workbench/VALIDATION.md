# LR-P1-02 验证与验收记录

本任务从最新 main `43062c6` 建立独立分支；PR #6 已于执行时合并在该基准中，其扩充数据/校验继续保留。工程功能可复现，三个真实样本只准备材料。没有用真实身份、真实客户案卷、第三方全文或真实签署事件进行测试。

## 合成测试

[测试代码](../../tests/test_review_workbench.py) 使用隔离临时目录、显式虚构 GitHub 用户/事件及 example.invalid/controlled://synthetic 引用；不是实际法律意见或签名。

| 验收测试 | 实际验证的行为 |
| --- | --- |
| T01 新候选 | 新合成 Skill 以描述/清单/模板创建工作包，不改核心代码；亦验证非 GitHub 来源及含空格文件名 |
| T02 版本变化 | 已签合成记录归档后创建 source-update 子记录，原始文件不变，新记录全部未核 |
| T03 法规变化 | regulatory-change + authority 查询定位可能关联项，保持待专业确认，无命中保守扩大核查 |
| T04 专业不通过 | fail、未补正或缺依据不能 approved-scope；needs-changes 后须 start 及本人新事件 |
| T05 授权冲突 | 专业通过但 rights pending 时拒绝 admitted；四轴全部齐备才接受独立最终事件 |
| T06 人工保护 | 重复 prepare 保留多行意见；自动区人工修改报冲突；重复同步不新增决定 |
| T07 范围扩大 | 新文件新 Review 不继承批准；排除文件不能直接进入既有范围 |
| T08 隐私隔离 | 私有/带凭据查询定位、越界/符号链接拒绝；敏感标记错误不回显；不读取私有证据正文 |

其他回归覆盖机器人/未授权角色/不足权限/错误摘要/陈旧或 dismissed 事件、签署快照篡改、父记录循环、模板重复/冲突、三轨实际不同权利门槛、暂停、到期提醒、归档/Git baseline、已入库后的修改阻断、中断孤立快照、重复 JSON 键，以及从三个真实对象固定输入重新创建的 27/4/19 范围与 15/15/16 空白检查项（不把未来生产 Review 数量/状态写死）。

## 本地与 CI 复现

```sh
python scripts/validate_skills.py skills
python scripts/validate_skills.py tests/fixtures/valid
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_candidates.py data/discovery/p1-batch-01.json
python scripts/validate_candidates.py tests/fixtures/candidates/valid.json
python scripts/validate_discovery_batches.py data/discovery/candidates.json data/discovery/p1-batch-01.json
python scripts/validate_p1_readiness.py
python scripts/validate_p1_readiness.py tests/fixtures/p1-readiness/valid.json --candidates tests/fixtures/p1-readiness/candidates.json
python scripts/validate_intake_plan.py
python scripts/validate_intake_plan.py tests/fixtures/intake/valid.json --candidates tests/fixtures/p1-readiness/candidates.json --readiness tests/fixtures/p1-readiness/valid.json
python scripts/validate_p1_handoff.py
python scripts/review_workbench.py validate --online --base-ref origin/main
python -m unittest discover -s tests -v
git diff --check
```

实际结果在 PR 描述记录最终本地测试数量及同一 head 的 Actions 链接。现有测试原为 75 项，本任务新增 24 项。在线校验对初始三条报告 **0 human events**，不能称为真实签署/专业认证通过。CI 保留所有原步骤，增加工作台/不可改历史检查；checkout 完整历史，PR 使用真实 base SHA。真实签署存在时才发起只读 GitHub 证据查询。

已对 main 比较 12 份冻结/审计文件字节：ROADMAP、正式 Schema、收录政策、原候选/readiness、PR #6 批次、intake、handoff、专业交接及三个原 manifest 均不变。内部工作包/指南相对链接也经检查。

## D01–D12 对照

| 标准 | 交付证据与边界 |
| --- | --- |
| D01 / D02 / D11 | 核心无候选 ID/数量分支；通用模板、数据描述、新来源和多业务可配置；合成新对象创建成功 |
| D03 | 三个实际工作包、问题矩阵、原站固定链接和人工区，见入口列表 |
| D04 | 精确意见/版本/范围摘要 + 本人 User/角色/权限/事件核验，初始不伪造真人签署；执业资格和自然人身份仍需维护者受控确认 |
| D05 | 七触发、唯一 ID/parent、固定版本和模板、历史快照/重放、Git baseline、归档、法规关联及到期提醒 |
| D06 | 四轴与各轨门槛分离，独立最终事件；不生成正式 Skill 或自动合并 |
| D07 | 三个初始 professional pending、jurisdiction proposed、无签名/法规日期/入库决定 |
| D08 | T01–T08 均有可执行正反断言，其余回归见测试代码 |
| D09 | 本地原有校验及全部单元测试；远端最终 head 的 Actions 结果由 PR 提供，不以本地结果冒称 CI |
| D10 | 维护者通过 GitHub 编辑 Markdown/本人 Review，Codex 处理描述、配置及同步，无须维护者操作 JSON/Python |
| D12 | P0 审计/路线图/八字段保持冻结；不自动签署、不修改候选历史状态、不合并 main |

## 未完成的人工事项与限制

审核账号/角色尚未配置，专业身份/资质证据未核实；三个样本全部逐项法律复核、授权/原创性或用途确认、依赖验证、各轴签署及正式入库决定仍待执行。复核期限由实际审核人填写，不填造日期。

基础敏感检测不保证识别全部隐私/权利问题，发布前仍需人工审查。摘要/结构合法不代表法律正确或自然人身份认证。测试中的 GitHub API 为显式合成依赖，真实 API 导入路径需在实际本人事件发生后执行在线核验；不能为测试创建虚假真实审批。工具不自动监控法规、运行上游、联系权利人、恢复暂停或执行下架。

本 PR 交付后等待 ChatGPT 审查和 Human Maintainer 验收/合并，禁止自动合并。

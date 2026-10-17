# RV-20261017-contract-review｜法律 Skill 专业复核工作包

- 对象：discovery-contract-review（candidate）
- 轨道提案：curated-hosting
- 固定版本：`f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`
- 触发：initial-intake；前次记录：无
- 拟核法域：CN-Mainland，待专业确认
- 拟核文件：27；排除边界：固定 manifest 中所有未列入 review_scope 的文件（4 项）均排除；只读线索不构成复制许可

## 审核材料和人工填写

- [来源固定链接与范围](evidence.md)
- [通用/专项问题矩阵](matrix.md)
- [人工专业意见区](workbook.md)
- [结构化记录和状态](record.json)
- [维护者操作指南](../../../../docs/review-workbench/MAINTAINER.md)

## 已发现疑点和原始依据

- [既有证据 docs/SKILL_INTAKE_POLICY.md](../../../../docs/SKILL_INTAKE_POLICY.md)
- [既有证据 docs/reviews/P1_LEGAL_REVIEW_HANDOFF.md](../../../../docs/reviews/P1_LEGAL_REVIEW_HANDOFF.md)
- [既有证据 data/reviews/p1-handoff.json](../../../../data/reviews/p1-handoff.json)
- [既有证据 data/discovery/p1-readiness.json](../../../../data/discovery/p1-readiness.json)
- 确认 NOMOREKKK 及贡献者对拟用文档、规则、脚本的授权链；MIT 不覆盖外部服务；跨境贸易术语、法条汇编及二进制模板另行核实。
- 根入口与安装示例不一致；Python 3.10+、Windows officecli 版本/API/许可证、OCR 与检索连接器需单独确认；不执行上游。
- 确认实际适用法域、固定版本及目标使用场景；逐条核对官方现行文本、生效/废止/过渡规则，并留存具名专业复核证据。
- 核对违约金、利息及保证金阈值的适用条件，避免把经验阈值写成普遍强制规则。
- 逐条核验合同分类规则、民法典及司法解释的生效、废止与过渡规定。

## 尚未完成事项

创建时所有 C01–C10 和专项项均待人工核查，资质、利益冲突、法规时效及签署均未确认；实际后续进度见 record.json 和 status。
授权链、依赖、范围/用途待独立审核；八字段元数据、去重和工程检查待执行。当前未专业复核、未获授权批准、未入库。

## 最终决定和签署说明

专业人员填写工作表后，由本人在 GitHub Review 中声明角色、决定、绑定摘要和依据。
同一人可分别担任 Legal Reviewer 和 Human Maintainer，必须使用独立事件。Codex 只同步核验事件，不代签或自动批准。
重大法律或授权风险须记录受影响范围、暂停决定并由维护者执行处置；历史证据不自动删除。

# RV-20261017-china-legal-counsel｜法律 Skill 专业复核工作包

- 对象：discovery-china-legal-counsel（candidate）
- 轨道提案：curated-hosting
- 固定版本：`73ff53a857ffbdd91296bf41ed5bcc1294bc2042`
- 触发：initial-intake；前次记录：无
- 拟核法域：CN-Mainland，待专业确认
- 拟核文件：19；排除边界：固定 manifest 中所有未列入 review_scope 的文件（2320 项）均排除；只读线索不构成复制许可

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
- 确认 Suze 与仓库发布者及贡献者关系；知识库原始/清洗/切片、商业数据库、律所文章、品牌图像和用户背景均不随 MIT 自动授权，本范围全部排除。
- 绝对路径须后续单独适配；Python 脚本默认相对 knowledge-base 并支持 --kb；不含知识库的组件不能声称完整可用。curl/pdftotext 与官方站点访问条件另审。
- fetch_official_sources.py 存在特定主机 curl TLS 放宽回退；上线前另审和修正，当前不运行。引用字符串存在检查不等于法律效力或结论校验。
- 确认实际适用法域、固定版本及目标使用场景；逐条核对官方现行文本、生效/废止/过渡规则，并留存具名专业复核证据。
- 逐项核验合同、广告、数据、劳动及公司治理规则的法域、现行文本与场景适用。
- 抽查知识库来源与引用是否真正支持结论，确认重大事项人工升级边界。

## 尚未完成事项

创建时所有 C01–C10 和专项项均待人工核查，资质、利益冲突、法规时效及签署均未确认；实际后续进度见 record.json 和 status。
授权链、依赖、范围/用途待独立审核；八字段元数据、去重和工程检查待执行。当前未专业复核、未获授权批准、未入库。

## 最终决定和签署说明

专业人员填写工作表后，由本人在 GitHub Review 中声明角色、决定、绑定摘要和依据。
同一人可分别担任 Legal Reviewer 和 Human Maintainer，必须使用独立事件。Codex 只同步核验事件，不代签或自动批准。
重大法律或授权风险须记录受影响范围、暂停决定并由维护者执行处置；历史证据不自动删除。

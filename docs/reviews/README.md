# 精选托管预审与 P1 法律交接

本目录为 LR-P0-05 附加工程交付，按既有[三轨政策](../SKILL_INTAKE_POLICY.md)预审，不改变原候选 readiness。**READY_FOR_REVIEW — HUMAN_APPROVAL_PENDING** 表示工程交接可供审阅，不是托管、专业复核或正式入库批准。

- [contract-review 材料清单与边界](discovery-contract-review.md)
- [contract-review-zh 材料清单与边界](discovery-contract-review-zh.md)
- [china-legal-counsel 材料清单与边界](discovery-china-legal-counsel.md)
- [法律专业复核交接包](P1_LEGAL_REVIEW_HANDOFF.md)
- [结构化记录契约及四类逐文件决策](../../data/reviews/README.md)
- [冻结 P0 验收准备报告](../P0_ACCEPTANCE_REPORT.md)

2026-10-16 核查：从公开原仓库读取固定 commit 的 Git 对象、完整文件树、根 LICENSE/README/入口，以及其余工作流/脚本的结构与来源标记；不检出安装、不导入或执行上游代码。临时只读对象位于仓库外审计工作区，未进入提交。二进制模板和图像未解析，知识库只列树；未检查全部贡献者历史、未向权利人发信、未逐条核实官方法规。原 HEAD 恰与三条固定 revision 相同，未观察到版本差异；不是持续监控结论。后续有实质变化必须保留旧版本、新增差异与重新审计记录。

清单统计为文件（不含目录对象）：31 / 13 / 2339；此前 readiness 的 35 / 16 / 2356 是含目录的递归树项数，口径差异不是来源变化。每个文件均在对应 JSON 有独立判定，无目录通配符替代；长知识库不在 Markdown 重复展开。完整 tree SHA 在结构化交接记录中，离线重建检查完整性。

根 MIT/Apache-2.0 仅提供提交范围审核的线索。对当前项目原创部分的拟用途为：未来经批准的镜像复制、修改适配、公开再分发、宿主运行及技术测评；商用服务、商业数据库输出再分发和品牌使用均须逐项确认。授权审核应列出每种用途及材料版本、权利主体、保留声明、期限/限制。已有开源许可覆盖且授权链充分的部分不强制另取新许可；链条、外部来源或用途不明的部分，Human Maintainer 决定向相关权利人取得澄清或补充书面授权。公开 PR 只记录脱敏定位与结论，不附私人通信或第三方全文。

## 持续复核工作台

LR-P1-02 的 [Review Workbench v1](../review-workbench/README.md) 另建模板、逐轮记录与人工工作表；P0 交接事实及排除边界保持冻结。初始三个实例仅材料就绪，专业/授权/签署/入库均待执行。

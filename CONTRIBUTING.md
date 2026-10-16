# 社区贡献指南

欢迎通过 Issue 提出问题或建议，通过独立分支与 PR 提交贡献。首先阅读 [路线图](ROADMAP.md)、[Agent 规范](AGENTS.md) 和 [脱敏规范](docs/ANONYMIZATION.md)。main 保持稳定，所有实质变更须经审核，由 Human Maintainer 合并；禁止自动合并或强制推送。

## Skills 收录

三轨策略见 [SKILL_INTAKE_POLICY.md](docs/SKILL_INTAKE_POLICY.md)，首批提案及扩充方式见 [P1_SELECTION_PLAN.md](docs/P1_SELECTION_PLAN.md)。A 精选托管须先取得指定材料、版本、复制/再分发与拟用范围授权及法律专业批准；B 原创使用独立标识和需求/设计/测试来源，不得复制、改写或由模型变相复刻受限第三方；C 外部索引只保留固定原链接及原创元数据，不赋予运行、测评、改编、复制或再分发权。三轨都须满足正式法域与法规时效要求才能进入目录。

模式提案写入 `data/intake/p1-proposals.json`，用 Candidate ID 与 readiness 摘要关联原证据；不要重复许可正文或候选审计。原创机会另立 ID，只表示待立项，原候选与阻塞保留。P0 提案不能写成托管/专业/目录批准，也不能声明可复制或再分发；后续真实审批需独立证据和 PR。实际使用前依政策复核来源与许可变化，不擅自联系权利人。

LR-P0-03 的候选质量审计和 P1 准备另见 [P1_READINESS.md](docs/P1_READINESS.md)。新增或变更候选时，应同步准备记录、完整候选快照和证据；执行 `python scripts/validate_p1_readiness.py` 检查完整对应关系。原有 needs-evidence 不得静默升级授权，blocked/rejected 须列明证据、影响、下一步和责任方。ready-for-professional-review 仅允许提交专业复核，正式入库仍需法律专业证据与 Human Maintainer 的独立 PR 批准。

发现阶段请先按 [DISCOVERY_PROTOCOL.md](docs/DISCOVERY_PROTOCOL.md) 向 `data/discovery/candidates.json` 提交来源、版本、核查状态与证据说明，并执行 `python scripts/validate_candidates.py data/discovery/candidates.json`。候选与正式目录使用独立契约；许可缺失或冲突、法域及法规时效未核实均须如实标记，不得把候选直接搬入 `skills/`。候选结构通过不构成正式入库或推荐。

P0-01 不批量收录 Skills，正式目录整合在 P1 开展。后续收录时，每个 Skill 在 `skills/<id>/metadata.json` 提交一个 JSON 对象，按 [SCHEMA.md](docs/SCHEMA.md) 填写唯一标识、名称、描述、原始来源、法域、业务分类、法规时效锚点及运行载体。

应可定位原始作者与版本，描述真实能力与限制；明确核实法域和时效基准，不得编造日期、功能或测评成绩。未知日期的条目应留作待补资料，不进入正式目录。机器校验通过后，仍需人工审核来源、授权、法律专业适用性与信息质量。

第三方 Skills、代码、数据集、法律文本及其他材料须确认各自授权，保留来源、署名及必要的版权和许可证声明，并在 PR 中提供授权依据。未确认授权的第三方内容不得直接复制入库；此时仅提议原始链接，且链接也不自动满足正式收录条件。不得将第三方材料声明为 LexRouter 原创作品或擅自改为 MIT 授权。

## 提交与审核

1. 从最新 main 建立任务分支，保持改动聚焦；重大设计先通过 Issue 讨论并交维护者决策。
2. 使用 Python 3.11+ 创建虚拟环境，执行 `python -m pip install -r requirements.txt`。
3. 执行以下检查并附实际结果：

   ```sh
   python scripts/validate_skills.py skills
   python scripts/validate_candidates.py data/discovery/candidates.json
   python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
   python scripts/validate_intake_plan.py data/intake/p1-proposals.json
   python -m unittest discover -s tests -v
   git diff --check
   ```

4. 使用 PR 模板说明改动、依赖理由、测试、授权及风险。不得将密钥、隐私或 Holdout 内容贴入讨论或日志。
5. 等待自动检查和人工审核；根据意见修订。法律内容须法律专家复核，最终由 Human Maintainer 验收合并。

## 许可证与第三方授权

Human Maintainer 已在 LR-P0-01A 中批准 LexRouter 自主原创代码采用 [MIT License](LICENSE)，版权声明为 `Copyright (c) 2026 fitalex`。提交自主原创代码贡献时，应确认自己有权按 MIT 条款提供该贡献；保留 MIT 要求的版权和许可声明。

此决定不替代或扩大第三方 Skills、代码、数据集、法律文本及其他材料各自的授权，贡献也不自动改变第三方权利。维护者仍须审核第三方授权与许可兼容性，必要声明必须随相关材料保留。直接依赖检查记录见 [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md)；新增或升级依赖时应同步复核，不擅自改变其许可证。

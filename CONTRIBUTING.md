# 社区贡献指南

欢迎通过 Issue 提出问题或建议，通过独立分支与 PR 提交贡献。首先阅读 [路线图](ROADMAP.md)、[Agent 规范](AGENTS.md) 和 [脱敏规范](docs/ANONYMIZATION.md)。main 保持稳定，所有实质变更须经审核，由 Human Maintainer 合并；禁止自动合并或强制推送。

## Skills 收录

P0-01 不批量收录 Skills，正式目录整合在 P1 开展。后续收录时，每个 Skill 在 `skills/<id>/metadata.json` 提交一个 JSON 对象，按 [SCHEMA.md](docs/SCHEMA.md) 填写唯一标识、名称、描述、原始来源、法域、业务分类、法规时效锚点及运行载体。

应可定位原始作者与版本，描述真实能力与限制；明确核实法域和时效基准，不得编造日期、功能或测评成绩。未知日期的条目应留作待补资料，不进入正式目录。机器校验通过后，仍需人工审核来源、授权、法律专业适用性与信息质量。

第三方内容须确认原许可或取得授权，保留来源和署名并在 PR 中提供授权依据。无明确授权时仅提议原始链接，不复制受限全文、代码或材料。无明确授权的链接也不自动满足正式收录条件。

## 提交与审核

1. 从最新 main 建立任务分支，保持改动聚焦；重大设计先通过 Issue 讨论并交维护者决策。
2. 使用 Python 3.11+ 创建虚拟环境，执行 `python -m pip install -r requirements.txt`。
3. 执行以下检查并附实际结果：

   ```sh
   python scripts/validate_skills.py skills
   python -m unittest discover -s tests -v
   git diff --check
   ```

4. 使用 PR 模板说明改动、依赖理由、测试、授权及风险。不得将密钥、隐私或 Holdout 内容贴入讨论或日志。
5. 等待自动检查和人工审核；根据意见修订。法律内容须法律专家复核，最终由 Human Maintainer 验收合并。

## 许可证待决

具体开源许可证尚未人工批准，正式发布前必须解决。公开仓库不等于已授予明确的开源再分发许可，贡献也不自动改变第三方权利。维护者应在发布前确认项目许可、贡献授权及第三方许可兼容性。本阶段不擅自选择 MIT、Apache-2.0 或其他许可证。

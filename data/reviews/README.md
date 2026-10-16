# P1 交接记录与材料清单

[LR-P0-05](../../docs/daily-specs/LR-P0-05.md) 的 [p1-handoff.json](p1-handoff.json) 仅关联现有 A 类提案，不复制完整候选审计。候选事实在 `data/discovery/`，三轨提案在 `data/intake/`；两条摘要绑定完整原记录。现有十候选、七条 blocked、四项原创机会均不改动。

三个独立清单位于 [manifests/](manifests/)，逐文件记录原路径、Git blob SHA、mode、类型、作用、阅读深度和拟议决策；原仓库和固定提交通过 Candidate ID 查阅 readiness。包含整个固定树的文件，含明确排除项；目录由文件路径可复原。不存上游全文、图片、合同、笔记、知识库、执行脚本或许可证全文。

| decision | 准确含义 |
| --- | --- |
| `eligible-for-scope-review` | 有足够当前来源/许可事实提交**具体用途授权审核**；仍须查授权链、专业质量和运行条件，不是复制/托管批准 |
| `requires-authorization` | 须补充权利人授权或许可适用范围解释，不能进入拟复制包 |
| `exclude-from-hosting` | 本轮明确排除，即使未来证明有权使用，也须新 PR 改范围 |
| `unverified` | 当前证据不足，暂不决定是否可纳入 |

阅读深度：`read` 为完整入口/README/LICENSE 只读核查；`static-scan` 为文件标题、结构、导入、外部命令、权利及来源标记的静态检查，不表示逐句审阅；`not-read` 仅核对 Git 树路径/blob/mode。尤其知识库 2316 文件未逐件阅读。根许可证和静态扫描都不是权属保证。

`basis` 是下列证据说明的短键：`root-license-pending-chain` 指固定根许可和尚待确认的贡献者链；`third-party-trade-terms` 指跨境贸易参考中的 Incoterms；`compiled-source-rights` 指预录法规/索引汇编；`notes-and-reference-rights` 指笔记、案例、法条摘编及示例的混合来源；`binary-provenance-unverified` 指未解析模板；`outside-proposed-package` 指开发或测试附属材料；`exclude-data-and-brand-context` 指本轮排除知识库、作者背景和宣传素材。详细证据、补证事项见 [材料预审说明](../../docs/reviews/README.md)。

```sh
python scripts/validate_p1_handoff.py
python -m unittest discover -s tests -v
```

校验复用原 jsonschema、readiness 和 intake 校验，不联网、不运行上游：检查准确覆盖 A 类提案、原版本及摘要、逐文件清单摘要/数量/唯一性和路径安全，并从 mode/path/blob 重建 Git tree SHA，核对既有入口/README/LICENSE blob。Git 哈希只能证明材料身份与清单完整性，不能证明许可范围或法律正确性。状态固定未托管批准、未专业复核、未入库，时效为原未核实状态及 null；不提供批准接口。未来真实批准须另立证据契约与 PR，不能放宽此 P0 快照。

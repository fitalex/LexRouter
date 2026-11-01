# Gate 2 回归测试 CI 补正

Owner：Codex Astra；交叉复核：独立工程审查；最终验收：Human Maintainer。

原本仅保存在 ADAPTATION_TESTS.md 的九项回归现由共用工程分支 `codex/gate2-regression-ci` 中 `tests/test_gate2_adaptation.py` 维护，接入 Validate Skills 的三个候选矩阵任务。候选作为只读数据，测试实现从共用工程检出目录加载；日志分别记录实现 SHA、候选实际 HEAD 和已接受 main，不将测试通过解释为真人签署。

本分支通过普通合并接入 main `2b0959c1acdd2fe8696617784266caab630c4477`，保留 v1 原件、所有历史、bundle 与空 ledger。未将测试或工作流直接加入签署分支，以保留“可执行输入必须与 main 相同”的校验。

工程 PR 经人工合并后，三个候选仍需普通合并该已接受 main，再重跑校验。共用 CI 每次重新获取三个 PR 的实际 HEAD；旧 Gate 2 HEAD 只作为 v1 原件不可变比较基线。若 main 或候选变化导致代码不一致，测试保持失败保护。

Gate 3 暂不启动；资质索引仍为空，未提交真实 Review 或同步签署。历史 TEST_OUTPUT.md 和 VALIDATION.md 保留其原执行时点，本次运行证据另见共用工程 PR。

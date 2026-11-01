# Gate 2 回归自动化补正

Owner：Codex Astra；交叉复核：独立工程 Agent、ChatGPT 工程复审；最终验收：Human Maintainer。

对应 PR #9、#10、#11 的工程复审意见：将仅在 Markdown 留存的九项本地回归迁入正式测试，并提供真实 GitHub CI 输出。共用实现为 `tests/test_gate2_adaptation.py`，不再维护三份代码或执行 Markdown 中的代码块。

## 执行方式与证据边界

Validate Skills 保留既有完整单元测试及 v1/v2 校验，增加三个候选矩阵任务。每次运行读取 PR 实际 HEAD 和已接受 main，记录 SHA，再检出该不可变 HEAD 作为数据。测试代码、依赖和合成身份 fixture 从工程实现目录加载，不执行候选目录的 Python、依赖安装或第三方 Skill。权限仍为只读，不提交 Review、不写 ledger、不接触真实资质。

默认 `python -m unittest discover -s tests -v` 执行既有 168 项，明确跳过需要外部候选的模块一次；不能称为 177 项已执行。三个独立矩阵任务分别显式运行九项，共 27 次候选回归。缺配置、缺 bundle、错 HEAD、脏数据、遗漏原件均失败，不能以空扫描通过。日志分别显示实现版本、被测候选 HEAD、当前 main 和 v1 原件基线。

九项覆盖：完整矩阵和空 ledger；真实未核证据拒批；缺法源/事实/时效；缺逐项不适用理由；来源、manifest、范围及受保护代码改变；伪身份/授权；全部 v1 原件与历史；真实临时副本删除/改写及摘要清单遗漏；生产政策和空签署隔离。原件基线固定为工程复审接受的三个 Gate 2 HEAD；它们只用于历史比较，当前材料始终取实时 HEAD。

本地复现时，检出共用工程实现和候选到两个目录，从实现目录执行（参数值按 CI 日志）：

```sh
GATE2_REQUIRED=1 \
GATE2_CANDIDATE_ROOT=/path/to/candidate-checkout \
GATE2_BASE_REF=<accepted-main-sha> \
GATE2_HEAD_REF=<candidate-head-sha> \
GATE2_ORIGINAL_REF=<reviewed-gate2-original-sha> \
GATE2_REVIEW_ID=RV-20261017-contract-review \
python -m unittest discover -s tests -p test_gate2_adaptation.py -v
```

原件基线：#9 `6d86b10f34965eee4f65ccbe94078067c1cde5db`；#10 `ad1a925a185f7063571962ea99f3624ba12ec6f3`；#11 `ca313b5a9ea619700eac5ea0333dd958fa55226a`。仅用于回归，不是法律签署时点。

## 合并顺序与停止边界

测试和工作流属于受保护的可执行输入，不能直接添加到三个签署 PR 而绕过与 main 一致的校验。故提出独立共用工程 PR，三个候选仅普通合并当前已接受 main 并更新审阅说明，保留 v1、bundle、空 ledger 逐字节不变。共用工程 PR 的 CI 可在合并前对三个真实 HEAD 提供回归证据。

人工验收并合并共用工程 PR 后，三个候选必须再普通合并该已接受 main，并重跑 CI；否则受保护代码与 main 不一致会保持失败。自动化在合并前处于待验收状态，不声称已成为 main 的长期规则。CI 的只读矩阵不会把跨候选测试结果伪装为各候选的签署 CI 授权。

本轮停在 Gate 2。三个候选保持 Draft，资质索引为空，任何真实签署、同步演练、专业决定或入库均不在本补正中执行。

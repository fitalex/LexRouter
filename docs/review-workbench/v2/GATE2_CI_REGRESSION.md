# Gate 2 回归与后续生命周期

Owner：Codex Astra；交叉复核：独立工程 Agent；工程验收：ChatGPT；合并决定：Human Maintainer。

共用实现 `tests/test_gate2_adaptation.py` 保留九项候选回归。Validate Skills 保留既有套件并运行三个只读候选矩阵；实现目录执行代码，候选目录仅为数据，不执行其 Python 或依赖。新增生命周期及引用选择测试进入默认单测。

## 固定快照与活动检查

空资质与空账本仅断言固定 Gate 2 ORIGINAL 提交的政策和 ledger。其可信锚点是当时 main `d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`。该固定快照严格测试来源/manifest/范围和可执行输入篡改负例；未核证据拒批也使用原始快照，后续补齐证据不会使负例失效。

活动检查仅选择 GATE2_REVIEW_ID 指定的 bundle，其他合法 bundle 不并入其范围。验证当前完整矩阵、固定来源/范围/排除/模板、当前 main 已接受的政策、账本摘要与已接受账本前缀。非空账本调用生产 verify_saved_history 重放真实事件授权、历史政策、来源、摘要和状态机；CI 即便空账本也调用 immutable_history，防止删除尚未合并的签署。开放 PR 检查当前权限/有效期，关闭或合并 PR 采用历史审计模式，继续核验签署当时的授权和不可变性。

v1 原件以固定快照的完整清单及摘要验证；目标 case 不可删改，其他 case 的合法独立签署或合并不会导致本目标失败。真实签署与受控资质只接受生产校验器认证，本轮测试只在内存使用明确标为 SYNTHETIC 的 fixture。

## 引用与退役规则

三个候选由矩阵声明 PR、Review ID、固定 ORIGINAL。每次解析元数据并将提交 SHA、main SHA、实现 SHA、生命周期写入日志。开放 PR 使用实际 head；当前 PR 事件绑定事件 head，防止 A 的检查测成 B。已合并 PR 使用 merge_commit_sha；已关闭未合并 PR 使用最后 head.sha，均不依赖分支存在。缺提交/未知状态直接失败，禁止静默跳过。GitHub 无法再读取提交时，须人工接受显式固定快照迁移，或在独立 PR 移除矩阵行并保留历史 CI 链接；不得自动退役。

ORIGINAL：#9 6d86b10f34965eee4f65ccbe94078067c1cde5db；#10 ad1a925a185f7063571962ea99f3624ba12ec6f3；#11 ca313b5a9ea619700eac5ea0333dd958fa55226a。

本地从实现目录设置 GATE2_REQUIRED=1、GATE2_CANDIDATE_ROOT、GATE2_BASE_REF、GATE2_HEAD_REF、GATE2_ORIGINAL_REF、GATE2_REVIEW_ID，执行 `python -m unittest discover -s tests -p test_gate2_adaptation.py -v`。CI 另设置 GATE2_PR、GATE2_ACTIVE、只读 GH_TOKEN，以审计远端事件历史。默认套件未配置候选时明确跳过模块一次；矩阵配置缺失或目标文件缺失必须失败。

## 合并时序

本 PR 仅提出测试/工作流变更。人工合并后，固定快照回归和活动材料完整性检查继续运行；待同步候选不会因为新增测试文件与 main 不同而使这类材料回归失效。它们不等于当前 head 已具备签署资格。

真实签署的生产 verify_anchors 始终严格检查可执行输入与 main 一致：新 main 接受基础设施后、候选未同步前拒绝签署；普通合并同步后恢复。合成状态转移测试实际验证这三个阶段，没有放宽生产条件。候选同步后须重跑自己的完整 CI 和在线入口，随后另行决定 Gate 3。

本轮不修改政策/资质/真实 ledger/法律材料，不执行任何实际签署，不合并任何 PR。

# 元数据工具测试

LR-P1-01 的 `test_validate_discovery_batches.py` 使用临时合成候选，覆盖多批合法统计、同套件不同任务、跨批 ID 重复、同入口跨 SHA/宿主/raw 与 blob/大小写/百分号编码、固定版本/入口证据遗漏、重复输入、原候选契约错误、坏 JSON/UTF-8/缺文件、CLI 0/1/2 和禁网运行。它不声称自动完成语义去重；真实批次的人工比较见 `docs/P1_BATCH_01_REVIEW.md`。CI 分别运行新批契约及显式新旧联合检查，不抓取第三方站点；无新增依赖。

LR-P0-03 新增 `fixtures/p1-readiness/candidates.json` 与 `valid.json` 配对合成样本、`test_validate_p1_readiness.py` 正反测试。覆盖全部记录及嵌套必填、ID 完整对应、重复和未知 ID、非法状态、无因阻塞、候选快照和字段漂移、来源固定版本、证据读取与 blob 声明、责任遗漏、授权冲突/限制不得伪装 clear、时效日期和专业完成状态禁止升级。反样本在内存中对合成正样本作定向变异，不污染真实候选；CLI 反向用例验证退出 1 与错误位置。禁用 socket 验证准备检查不依赖网络；不安装或执行第三方候选。

`fixtures/valid/` 为固定合法样本，`fixtures/invalid/` 包含分别缺少法域、业务分类、时效锚点及错误字段类型的固定非法样本。全部内容为合成工程数据；占位来源和日期不构成实际核对证据，不是测评数据或正式 Skill。

`python -m unittest discover -s tests -v` 通过真实 CLI 验证退出码、文件位置与字段错误，覆盖日期、枚举、空分类、额外字段、重复 ID、路径、目录递归及 JSON 解析。非法样本被拒绝才算测试通过，不能仅校验空的 `skills/`。

`fixtures/candidates/valid.json` 是独立候选契约的合成正样本；`fixtures/candidates/invalid/` 包含来源缺失、重复 ID、非法判定、授权/法规时效对象或状态缺失七个固定反样本。它们不是真实发现记录，不代表许可或法律复核已经完成。

`test_validate_candidates.py` 离线测试候选 CLI、必填字段、日期、URL、状态一致性、错误位置、JSON 语法和重复键，并验证候选与正式契约不能混用。CI 另检查真实 `data/discovery/candidates.json` 的结构；测试不访问第三方网站，不确认来源真实性。原有 `test_validate_skills.py` 及其 12 项正式元数据测试保留不变。

```sh
python scripts/validate_candidates.py tests/fixtures/candidates/valid.json
python -m unittest discover -s tests -v
```

## LR-P0-04 选品检查

`test_validate_intake_plan.py` 使用 `fixtures/intake/valid.json` 与既有合成 readiness/candidates 配对，验证 A/C/B 提案、原阻塞及审计关联、未知/重复/遗漏 ID、合法模式、独立原创 ID 与权限、审批轴升级、复制/再分发拒绝、门槛及角色、坏 JSON/UTF-8/文件和离线运行。反例在临时目录变异合成数据，不执行第三方内容；生产默认 CLI 也须通过。原有候选和 readiness 审计约束继续由原校验器及原测试负责。

## LR-P0-05 交接检查

`test_validate_p1_handoff.py` 的 14 项测试用既有合成审计/提案和临时合成文件清单验证正例、CLI、审批/时效越权、ID 与原版本绑定、逐文件四类决定、未读文件误判、清单摘要/数量/核心材料、Git tree 重建、原 blob 证据、路径/符号链接逃逸、待办/责任遗漏、坏 JSON/重复键/UTF-8/缺文件及断网运行。反例只在临时目录变异；生产 CLI 另验证 3 条真实交接、2383 文件清单。未运行上游代码或法律用例。

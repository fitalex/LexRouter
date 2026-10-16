# 法律 Skills 发现与候选筛选协议 v1

本协议服务 LR-P0-02，为 P1 的 30–50 个 Skills 整理提供发现入口。发现对象是公开可访问的 Skills、Rules、Prompts 和工作流；不测评、评分、生成榜单或提供路由推荐。正式字段与法律时效要求仍以 [SCHEMA.md](SCHEMA.md)、[正式 Schema](../schemas/skill.schema.json) 和 [测评协议](EVAL_PROTOCOL.md) 为准。

## 发现与核查流程

1. **来源发现**：优先检索中国大陆实务，覆盖合同审查、民商事诉讼、法律检索、企业合规、公司并购、刑事/行政六类。记录检索词、范围、日期和未覆盖方向。聚合目录及搜索摘要只作线索，回到原始项目核查；纯模型、法规数据库或 MCP 数据接口不作为 Phase 1 Skill，只有可辨识工作流时才考虑其工作流入口。
2. **来源核查**：定位原发布账号、原始能力入口及公开说明，优先固定 commit/tag；记录实际读取的证据 URL、版本、核查日期和访问结果。维护主体只按公开账号或来源自述记录，不推定真实身份、作者资质或权属。只访问仓库首页不足以证明某个 Skill 存在，应核对具体入口。URL 格式通过不等于来源真实；网站不可访问时记 `unavailable` 或 `unverified`，保留失败情况及待核查链接，不标为已核实。
3. **法律分类**：按现有 Schema 六类枚举，可多选；分类依据是可定位的任务说明。法域单独记录来源声明及其证据，中文、作者所在地、仓库名称均不能单独证明适用中国大陆法。未知填 `unknown`，非大陆法域填 `other` 并在说明中写明具体范围，不混入正式目录。运行载体使用现有枚举，多个宿主选择有证据的主要载体并解释；通用 Agent Skills 或未确认专属宿主用 `other` 并说明，不能虚构兼容性。
4. **授权核查**：核对固定版本入口、README、LICENSE/NOTICE 及相关范围。记录原许可名称和限制，冲突或缺失进入待核实；搜索摘要、GitHub 自动识别、公开可访问均不能替代授权。未确认第三方授权前不得复制完整 Skill；本阶段只提交原链接、许可事实与独立撰写的简述。不得统一声明第三方材料为 MIT。复制、改写、再分发、商用、品牌及外部数据的授权范围须分别判断，后续实际使用前重新复核。
5. **候选判定**：来源、分类及许可事实足以继续整理者为 `candidate`；入口、法域、授权冲突等仍需补证者为 `needs-evidence`；已知不符合范围、禁止目标使用、无可辨识工作流、伪造来源等为 `rejected`，在说明中记录拒绝依据。已拒绝记录可保留用于防止重复发现，统计时与继续整理的记录分开。

同一能力不同镜像或宿主不重复计数；同一套件可记录一个明确的入口，不以 README 声称的子技能数量扩大发现数量。后续拆分须逐项核查入口、授权与独立用途，保留父项目来源并由 PR 说明去重依据。

## 证据与状态边界

- GitHub Stars、下载量、作者声明、自报认证或项目自身评分不能证明法律专业能力。
- 发现成功仅证明找到来源及能力线索，不代表法律有效性、法律专业水平或输出质量已经验证。
- 来源核查日期、仓库更新时间、抓取时间和模型知识截止时间不能作为法规时效核对日期；作者自称“现行有效”也不够。
- 不得将未经测评的候选标记为正式推荐；`candidate` 仅表示继续整理，不代表正式收录、已测试、可安装或可推荐。
- 候选清单不得包含真实敏感卷宗、密钥、Holdout 内容或未经授权的第三方全文；遵守 [脱敏规范](ANONYMIZATION.md) 与 [贡献指南](../CONTRIBUTING.md)。

| 对象 | 状态 | 含义 |
| --- | --- | --- |
| 来源 | `verified-public` / `unverified` / `unavailable` | 已实际读取原始入口及证据 / 尚未独立读取 / 本次访问失败；不涉及专业或权属确认 |
| 法域 | `source-declared` / `pending-verification` / `verified` | 来源有明确法律体系或法规依据声明 / 证据不足或矛盾 / 已有可追溯专业复核依据；不能仅凭作者自述升为 verified |
| 授权 | `verified` / `pending-verification` / `restricted` / `not-permitted` | 固定版本许可文本明确且无已知冲突 / 缺失、冲突或范围待核 / 已识别附加限制且目标用法待审 / 已知禁止拟议使用或复制 |
| 法规时效 | `not-checked` / `pending-verification` / `verified` | 未开展逐条核查 / 已核查部分但证据不完整 / 针对固定版本、适用场景及截至日期完成法规状态核对并有专业复核证据 |
| 判定 | `candidate` / `needs-evidence` / `rejected` | 继续整理 / 待补证据 / 拒绝收录；任何状态均不构成推荐 |

授权 `verified` 仅表示已核对指定提交的许可文本与声明，不是全面法律审计，也不保证权利人确有全部授权权利。`restricted` 不等于一概不能使用；本流程在拟议复制、改写和分发范围审查完成前保留为待补证据。`not-permitted` 必须判为 `rejected`，不能绕过限制。

## 候选数据契约

清单位于 [data/discovery/candidates.json](../data/discovery/candidates.json)，与正式 `skills/` 隔离。顶层为 `format_version: 1` 和 `candidates` 数组；每个候选不是完整 Skill 元数据，不提供伪造的 `regulatory_as_of`。空数组允许通过结构检查但须明确报告 0，不能声称完成发现目标。未知状态必须显式记录，禁止省略、空值或自由文本替代枚举。

| 必填字段 | 类型与要求 |
| --- | --- |
| `candidate_id` | 遵循正式 ID 字符限制，在清单内唯一；与正式 `id` 分开 |
| `name` / `description` | 使用正式 Schema 的非空及长度约束；简述能力与未验证边界 |
| `source_url` | 具体原始入口的绝对 HTTPS URL；只作格式校验 |
| `maintainer` | 非空字符串，标明公开维护账号及身份核查边界 |
| `business_categories` | 沿用正式 Schema 非空、唯一的六类业务枚举 |
| `jurisdiction` | 对象：`value`（`CN-Mainland` / `unknown` / `other`）、`status`、`evidence_url`、`notes`；四项均必填 |
| `runtime` / `runtime_evidence` | 沿用正式运行载体枚举；非空文字解释依据、其他载体或多宿主选择 |
| `source_verification` | 对象：`status`、有效日期 `checked_at`、非空 `revision`、非空且不重复的 HTTPS `evidence_urls`、`notes`；不能获取版本时明确说明，不能捏造 SHA |
| `authorization` | 对象：`status`、非空 `license`、非空且不重复的 HTTPS `evidence_urls`、`notes`；未知许可用 `not-identified`，链接可指向待核查或访问失败位置并说明 |
| `regulatory_currency` | 对象：`status`、`as_of`、不重复的 HTTPS `evidence_urls`、`notes`；未完成核查时 `as_of` 必须为 null；`verified` 必须有有效日历日期及至少一个核查依据链接，说明中应定位专业复核证据 |
| `candidate_status` / `evidence_notes` | 合法判定枚举及非空证据、限制或拒绝理由 |

上表各对象均禁止额外字段。法域、授权、时效及来源的状态值见前表。`candidate` 要求来源为 `verified-public`、授权为 `verified`，大陆法域有 `source-declared` 或 `verified` 证据；不要求法规时效已核实，因为它尚未进入正式目录。其他情况保留 `needs-evidence` 或有理由地拒绝。

## 检查、维护与正式入库

```sh
python -m pip install -r requirements.txt
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_skills.py skills
python -m unittest discover -s tests -v
git diff --check
```

候选 CLI 默认检查该清单，也可传单个 JSON 文件；只离线检查 UTF-8 JSON、字段、类型、日期、URL 格式、状态一致性与 ID 唯一性，不抓取、下载或执行 Skill。错误写 stderr，标明文件和 JSON Pointer；语法错误附行列；成功退出 0，失败退出 1，参数错误退出 2。拒绝重复 JSON 键和 NaN/Infinity 等非 JSON 常量。契约在脚本中使用现有 jsonschema 实现，复用正式 Schema 的基础字段约束与错误位置辅助函数，无新增依赖，不修改正式校验器。

CI 同时检查实际候选清单、合成正反样本及原有正式校验测试；不依赖实时第三方网站。结构通过不改变记录的核查状态。每次修改候选须保留原始许可与证据，状态变化由 PR 说明理由；来源变化、许可冲突或错误应补新核查记录，不静默升级状态。

进入 P1 后，必须再次核对版本、实际许可范围、法域与法规时效，提供法律专家复核依据，满足正式八字段 Schema 和贡献指南，经独立 PR 审核才能建立 `skills/<id>/metadata.json`。禁止将候选 JSON 直接搬到正式目录；正式收录也不等于测评通过或推荐。未核实法规时效的条目继续留在候选区。

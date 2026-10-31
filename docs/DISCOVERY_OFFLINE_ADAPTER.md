# Discovery 离线适配器原型（LR-DSH-DISC-01）

- 状态：**离线原型，Draft PR，未合并、未启用**；R2 审计 P1/P2 已修复，R3 安全修复已提交，等待 Codex Astra 针对新 head 独立复核。
- 日期：2026-10-31。
- 范围：为每周中文法律 Skills 自动发现提供可重复测试的三个接口；不接真实 Search/Fetch API，不接 API Key，不启用调度。
- 边界：未修改 `ROADMAP.md`、正式八字段、`schemas/`、`data/discovery/candidates.json`、`data/discovery/p1-batch-01.json`、Review Workbench、安全签署或权限代码。
- 产物只用于离线验证。本文和代码都不构成法律、授权、法域或法规时效结论。

## 1. 开源方案调研

数据来自 GitHub REST API 的只读仓库元数据（2026-10-31 查询）；未安装、未运行、未复制上述项目源码。

| 候选 | 功能与复用价值 | 维护活跃度 | 许可证与依赖风险 | 与 LexRouter 现有架构 | 结论 |
| --- | --- | --- | --- | --- | --- |
| [ddgs](https://github.com/deedy5/ddgs) v9.16.1 | 多后端元搜索，直接产出标题/URL/摘要；适合未来替换 `SearchTransport` | 3,042 stars；最近推送 2026-10-23；MIT | 依赖 `click>=8.1.8`、`primp>=1.3.1`、`lxml>=4.9.4`；依赖非官方搜索端点，受限流、页面结构、服务条款影响 | Python >=3.10，可包在现有 transport 协议后；不改变 Fixtures/测试 | **不采用为运行时依赖**。接口保留；后续真实接入须另立任务，评估端点稳定性、条款、成本与凭据 |
| [trafilatura](https://github.com/adbar/trafilatura) v2.3.1 | HTML 正文/元数据抽取、爬取与多格式输出；适合未来处理非 GitHub 的网页来源 | 7,046 stars；最近推送 2026-10-30；Apache-2.0 | 依赖 `certifi`、`charset_normalizer>=3.5.2`、`courlan>=1.4.0`、`htmldate>=1.11.0`、`lxml>=6.1.3`、`urllib3>=2.8,<3`；Apache-2.0 需保留声明 | Python >=3.10；引入 6 个运行时依赖，对本轮 GitHub raw/Markdown Fixtures 无必要 | **暂不采用**。先完成固定版本读取与授权边界；出现真实 HTML 来源需求时再评估 |
| [datasketch](https://github.com/ekzhu/datasketch) v2.0.0 | MinHash/LSH 近似去重，可处理大规模文本近重复 | 2,977 stars；最近推送 2026-10-26；MIT | 依赖 `numpy>=1.11`、`scipy>=1.0.0`，对当前规模过重 | Python >=3.9；数值依赖和概率阈值会引入额外调参 | **不采用**。当前只需 URL 级同入口去重；语义去重按协议必须人工复核，不能把相似度当能力结论 |

**取舍**：优先复用成熟方案是默认原则，但本轮三个候选都不能同时满足“离线可重复、零新增依赖、不复制未授权全文、机器只做同入口去重”。因此采用标准库薄适配器，并保留 `SearchTransport` / `SourceStore` 协议，使 ddgs 或 trafilatura 可在后续独立任务中接入而不改三个接口。该决定不评价上述项目的质量，也不表示已获得其数据源或第三方内容的授权。

## 2. 三个最小接口

入口为 `discovery.DiscoveryAdapter`；`normalize` 同时作为纯函数导出，便于单独测试。

| 接口 | 返回 | 保留的信息 |
| --- | --- | --- |
| `search(query, *, limit=20)` | `SearchResult`：`hits`、`status`（`ok`/`empty`/`error`）、`error.code`、`error.retryable`、`warnings` | 查询词、provider、检索日期、命中顺序、来源 ID、固定 revision 线索 |
| `fetch_pinned(ref)` | `SourceSnapshot`：metadata、`revision`、`evidence_urls`、`retrieved_at`、`status`、`content`/`content_policy` | 请求的 `PinnedRef`、实际 revision、许可线索、法域声明、失败原因；请求与存储 URL 都必须通过严格规范语法校验，并绑定同一源文件路径 |
| `normalize(hit, snapshot=None)` | 现有候选契约的 `dict` | 来源 URL/版本/证据链接；未知状态显式保留；不写法规时效日期 |

`DiscoveryAdapter.collect(query)` 串联三者，并返回独立的批次审计：run ID、时间、搜索状态、命中数、重复、失败阶段、候选统计、内容扣留数。`manifest()` 仅含 `format_version` 与 `candidates`，可直接交给现有 `scripts/validate_candidates.py`。

**CLI 输出契约**：只接受 `--output-dir DIR`。`DIR` 必须是不存在的仓库外路径；CLI 新建 `0700` 私有目录并固定写入 `candidates.json` 与 `audit.json`（`0600`）。旧的任意 `--output`/`--audit` 文件参数已移除，旧调用会以参数错误退出 2。省略 `--output-dir` 时仍将 manifest 输出到 stdout。

### 状态词汇

| 层 | 状态 |
| --- | --- |
| Search | `ok` / `empty` / `error` |
| Fetch | `ok` / `metadata-only` / `not-found` / `revision-mismatch` / `source-mismatch` / `invalid-ref` / `transport-error` / `invalid-source` |
| Candidate | 沿用现有 `candidate` / `needs-evidence` / `rejected` |

`empty` 是合法空结果，不是错误；搜索失败返回 `error` 而不是空列表冒充成功。读取失败不会用搜索摘要替代来源核查。

## 3. 不伪造核查结果的规则

- **法规时效**：`regulatory_currency` 恒为 `not-checked`、`as_of: null`、证据为空。任何检索日期、抓取日期或 fixture 日期都不会被写成时效基准日。
- **法域**：只读取快照中的显式声明；`unknown` 不推断。快照声称 `verified` 时降为 `source-declared`，因为本适配器不执行法律专业复核。若快照缺少有效、可定位的法域证据 URL，仅保留命中入口并降为 `pending-verification`，不得因回退 URL 自动保持 `source-declared`。
- **授权**：`verified` 仅在存在可识别许可名称与至少一个 HTTPS 许可证据时保留；未知状态降为 `pending-verification`；`not-permitted` 直接导致 `rejected`。搜索摘要中的许可线索不构成授权。
- **来源**：没有快照时只能得到 `unverified`；读取失败映射为 `unavailable` 或 `unverified`，并保留错误原因。请求与存储 URL 都必须符合严格 GitHub 规范语法：只接受 `blob`/`raw`/`raw.githubusercontent.com` 固定 revision 形式；owner/repo/revision 不得百分号编码；文件路径段不得包含字面或编码 dot-segment、编码分隔符、空段或控制字符。失败返回 `invalid-ref`/`invalid-source`，不返回正文，也不得成为 `verified-public`。
- **写入**：离线 CLI 只接受 `--output-dir`，在仓库外新建一个进程独占的私有目录（`0700`），固定写入 `candidates.json` 与 `audit.json`（`0600`）。不提供任意文件名，不接受已有目录或仓库路径。目录通过已打开的父目录 fd 与 `mkdir`/`open(..., dir_fd=...)` 创建和写入，避免预检后父 symlink 切换；不产生临时文件。若第二次写入失败，按创建时记录的 `st_dev`/`st_ino` 只清理仍属于本次运行的对象，其他写入者替换的文件保留；清理逐项 best-effort，失败时退出非零并报告残留，不报告成功。
- **全文**：只有 `content_policy: synthetic-own` 的合成 fixture 才返回正文；`reference-only` 即使本地存放了正文也返回 `metadata-only` 且 `content=None`。归一化结果从不包含正文字段。
- **候选判定**：仅当来源 `verified-public`、授权 `verified`、法域 `CN-Mainland` 且状态为 `source-declared`/`verified` 时才为 `candidate`；其余为 `needs-evidence`。这不等于法律或入库批准。
- **去重**：复用仓库校验器的 GitHub 同入口规则（大小写、blob/raw、raw host、百分号编码、不同 revision）。跨仓库镜像、同义工作流、fork 共有内容仍须人工比较；测试只证明同入口不重复计数。

## 4. 代码与 Fixtures

| 路径 | 作用 |
| --- | --- |
| `discovery/models.py` | 命中、快照、失败、批次结果的不可变数据类与状态枚举 |
| `discovery/search.py` | 解析、空结果/错误映射、可注入 `SearchTransport`、本地 fixture transport |
| `discovery/fetch.py` | 请求/存储双侧 pin 校验、来源一致性、revision 一致性、正文复制策略、本地 source store |
| `discovery/normalize.py` | 候选契约映射、未知状态/缺失法域证据降级、无正文复制 |
| `discovery/dedupe.py` | 与 `scripts/validate_discovery_batches.py` 对齐的同入口键 |
| `discovery/adapter.py` | 三个接口的门面与 `collect()` 审计 |
| `scripts/discovery_offline.py` | 离线 CLI；新建私有输出目录并固定文件名；父目录 fd 绑定、对象身份校验与 best-effort 回滚 |
| `tests/fixtures/discovery/search_responses.json` | 合成搜索响应：正常、空、超时、结构错误、缺字段 |
| `tests/fixtures/discovery/sources.json` | 合成固定来源：可复制、仅元数据、含故意标记的受限正文 |
| `tests/test_discovery_adapter.py` | 58 项离线测试 |

所有 fixture 使用虚构的 `synthetic-labs` 仓库与自写正文，不含真实第三方 Skill 全文、真实卷宗、密钥或 Holdout 内容。fixture 中的“MIT”“CN-Mainland”“verified”只是测试状态输入，不是真实核查证据。

## 5. 可重复命令与已验证结果

在仓库根目录、Python 3.11 虚拟环境中：

```sh
python -m unittest tests.test_discovery_adapter -v
python scripts/discovery_offline.py --query "合成合同审查" \
  --output-dir /tmp/lexrouter-discovery-run
python scripts/validate_candidates.py /tmp/lexrouter-discovery-run/candidates.json
python scripts/validate_discovery_batches.py /tmp/lexrouter-discovery-run/candidates.json
python scripts/validate_skills.py skills
python scripts/validate_candidates.py data/discovery/candidates.json
python scripts/validate_candidates.py data/discovery/p1-batch-01.json
python scripts/validate_discovery_batches.py data/discovery/candidates.json data/discovery/p1-batch-01.json
python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
python scripts/validate_intake_plan.py data/intake/p1-proposals.json
python scripts/validate_p1_handoff.py
python -m unittest discover -s tests -v
git diff --check
```

本机实际结果：

- 新测试：**58/58 OK**。
- 离线 CLI：`search=ok hits=3 candidates=2 duplicates=1 failures=0 content_withheld=1`；生成 manifest 通过 `validate_candidates.py` 与 `validate_discovery_batches.py`。
- 原有校验器：正式目录 0；旧/新候选各 10；联合 20；readiness 10；提案 10；handoff 3，全部通过。
- 全量测试：在 `TMPDIR=/private/tmp` 下 **226/226 OK**。
- macOS 默认 `TMPDIR` 下，现有 Review Workbench 因 `/var` 与 `/private/var` 路径归一化出现 5 failures / 34 errors；在未改动的 `origin/main` 工作树上同样复现（168 项中相同 5 failures / 34 errors），与本 PR 无关。CI 使用 Linux，不依赖该 workaround；PR 会列出两种结果，不把默认命令写成已通过。
- R2 修复前，新增的 9 个负例在旧 head `18222fb` 上失败：3 个存储 pin 负例、2 个法域证据负例、4 个 CLI 写入负例；修复后全部通过。
- R3 修复前，在旧 head `7de45c3` 上复跑 Astra 独立脚本：6 个 dot-segment 子例、symlink 切换与 2 个 CLI 清理/替换负例失败；修复后 Pin/Jurisdiction 类原样通过，CLI 四类缺陷由 `test_dot_segments_*`、`test_encoded_path_separators_*`、`test_parent_symlink_swap_*`、`test_rollback_preserves_*`、`test_persistent_cleanup_failure_*` 覆盖并通过。
- `git diff --check`：无输出。

## 6. 未完成事项与后续边界

1. **真实搜索**：ddgs 或正式搜索 API 的接入、凭据、成本、限流、服务条款、重试与缓存，须另立任务并经 Human Maintainer 授权；本轮不启用。
2. **真实读取**：固定版本 HTTP 读取、GitHub 条件请求、速率限制、robots/条款与失败重试；`SourceStore` 协议已留出替换点。
3. **结构化提取**：只有出现非 GitHub HTML 来源时才评估 trafilatura；不得把抽取结果当法律结论。
4. **分类与载体**：`business_categories` / `runtime` 是搜索层或人工输入线索，适配器不猜。真实运行需要独立分类流程及人工复核。
5. **语义去重**：机器只做同入口键；跨仓库镜像、同义任务和套件子项仍按协议人工比较。
6. **批次持久化**：接入 `data/discovery/` 新批次、CI 与统计须独立 PR；不得覆盖现有 20 条候选，不得直接写 `skills/`。
7. **调度**：未实现 cron、队列、后台服务或 API Key 管理。
8. **法律与授权**：全部状态仍待具备能力的人类复核；`candidate` 仅是继续整理状态。
9. **输出契约变更**：CLI 已移除任意 `--output`/`--audit` 文件参数，调用方必须改用 `--output-dir` 并在目录中读取 `candidates.json`/`audit.json`。旧命令会以参数错误退出 2。
10. **输出残余风险**：私有目录为 `0700`，回滚按创建时的 `st_dev`/`st_ino` 身份校验；同 UID 在目录内“原地修改”而非替换的文件不在可检测范围。直接写两个固定文件不提供崩溃/断电后的成对可见性或 fsync 持久性保证；失败会非零退出并报告残留，不报告成功。
11. **平台边界**：目录身份校验依赖 `/proc/self/fd`（Linux）或 `F_GETPATH`（macOS）；两者都不可用时拒绝 `--output-dir` 模式。当前原型只支持 GitHub 固定 URL 形式，其他宿主须另立固定版本规则。

## 7. 给 Antigravity 的文档变更清单（未执行）

以下仅为建议，均未在本 PR 修改；由 Antigravity 在工程合并后维护，技术事实以本 PR 和合并 commit 为准：

| 目标文件 | 建议变更 |
| --- | --- |
| `docs/DISCOVERY_PROTOCOL.md` | 在“自动化 Discovery 分工”后增加“离线适配器原型”小节，链接本文，说明三接口、状态词表、离线边界；明确未启用、未接 API、未新增候选 |
| `data/discovery/README.md` | 增加一句：LR-DSH-DISC-01 只产出合成 fixture 结果，未新增/修改候选记录，候选总数仍为 20 |
| `tests/README.md` | 增加 58 项 Discovery 适配器测试的覆盖范围与断网说明 |
| `docs/daily-specs/README.md` 及新增任务页 | 若项目要求逐任务索引，登记 LR-DSH-DISC-01 的范围、PR、未完成事项；不得写成已上线或已启用 |
| `README.md` | 合并后可在“本地检查”增加 `python -m unittest tests.test_discovery_adapter -v`；如展示 CLI，须使用 `--output-dir` 新契约；合并前不应宣称能力已上线 |
| `docs/DEPENDENCIES.md` | 记录“本任务未新增/升级依赖”；不改变现有 MIT 依赖结论 |

不得修改 `ROADMAP.md`、正式 Schema、八字段、候选记录、Review Workbench 或签署权限；不得把本文写成法律/授权/时效已核实。

## 8. 交接状态

- 工程：可审阅的离线原型，测试与校验证据见上。
- 未合并：Draft PR 目标 `main`，由 Human Maintainer 验收；本任务不自行合并、不进入真实 API 集成阶段。
- 审计：ChatGPT GPT-6 已提出 P1/P2；本 PR 已完成修复并保留 Draft。
- 待独立复核：Codex Astra 针对**新 head** 复核（pin 规范语法、私有输出目录、对象身份回滚）；之后由 Human Maintainer 审核。旧 head 的复核结论不复用。

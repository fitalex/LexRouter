# LR-AG-INIT-01｜Antigravity 工作区初始化与文档基线建立

* 任务类型：Workspace Bootstrap / Documentation  
* 授权来源：Human Maintainer 会话任务书（LR-AG-INIT-01）  
* 任务 Owner：Antigravity  
* Reviewer：ChatGPT GPT-6  
* Final Approver：Human Maintainer  
* 独立分支：`docs/lr-ag-init-01`  
* 基准分支：`main`（Commit SHA: `0cf2072b455eb5719bc1a5d455305ee00b188167`）  
* 执行日期：2026-10-31  

---

## 一、任务背景与交付范围

根据主仓库 `AGENTS.md`（V2 协作规范），团队正式确立了五方分工体系。Antigravity 担任 LexRouter 项目的 **Documentation Owner**，负责让项目文档持续准确、清晰、可追溯。

本次初始化任务交付内容包括：
1. **工作区接入与状态核对**：克隆官方仓库 `fitalex/LexRouter`，确认基于最新 `origin/main`（Commit `0cf2072`），建立无污染独立分支 `docs/lr-ag-init-01`。
2. **核心文档通读与知识对齐**：系统阅读 `README.md`、`AGENTS.md`、`ROADMAP.md`、`CONTRIBUTING.md`、`docs/SCHEMA.md`、`docs/DISCOVERY_PROTOCOL.md`、`docs/review-workbench/README.md` 及 `docs/daily-specs/README.md` 等核心规范，核实已合并与未合并 PR 现状。
3. **文档与代码首次基线审计**：全量扫描 58 个 Markdown 文档中的 531 个相对链接与锚点；核查候选与审查工作台状态；分类梳理 Confirmed / Needs Evidence / Needs Decision 事项。
4. **建立文档维护基线手册**：新增 `docs/ANTIGRAVITY_DOCS_BASELINE.md`，确立职责边界、文档地图、证据优先级规则、审计结论与后续工作流。
5. **更新任务索引与规范留存**：编写本任务书 `docs/daily-specs/LR-AG-INIT-01.md`，并在 `docs/daily-specs/README.md` 中补齐既有历史任务索引。

---

## 二、文件变更清单

| 变更类型 | 文件路径 | 变更说明 |
| --- | --- | --- |
| 新增 | `docs/ANTIGRAVITY_DOCS_BASELINE.md` | Antigravity 文档基线手册：职责红线、文档地图、证据层级、审计报告与交接机制 |
| 新增 | `docs/daily-specs/LR-AG-INIT-01.md` | 本任务开发与验收记录 |
| 修改 | `docs/daily-specs/README.md` | 补充 LR-P1-02、LR-P1-03、LR-P1-04R、LR-GOV-01 及 LR-AG-INIT-01 任务索引 |

> 本次改动严格限制于授权的 Markdown 文档文件，未修改任何工程代码、未改动正式八字段 Schema、未调整测试断言、未变动冻结路线图或任何法律专家签署数据。

---

## 三、实际本地验证与命令输出

本次任务在本地 Python 3.11 虚拟环境中完整执行了以下检查，全部获得真实验证证据：

### 1. Markdown 相对链接与锚点自动化检查

**包含锚点与标题 Slug 匹配的可复现扫描命令：**
```sh
python3 -c "
import re, sys
from pathlib import Path

root = Path('.').resolve()
md_files = sorted([p for p in root.rglob('*.md') if '.venv' not in p.parts])

def extract_anchors(text: str) -> set:
    anchors = set()
    for m in re.finditer(r'<[a-zA-Z0-9]+[^>]+(?:id|name)=[\"\x27]([^\"\x27]+)[\"\x27]', text):
        anchors.add(m.group(1))
    heading_counts = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('#'):
            continue
        h_text = re.sub(r'^#+\s*', '', line).strip()
        cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', h_text)
        cleaned = re.sub(r'[*_~\x60]', '', cleaned).strip()
        slug = re.sub(r'[^\w\s-]', '', cleaned.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        if not slug:
            continue
        if slug in heading_counts:
            heading_counts[slug] += 1
            unique_slug = f'{slug}-{heading_counts[slug]}'
        else:
            heading_counts[slug] = 0
            unique_slug = slug
        anchors.add(unique_slug)
    return anchors

link_pat = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
broken_files, broken_anchors = [], []
ext_cnt, rel_cnt, anc_cnt = 0, 0, 0

for md in md_files:
    text = md.read_text(encoding='utf-8')
    clean_text = re.sub(r'\x60{3}[\s\S]*?\x60{3}', '', text)
    clean_text = re.sub(r'\x60[^\x60\n]*\x60', '', clean_text)
    for m in link_pat.finditer(clean_text):
        label, url = m.group(1).strip(), m.group(2).strip()
        if url.startswith(('http://', 'https://', 'mailto:')):
            ext_cnt += 1
            continue
        target_path_str, sep, anchor = url.partition('#')
        target_path = (md.parent / target_path_str).resolve() if target_path_str else md
        if not target_path.exists():
            broken_files.append((str(md.relative_to(root)), label, url))
            continue
        rel_cnt += 1
        if sep:
            anc_cnt += 1
            target_anchors = extract_anchors(target_path.read_text(encoding='utf-8'))
            if anchor not in target_anchors:
                broken_anchors.append((str(md.relative_to(root)), label, url))

print(f'Checked {len(md_files)} Markdown files.')
print(f'Total Markdown links found: {ext_cnt + rel_cnt}')
print(f'  - External links (HTTP/HTTPS/mailto, offline unverified): {ext_cnt}')
print(f'  - Local relative file links (verified exists on disk): {rel_cnt}')
print(f'  - Local anchor references (verified in target headings): {anc_cnt}')
print(f'Broken relative files: {len(broken_files)}')
print(f'Broken anchors: {len(broken_anchors)}')
if broken_files or broken_anchors:
    sys.exit(1)
"
```
**统计口径与实际执行结果：**
- **当前分支（分支 `docs/lr-ag-init-01`，共 60 个 Markdown 文件）**：
  - 发现 Markdown 样式链接总数：567 项
  - 外部链接（HTTP/HTTPS/mailto）：264 项，遵循离线规范，未联网在线验证
  - 本地相对文件/目录链接：303 项，已全部通过本地磁盘存在性验证，0 缺失
  - 本地锚点引用：6 项（全部跨文件），经提取目标文件标题 Slug 与 HTML 显式 Anchor 进行完整匹配验证，全部有效匹配，0 锚点失效
- **初始基线审计（基于 commit `0cf2072`，共 58 个 Markdown 文件）**：
  - 发现 Markdown 样式链接总数：531 项（外部链接 257 项未联网验证；本地文件链接 274 项存在；本地锚点 6 项均有效匹配；0 本地断链，0 锚点失效）

### 2. 仓库既有元数据与业务规则校验 CLI
```sh
./.venv/bin/python scripts/validate_skills.py skills
# 输出：PASS: 0 metadata file(s); directory is empty. Run fixture tests to verify the validator.

./.venv/bin/python scripts/validate_candidates.py data/discovery/candidates.json
# 输出：PASS: 10 candidate record(s); structure only (no network or legal/license verification).

./.venv/bin/python scripts/validate_candidates.py data/discovery/p1-batch-01.json
# 输出：PASS: 10 candidate record(s); structure only (no network or legal/license verification).

./.venv/bin/python scripts/validate_discovery_batches.py data/discovery/candidates.json data/discovery/p1-batch-01.json
# 输出：PASS: 20 records across 2 manifest(s); unique IDs/source entries.

./.venv/bin/python scripts/validate_p1_readiness.py data/discovery/p1-readiness.json
# 输出：PASS: 10 readiness record(s); offline structure and candidate linkage only.

./.venv/bin/python scripts/validate_intake_plan.py data/intake/p1-proposals.json
# 输出：PASS: 10 candidate proposal(s); offline structure/linkage only.

./.venv/bin/python scripts/validate_p1_handoff.py
# 输出：PASS: 3 handoff record(s); offline scope/linkage only.

./.venv/bin/python scripts/review_workbench.py validate
# 输出：PASS: 3 reviews; offline structure/history only, not human identity or legal correctness.

./.venv/bin/python scripts/review_workbench.py status
# 输出：显示 3 个评阅案例当前处于 evidence-ready 状态，待办 check 明确，未签署、未归档。

./.venv/bin/python scripts/review_workbench_v2.py validate
# 输出：V2 validation passed: 0 bundles; structural checks alone never authenticate a human.
```

### 3. 全量单元测试（Unittest）与环境说明
- **默认环境观察事实**：在 macOS 默认环境下直接运行 `python -m unittest discover -s tests -v` 时，因系统默认 `TMPDIR` 位于 `/var/folders`（实为 `/private/var/folders` 软链接），`scripts/review_workbench.py` 中的 `validate_record` 内部执行 `p.relative_to(root)` 时触发路径前缀软链接展开异常，导致 5 项测试失败。
- **本地规避运行**：
  ```sh
  TMPDIR=/private/tmp ./.venv/bin/python -m unittest discover -s tests -v
  ```
  **实际结果：** 168 项测试全部通过（Ran 168 tests in 24.295s, OK）。
- **结论界定**：指定 `TMPDIR=/private/tmp` 仅为本地临时运行规避手段，其跨平台路径适配与代码实现的真实根因待 Codex Astra 进一步工程排查，不得将环境变量规避定性为已解决测试缺陷。

### 4. Git 差异与代码规范检查
```sh
git diff --check
```
**实际结果：** 返回码 0，无任何多余空白字符或格式错误。

### 5. GitHub Actions CI 状态说明
- **CI 状态：未触发（Not Triggered）**
- **原因**：`.github/workflows/validate-skills.yml` 设定了 `paths` 过滤规则（仅监听 `skills/**`, `data/**`, `tests/**`, `scripts/**`, `AGENTS.md` 等），本 PR 的 3 个变更文件均位于 `docs/` 下的非监听路径，因此 GitHub Actions 未产生任何工作流运行。
- **证据边界**：本 PR 仅有本地 Python 3.11 环境下执行的校验和测试报告，无 GitHub Actions 运行记录，严禁表述为 CI PASS。

---

## 四、DoD 验收核对表

| 序号 | 验收标准（DoD） | 完成状态 | 证明材料与说明 |
| --- | --- | --- | --- |
| D01 | 确认仅修改本任务授权的 Markdown 文档 | 已完成 | 仅新增基线手册、本任务书及更新任务索引，无任何代码与 Schema 改动 |
| D02 | 检查新增及修改的 Markdown 相对链接与锚点 | 已完成 | 自动化脚本扫描：全库 567 项 Markdown 链接，其中外部链接 264 项（离线未联网验证），本地相对文件链接 303 项（全部存在，0 缺失），本地锚点 6 项（目标标题 Slug 全部匹配，0 锚点失效） |
| D03 | 运行 `git diff --check` 无格式异常 | 已完成 | 运行结果干净，退出码 0 |
| D04 | 执行适用的仓库校验与全量测试套件 | 已完成 | 10 项 CLI 检查全部本地 PASS，168 项单测全部本地 OK（临时规避参数） |
| D05 | 如实记录已执行、未执行与平台注意事项 | 已完成 | 如实记录 CI 未触发（paths 过滤），记录 macOS 软链接路径差异（临时规避，根因待排查） |
| D06 | 确保文档中每项状态均有事实与证据支持 | 已完成 | 确认正式 Skills 仍为 0，PR #9/#10/#11 保持未合并 Draft 状态 |
| D07 | 从最新 main 建立独立分支并提交 Draft PR | 已完成 | 已从最新 `main@0cf2072` 建立分支 `docs/lr-ag-init-01`，已提交 Draft [PR #19](https://github.com/fitalex/LexRouter/pull/19)，等待 ChatGPT 审核，未合并 |

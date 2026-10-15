# Skill 元数据规范 v1

本规范与 [skill.schema.json](../schemas/skill.schema.json) 同步，采用 JSON Schema Draft 2020-12。每个文件为一个 UTF-8 JSON 对象，正式条目建议位于 `skills/<id>/metadata.json`。校验器递归检查指定目录内全部 `.json` 文件（后缀不区分大小写），因此不要在该目录混入其他用途的 JSON。

## 字段契约

以下八个字段全部必填；不允许额外字段、空值或以省略字段推定默认值。

| 字段 | 类型与约束 | 语义 |
| --- | --- | --- |
| `id` | 字符串，1–80 字符；小写字母/数字，单个连字符分段 | 仓库内稳定唯一标识；目录批量校验时检查重复，后续改名须审核 |
| `name` | 字符串，1–120 字符，至少一个非空白字符 | 原始能力名称，不虚构能力 |
| `description` | 字符串，1–500 字符，至少一个非空白字符 | 简短、可核实的用途与限制 |
| `source_url` | 绝对 HTTPS URI，不允许空白，须有主机 | 原作者或原始发布来源；优先链接固定版本。机器仅校验格式，不联网验证来源、可用性或授权 |
| `jurisdiction` | 字符串，仅允许 `CN-Mainland` | 中国大陆法域；v1 暂只收录该法域。Schema 的 default 仅作说明，不自动补齐，缺失仍失败 |
| `business_categories` | 非空字符串数组，元素唯一且来自下方枚举 | 适用业务分类，可多选，不用自由文本替代 |
| `regulatory_as_of` | `YYYY-MM-DD` 字符串，必须是有效日历日期 | 贡献者已核对该 Skill 所涉法律状态的法规时效基准日（截至该日），不是抓取日期、提交日期、模型知识截止日，也不是所有法规统一的生效日 |
| `runtime` | 字符串，来自下方枚举 | 原始能力的运行载体；不代表 LexRouter 已实现兼容或安装功能 |

业务分类允许值：

| 值 | 名称 |
| --- | --- |
| `contract-review` | 合同审查 |
| `civil-commercial-litigation` | 民商事诉讼 |
| `corporate-ma` | 公司并购 |
| `corporate-compliance` | 企业合规 |
| `criminal-administrative` | 刑事/行政 |
| `legal-research` | 法律检索 |

运行载体允许值：`claude-skill`（Claude Skills）、`codex-skill`（Codex Skills）、`cursor-rule`（Cursor Rules）、`dify-workflow`（Dify 工作流）、`prompt`（独立提示词）、`other`（其他载体，须在描述及 PR 中说明）。一个条目记录主要原始载体，多载体表示方式留待后续需求审核。

扩展法域、分类、载体或字段须通过 PR 同步更新 Schema、文档和测试，不得用 `other` 冒充其他法域或业务分类。

## 时效与人工审核

`regulatory_as_of` 必须有实际核对依据，收录 PR 应给出对应版本、引用法规及其生效/废止状态的来源，由法律专家复核。未知时不得填 `unknown`、`null`、空字符串或任意占位日期（包括把今天当作已核对日期）；资料不足的条目留在待补讨论中，不进入正式目录。

格式校验能够拒绝不存在的日历日期，但不能证明某日确已核对、日期没有被编造或法规适用正确。历史法律场景、过渡条款及个别法律生效日期见 [测评协议](EVAL_PROTOCOL.md)，来源授权见 [贡献指南](../CONTRIBUTING.md)。

## 示例与验证

完整合法结构见 [固定合成样本](../tests/fixtures/valid/metadata.json)。其中日期和 `example.com` 链接仅供结构测试，不是正式条目的核对证据或已收录 Skill。

```sh
python -m pip install -r requirements.txt
python scripts/validate_skills.py skills
python scripts/validate_skills.py path/to/metadata.json
python scripts/validate_skills.py path/to/directory another/metadata.json
python -m unittest discover -s tests -v
```

省略路径时默认检查本仓库 `skills/`。目录递归读取 JSON；路径不存在、显式指定非 JSON 文件、JSON 解析失败、结构不符、批次内重复 `id` 均返回退出码 1。命令参数错误由 argparse 返回 2。所有文件合法返回 0；空目录明确显示 0 个文件，不能独立证明校验器有效。重叠输入路径去重；唯一性范围是本次输入集合，正式收录必须校验整个 `skills/`。

错误写入标准错误，指出文件路径和 JSON Pointer 字段位置（如 `/jurisdiction`）；JSON 语法错误附行列，根节点用 `/` 表示。CI 同时校验正式目录与固定合法样本，并执行非法样本测试。工具只校验数据，不下载或执行 Skill。

依赖选择：`jsonschema` 用于成熟的 Draft 2020-12 结构校验与日期检查；仅额外引入 `rfc3986-validator` 支持 URI 格式检查，避免安装无关格式检查依赖。Python 标准库 unittest 提供测试，不引入数据库、服务或测评框架。

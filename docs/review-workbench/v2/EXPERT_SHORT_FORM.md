# Gate1 四块专家短表

**可填写预览；不是签署、专业结论或入库批准。** 本人只需阅读对应候选的五组预览和必要证据，在下列短表填写真实意见，再本人提交一次 GitHub **Comment Review**。其后维护者另提交一次独立入库决定。Gate1 尚未启用自动接收，不要把此文档示例当成真实事件。

系统提供固定 Review-ID、完整 Scope 和 Group-ID；专家不编辑 JSON、不计算或复制摘要、不粘贴事件 URL，也不运行 CLI。对范围有异议时在理由中说明，由工程人员生成新范围/新Review，不能删掉文件后沿用原签署。各候选的预填格式见本页末的链接。

以下每个字段均给出纯格式例与待填占位。例子使用虚构对象和假设问题；`needs-changes` 仅演示语法，不能复制为三候选真实专业结论。**占位、例子和空白均不得被识别为有效签署。** 官方门户和 `not-verified` 证据不满足专业通过；未核范围可形成补正意见，但不能填通过或虚构日期。

## 1. scope：对象与精确范围

| 字段 | 纯格式示例（虚构） | 实际待填/系统预填位置 |
| --- | --- | --- |
| Review-ID | `RV-EXAMPLE-ONLY` | `〈系统预填本轮Review-ID，请核对〉` |
| Scope（可重复） | `SKILL.md` | `〈系统逐行预填所有完整路径，请核对〉` |

## 2. findings：各组专业判断

一组一行，格式为 `Group: ID | 决定 | 理由 | 限制`。五组均必须出现。理由按检查项 ID 指明关键事实、依据、适用推理、反例、待补正及证据位置；需要长说明时写在允许公开的附件中，在理由中明确定位。不得用“同意”“见材料”取代具体判断。

| 行内字段 | 纯格式示例（虚构） | 实际待填位置 |
| --- | --- | --- |
| Group-ID | `G1` | `〈系统预填G1–G5〉` |
| 组决定 | `needs-changes` | `〈approved-scope / needs-changes / rejected / not-applicable〉` |
| 组理由 | `示例：C02缺行为发生日期，不能选择适用版本；须补日期后核查` | `〈本人写具体理由、支持/反例、未决与证据索引〉` |
| 组限制 | `示例：补证前不得用于事实未明的交易` | `〈本人写适用限制；确无另加限制也须明确说明〉` |

`not-applicable` 必须写事实与依据，不能表达“没看过”。如仍缺任何组内必需项，选择补正或拒绝并说明，而非以整体通过隐藏未核项。

## 3. professional_decision：总体专业意见与独立性

| 字段 | 纯格式示例（虚构） | 实际待填位置 |
| --- | --- | --- |
| Axis | `professional_review` | `professional_review`（系统固定） |
| Decision | `needs-changes` | `〈approved-scope / needs-changes / rejected〉` |
| Reason | `示例：因G1缺事实、G2缺官方版本，暂不能形成通过意见` | `〈本人写总体专业理由、未完成补正及处理〉` |
| Limitations | `示例：限所列文件；未核事实不作签约建议` | `〈本人写明确用途和排除/保留事项〉` |
| COI | `示例：已披露与假设委托方的业务关系，待确定回避安排` | `〈本人真实利益冲突/独立性声明及必要处置〉` |

公开表不放证件、真实卷宗、签名图片、私信、受限附件或私人路径。一次性资质/能力核实索引由维护者在受控材料基础上接受，不能由AI造索引；表内公开账号也不证明专业资格。`admission_decision` 只供维护者的第二个独立事件，不能在本表同时作两种决定。

## 4. maintenance：法规核查基准

| 字段 | 纯格式示例（虚构） | 实际待填位置 |
| --- | --- | --- |
| Regulatory-As-Of | `not-verified`（尚未实际核法的补正意见）；日期格式为 `YYYY-MM-DD` | `〈本人实际核查日期；未核的非批准意见用not-verified〉` |

填写本人实际核查适用法规的日期；不得填写模型日期、抓取日、commit日或未来日期来补空。尚未实际核查时，补正或拒绝意见可明确填 `not-verified`；专业通过和入库决定必须提供实际日期。这个单一日期只是本轮基准；逐法有效期间和过渡仍在证据附件按检查项保留。下次复核日期、来源/法规/许可/范围/风险变化触发项由系统附件展示，专家可在限制或理由中要求调整。

## 完整可填写格式

正式提交的 Comment Review 中仅保留**一个** `lexrouter-review-v2` fenced block。标题和字段名固定；分组行内不要使用额外的 `|`，可用中文分号表达。下列是占位模板，尚不可提交；实际候选表已预填全部路径，链接见后。

```lexrouter-review-v2
[scope]
Review-ID: 〈系统预填〉
Scope: 〈系统逐行预填完整范围，不以省略号替代〉
[findings]
Group: G1 | 〈决定〉 | 〈具体理由、事实、依据及待补正〉 | 〈限制〉
Group: G2 | 〈决定〉 | 〈具体理由、事实、依据及待补正〉 | 〈限制〉
Group: G3 | 〈决定〉 | 〈具体理由、事实、依据及待补正〉 | 〈限制〉
Group: G4 | 〈决定〉 | 〈具体理由、事实、依据及待补正〉 | 〈限制〉
Group: G5 | 〈决定〉 | 〈具体理由、事实、依据及待补正〉 | 〈限制〉
[professional_decision]
Axis: professional_review
Decision: 〈总体专业决定〉
Reason: 〈本人总体理由〉
Limitations: 〈本人用途、排除及保留〉
COI: 〈本人独立性和利益冲突声明〉
[maintenance]
Regulatory-As-Of: 〈本人实际核查YYYY-MM-DD〉
```

- [通用合同审查预填短表](contract-review-form.md)：27文件，G1–G5。
- [律师服务合同预填短表](contract-review-zh-form.md)：4文件，G1–G5。
- [企业法务组件预填短表](china-legal-counsel-form.md)：19文件，G1–G5；数据库排除。

接收端须拒绝未知字段、重复单值键、重复/遗漏组、路径缺失/扩大、空白/占位、非法决定、未来/过期日期、身份权限/事件不可信和无法在线核验等情况。具体校验实现由 Gate1 工程测试证明；本说明不声称现有 v1 CLI 已支持该格式。本人提交前若 PR head、材料或范围变化，应读取新材料；系统须按本人 reviewed head 绑定，不把旧意见自动升级为新版本意见。

## 完整已填写示例（仅格式演示）

以下虚构单组对象演示“未核法也能明确要求补正”，并非任何真实候选的专业意见。实际对象由机器生成所有必需组，不得照抄这个示例省略其余组；该 Review-ID 在真实候选中不存在。

````text
```lexrouter-review-v2
[scope]
Review-ID: RV-EXAMPLE-ONLY
Scope: SKILL.md
[findings]
Group: G1 | needs-changes | CR01示例：不能在未区分约定标的、违约损失、调整请求与具体法律适用时，以合同价30%统一判断无效；须补行为日期、官方条款和适用版本后复审 | 补正前不得输出确定效力结论
[professional_decision]
Axis: professional_review
Decision: needs-changes
Reason: 示例：事实时间和官方版本未核实，暂不形成专业通过意见
Limitations: 示例：仅讨论所列文件的假设命题，不授权托管、运行或入库
COI: 示例：假设复核人与该虚构项目无利益关系；真实表必须由本人如实填写
[maintenance]
Regulatory-As-Of: not-verified
```
````

维护者第二步由程序生成同一范围及议题的短表，`Axis` 为 `admission_decision`，决定选 `admitted / declined / suspended`，另写本人理由。该事件绑定已经同步的专业意见和全部证据；程序绝不从专业通过自动推导入库。

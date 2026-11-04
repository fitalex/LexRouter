# Gate 2 验证说明

**本地168项既有完整单测、9项新增候选适配回归及全部14组校验命令通过。** [实际输出](TEST_OUTPUT.md)包含逐命令退出码及原始测试名称/计数。原件摘要见[兼容性报告](compatibility.md)。GitHub CI另外执行既有168项测试及v1/v2校验，实际run URL与最终head记录于本PR描述。

## 基线与范围

- 接受的main：`d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`；原PR #9 head：`a7c7d9541e0f6b84a30d5643890de59ed4673a7b`。
- 上游：`NOMOREKKK/contract-review-skill` / `f73f92b6341ef4e9f1765434bf348b1acb4fb1d3`；完整31个叶子路径/blob/mode/type已用实际GitHub tree重新比对，响应未截断。
- 范围27文件，排除4；15检查项逐文件映射，共405行。bundle 809207 B，小于900KiB，兼容GitHub Contents base64读取。
- 普通合并main并追加sidecar，不force-push、不修改既有提交。原28个case文件逐字节不变；旧start与人工工作表不改。程序、模板、政策、正式八字段和ROADMAP与main保持一致。

## 执行边界

执行正式skills/正例、candidate两批及去重、readiness/正例、intake/正例、P0 handoff、v1/v2 `validate --online --base-ref origin/main`、diff检查、候选附加9项测试与完整unittest。提交前另作已暂存diff检查和文档本地链接检查。

附加9项以真实候选bundle和空ledger为输入：完整覆盖/空签署；现有未核材料不能通过；缺法源/事实/时效拒绝；逐项不适用理由缺失拒绝；来源/manifest/范围变化拒绝；合成伪身份/权限拒绝；v1原件一致；删除/改写原件拒绝；政策与真实ledger没有被测试签署污染。测试仅在内存使用标为SYNTHETIC的完整证据fixture，不持久化伪签署或虚假资质。源码及重跑方式见[ADAPTATION_TESTS.md](../ADAPTATION_TESTS.md)。

真实ledger仍为空，真人事件为0。在线入口验证没有伪造事件、没有执行真实签署往返；当前空`credential_refs`继续阻断签署。源树adapter使用已实际在线比对过的固定manifest作为离线回归夹具，不声称离线认证GitHub事件。后续Gate3再由本人真实Review检验通知与自动写回。

## 法律、权利与工程缺口

来源页面、文号、条款和日期的检索记录见[sources](sources.md)，不能当作专家结论。逐条事实、法律适用、时效/过渡及第三方权利链继续`not-verified`；没有填实际法规复核日期。原许可证仅只读核查，未复制第三方Skill正文、安装或执行上游。运行、OCR/宿主/知识库/外部服务等限制见[precheck](precheck.md)。

shell Git代理不可连接，远端元数据读取和受保护的fast-forward提交通过已授权GitHub连接器执行；远端tree必须与本地最终tree一致。不会因网络条件降级签署信任，也不读取仓库外私有资质材料。

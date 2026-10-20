# LR-P1-04R Gate 1 验证证据

本地全量 **161 项测试通过**：原有118项、v2核心32项、可信同步桥接11项；原有全部校验及v1/v2在线验证入口通过。完整命令、标准输出和测试名称见 [TEST_OUTPUT.txt](TEST_OUTPUT.txt)，不是模型自述 PASS。GitHub Actions 的本次运行链接与结果记录在工程PR描述中。

**真人签署数为0，真实v2 bundle数为0。** GitHub身份、事件、写回和反例通过合成API fixture测试；没有提交真人Review、没有导入真实专业意见。`validate --online` 对空事件集通过不能称为真人签署验收；真实自动触发与令牌权限演练留在 Gate 3。

## 正反测试覆盖

| 边界 | 通过的正例 | 拒绝的反例 |
| --- | --- | --- |
| 预审/专业分离 | agent-precheck保存完整矩阵，账本初始为空 | AI机器字段不能成为真人签署；缺组、重复组、缺C项/专项、扩大范围 |
| 本人身份与main政策 | 合成User拥有已接受角色、受控资格索引和write权限 | Bot、错误本人、缺资格、分支自授权、角色/权限撤销、普通评论状态 |
| GitHub事件 | 未编辑Comment Review绑定当前head、完整附件和前序账本 | GraphQL查出首次导入前编辑、字段缺失/错误节点/查询错误，已导入事件编辑/撤销 |
| 来源与时点 | main subject/模板与完整固定Git tree吻合 | 省略专项模板、源blob变化、遗漏源文件、未核法源/事实/适用/时效、未来或过期日期 |
| 权利三轨 | 对应轨所有必需证据存在且明确核验 | 任一授权/许可/原创性/外部索引证据缺失或not-verified |
| 独立入库 | 同一真人可用两个独立事件分别作专业及维护者决定 | 未专业签署先admitted、复用同事件、伪造手工历史、替换终局意见 |
| CI真实性 | 指定GitHub Actions检查成功且可执行输入与main一致 | 缺检查、失败、旧head、错误app、最新重跑失败、同名workflow/根Python模块劫持 |
| 并发与写回 | Git tree提交只改一个ledger，ref不强推 | head/main/Review并发变化、CAS冲突、两个当前决定竞争 |
| 历史保留 | 原前缀字节不变，按真实事件确定性重放 | 摘要漂移、镜像字段篡改、未合并ledger/整轮目录删除、force-push、分页/commit截断 |
| 通知信任 | 无权限signal唤醒main程序，只从API取真实数据 | 错误workflow路径/事件、fork、非main PR、读取产物作为签署；公开未授权评论不能阻断本人 |
| 已接受历史 | 合并关闭后的原PR仍可追溯，过期历史不造成新轮死锁 | 旧档不续期、不把旧专业意见带入新轮；活跃入库仍检查当前时效与权限 |

测试代码：[核心](../../../tests/test_review_workbench_v2.py)、[工作流桥接](../../../tests/test_review_workbench_v2_sync_run.py)。所有身份、事件ID、日期和法律文字都是合成fixture，不能引用为真实法律或授权证据。

## 实际执行

执行了正式skills及正例、两批candidate及跨批去重、readiness及正例、intake及正例、P0 handoff、v1/v2工作台、全量unittest和diff检查。逐条命令与退出码保存在输出文件。

```sh
python scripts/validate_skills.py skills
python scripts/validate_intake_plan.py
python scripts/validate_p1_handoff.py
python scripts/review_workbench.py validate --online --base-ref origin/main
python scripts/review_workbench_v2.py validate --online --base-ref origin/main
python -m unittest discover -s tests -v
git diff --check
```

额外核对：三个短表Scope分别精确等于原subject的27/4/19个路径；预览映射分别完整覆盖15/15/16项原模板。42个保护文件（含全部27个case文件）与main逐字节一致，摘要见[迁移报告](PERMISSIONS_AND_MIGRATION.md#原件校验)。未新增依赖，未执行第三方代码。

## Gate 1 后的验收边界

- 本PR供工程验收，不合并/关闭/重写 #9、#10、#11，不修改冻结路线图、正式八字段、v1签署及归档。
- Gate 2先接受必要的真实受控资格索引，再逐候选重新绑定main/head和新v2附件；预览中的法源门户、未核时效和授权缺口必须补齐。
- Gate 3由本人实际提交一次新的Comment Review，验证GitHub通知、API权限及CAS回填。不得为演示自动提交机器人签名。
- 当前运行环境的shell Git网络代理不可连接，远端基线核对与工程PR提交使用已授权GitHub连接器。此项不影响离线测试，不冒称本地完成了真实GitHub签署往返。

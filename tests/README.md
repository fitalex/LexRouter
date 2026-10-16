# 元数据工具测试

`fixtures/valid/` 为固定合法样本，`fixtures/invalid/` 包含分别缺少法域、业务分类、时效锚点及错误字段类型的固定非法样本。全部内容为合成工程数据；占位来源和日期不构成实际核对证据，不是测评数据或正式 Skill。

`python -m unittest discover -s tests -v` 通过真实 CLI 验证退出码、文件位置与字段错误，覆盖日期、枚举、空分类、额外字段、重复 ID、路径、目录递归及 JSON 解析。非法样本被拒绝才算测试通过，不能仅校验空的 `skills/`。

`fixtures/candidates/valid.json` 是独立候选契约的合成正样本；`fixtures/candidates/invalid/` 包含来源缺失、重复 ID、非法判定、授权/法规时效对象或状态缺失七个固定反样本。它们不是真实发现记录，不代表许可或法律复核已经完成。

`test_validate_candidates.py` 离线测试候选 CLI、必填字段、日期、URL、状态一致性、错误位置、JSON 语法和重复键，并验证候选与正式契约不能混用。CI 另检查真实 `data/discovery/candidates.json` 的结构；测试不访问第三方网站，不确认来源真实性。原有 `test_validate_skills.py` 及其 12 项正式元数据测试保留不变。

```sh
python scripts/validate_candidates.py tests/fixtures/candidates/valid.json
python -m unittest discover -s tests -v
```

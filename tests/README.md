# 元数据工具测试

`fixtures/valid/` 为固定合法样本，`fixtures/invalid/` 包含分别缺少法域、业务分类、时效锚点及错误字段类型的固定非法样本。全部内容为合成工程数据；占位来源和日期不构成实际核对证据，不是测评数据或正式 Skill。

`python -m unittest discover -s tests -v` 通过真实 CLI 验证退出码、文件位置与字段错误，覆盖日期、枚举、空分类、额外字段、重复 ID、路径、目录递归及 JSON 解析。非法样本被拒绝才算测试通过，不能仅校验空的 `skills/`。

# Skills 目录与收录规范

这是 Phase 1 的正式能力元数据目录。P0-01 尚无正式条目；首批 30–50 个 Skills 的整理属于 P1，不在本次初始化中进行。

后续收录布局：`skills/<id>/metadata.json`，一个文件一个 Skill，字段遵循 [SCHEMA.md](../docs/SCHEMA.md)。目录中的所有 JSON 均被视为元数据文件。`id` 在全目录内唯一，来源应可追溯，必须明确法域、业务分类、真实的法规时效基准日与运行载体。未知时效不能编造日期以通过校验。

先提交原始来源、版本与授权依据供审核；未经许可不复制第三方内容。不得收录密钥、真实敏感数据或 Holdout 内容；不得把测试合成样本作为真实 Skill 入库。收录和修改通过独立分支 PR，执行：

```sh
python scripts/validate_skills.py skills
python -m unittest discover -s tests -v
```

机器校验只确认结构及批次内标识唯一，不代表法律专业审核、来源授权或性能测评通过。完整审核要求见 [CONTRIBUTING.md](../CONTRIBUTING.md)。当前许可证尚待人工批准，公开目录不代表取得明确的开源再分发授权。

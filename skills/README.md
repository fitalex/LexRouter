# Skills 目录与收录规范

这是 Phase 1 的正式能力元数据目录。P0-01 尚无正式条目；首批 30–50 个 Skills 的整理属于 P1，不在本次初始化中进行。

LR-P0-02 的发现候选保存在 [data/discovery/](../data/discovery/README.md)，不得放入本目录。候选可保留明确的待核实状态；正式条目必须满足真实法域、法规时效基准日与授权审核要求，不能用候选的来源核查日期代替。详见 [发现协议](../docs/DISCOVERY_PROTOCOL.md)。

后续收录布局：`skills/<id>/metadata.json`，一个文件一个 Skill，字段遵循 [SCHEMA.md](../docs/SCHEMA.md)。目录中的所有 JSON 均被视为元数据文件。`id` 在全目录内唯一，来源应可追溯，必须明确法域、业务分类、真实的法规时效基准日与运行载体。未知时效不能编造日期以通过校验。

先提交原始来源、版本与授权依据供审核；未经许可不复制第三方内容。不得收录密钥、真实敏感数据或 Holdout 内容；不得把测试合成样本作为真实 Skill 入库。收录和修改通过独立分支 PR，执行：

```sh
python scripts/validate_skills.py skills
python -m unittest discover -s tests -v
```

机器校验只确认结构及批次内标识唯一，不代表法律专业审核、来源授权或性能测评通过。完整审核要求见 [CONTRIBUTING.md](../CONTRIBUTING.md)。Human Maintainer 已批准 LexRouter 自主原创代码采用 [MIT License](../LICENSE)（LR-P0-01A）；第三方 Skills、代码、数据集、法律文本及其他材料仍遵循各自授权，必须保留必要的版权和许可证声明，未确认授权不得直接复制入库。收录不代表材料成为 LexRouter 原创作品或改为 MIT 授权。

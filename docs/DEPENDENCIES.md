# 直接依赖许可证检查

检查范围：LR-P0-01A 中的 [requirements.txt](../requirements.txt) 两项直接依赖。未新增、升级或修改依赖；不变更第三方许可证。

| 依赖 | 固定版本 | 许可证（SPDX） | 核对证据 |
| --- | --- | --- | --- |
| [jsonschema](https://pypi.org/project/jsonschema/4.25.1/) | 4.25.1 | MIT | 已安装发行包元数据 `License-Expression: MIT`；`jsonschema-4.25.1.dist-info/licenses/COPYING` 包含 MIT 完整条款，版权主体为 Julian Berman（2013） |
| [rfc3986-validator](https://pypi.org/project/rfc3986-validator/0.1.1/) | 0.1.1 | MIT | 已安装发行包元数据 `License: MIT license` 及 MIT classifier；`rfc3986_validator-0.1.1.dist-info/LICENSE` 包含 MIT 完整条款，版权主体为 Nicolas Aimetti（2019） |

核对方式：在仅安装 requirements.txt 所需依赖的虚拟环境中，使用 Python 标准库 `importlib.metadata.distribution()` 检查上述版本的发行元数据及实际附带许可文件。两项直接依赖均为 MIT，与 LexRouter 自主原创代码的 MIT 授权未发现明显冲突；这不是对整个依赖树或所有第三方材料的全面法律审计。

Human Maintainer 已在 LR-P0-01A 中批准 LexRouter 自主原创代码采用根目录 [MIT License](../LICENSE)。此决定不将依赖或第三方 Skills、代码、数据集、法律文本及其他材料声明为 LexRouter 原创作品，也不改变其各自授权。使用、复制或分发时必须保留必要的版权与许可证声明；未确认授权的第三方内容不得直接复制入库。

当前通过包管理器安装依赖，不将依赖源码复制入库。后续新增、升级、打包或分发时，应复核相应版本及传递依赖的许可义务，保留发行包中必要的原始声明，并同步更新本记录。

LR-P0-02 未新增或升级依赖；候选校验复用现有 jsonschema、URI 格式检查和 Python 标准库。第三方候选不是运行时依赖，未将其源码或全文复制入库；各候选的版本、许可事实及未核实事项独立记录在 [发现候选区](../data/discovery/README.md)，不得将本表两项 MIT 依赖的结论扩展至候选材料。

LR-P0-05 未新增、升级或打包依赖，交接校验复用既有 Python 标准库/jsonschema。上游 Skill 依赖仅只读整理于[三个材料清单](reviews/README.md)，未安装为本仓库依赖；其许可不由本表推定。

LR-P1-02 不新增/升级 Python 或前端依赖，复用标准库和现有 jsonschema。真实签署验证调用 GitHub CLI 的只读 gh api；CI runner 自带 gh，本地由工程人员配置官方 CLI，不打包其源码。初始记录及合成测试可离线执行；GH_TOKEN 不进入记录/日志。

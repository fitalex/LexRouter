# Gate 2 兼容性与原件摘要

候选 `contract-review`；原 Draft PR #9 head `a7c7d9541e0f6b84a30d5643890de59ed4673a7b`；已接受 main `d1c7ebabd5c33d2e92c6916804adc4018c89e5a0`。

适配使用普通双亲合并提交接入 main，再追加 v2 sidecar；不重排已有提交，不 force-push，不改 v1 原件或 start 历史。原 Review ID 与上游版本保持一致。

固定源 revision `f73f92b6341ef4e9f1765434bf348b1acb4fb1d3` 的全部 31 个叶子项，已从 GitHub API重新读取完整 tree，与 accepted manifest 的路径、blob、mode/type逐项一致，响应未截断。原 Git tree（含排除项）保持不变；本轮不执行上游代码、不复制第三方全文。

以下28个case文件在该PR适配前逐字节备份，摘要映射 SHA256 为 `2d94697f2243f79e9410c812fb39b1262b3b86dcc9ee870ce720c6511e588596`。包括本轮case的原分配record、人工作业表、原始矩阵、证据及其它case原件；适配后以同一映射验证。无真人专业签署，不把start历史认作专业通过。

可重跑的比对数据（只含公开路径与摘要）：

```json
{
  "original_pr_head": "a7c7d9541e0f6b84a30d5643890de59ed4673a7b",
  "main": "d1c7ebabd5c33d2e92c6916804adc4018c89e5a0",
  "original_files": [
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/evidence.md",
      "git_blob": "debfda51a8f5e7e0deeb26085ffb580807339e48",
      "sha256": "eeb3863115f01959e073fe40ae62a764e9cbd432a237b487cff5e62676663c21"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/generated.json",
      "git_blob": "163aebc9ef99a93e8327b37417ac9ccec42a67aa",
      "sha256": "98f0449c78064a3a6584a3cf4fadab6bf44840e7148f7f378755b8b387c55ef3"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/inventory.json",
      "git_blob": "b99b06b6fa4b3db53a4310d557c78f9b4383b3db",
      "sha256": "08310a3b045d51756f68abca14f23cb69b019a3805e3f860f18ec1df542c4b0e"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/matrix.md",
      "git_blob": "95c3162de85096b925ad978f36090ac2e9317af4",
      "sha256": "2edbc8165e8c52fe346bcec8681626199fe462984f817f3d85bab082a35234a4"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/packet.md",
      "git_blob": "32dd9540b776970ffd3d7d20f6095d65fd0bcf93",
      "sha256": "024bcac7e933bf97846d3c2a9dbba52db3ffa1ceda87455fc1df83ea3d3e4e73"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/record.json",
      "git_blob": "c543f8ba4dc5dae3df1fb13512f3bf0dcee6c686",
      "sha256": "ec991cfa87ede63bb64d7180956d8a51330aef3a940e4c1d333f632e301331a8"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/subject.json",
      "git_blob": "294098da2eea657c5ad3065bcb6a4c4600814a71",
      "sha256": "a4fc8d81881d5c5f389c48160762aae17abe98a70db9d06df0486ce68fb5a164"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/templates.json",
      "git_blob": "8e11042db106037935db20464ad593ad3f19f22d",
      "sha256": "896bbd093e303607c01b890c1bc88f79add3396352039230ace762849ff37823"
    },
    {
      "path": "data/reviews/cases/RV-20261017-china-legal-counsel/workbook.md",
      "git_blob": "85a088eba3f4c09923c4ca07458ab7d7f6f54b06",
      "sha256": "ff95c3e6c281e20a4f2504b75dd55b1b00736cee9c47ad9f9df5e856d297ff76"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/evidence.md",
      "git_blob": "30a678ae94e533e66e43e2085f8b79334a882519",
      "sha256": "1c25f01f3dc03b4e20e44796de4c0ec11550faab2ed086b03923e08e80e2fa85"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/generated.json",
      "git_blob": "7107d1c9c7fcc9b8bae820207726c6c2e8507b04",
      "sha256": "ea457ea049f0effb6be0ed6f48b675cdde60fe115279724d6033c23075ebb0e7"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/inventory.json",
      "git_blob": "6b34e589d84576f6f7704d8ccb73230482d6a2d6",
      "sha256": "3366efdc0ec544b3618477fb18b70d8d31db57613ed23c06a67f4ab8c7029bff"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/matrix.md",
      "git_blob": "1db8708058defbc7cf16731fbc59ba0b91939cdc",
      "sha256": "4e397b95ac6c2ecfd6c3f4a6d94e06605083f2ff523a599e6837141510d9524e"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/packet.md",
      "git_blob": "2a6aec532ad834fe320ad5ebf420672b6e852389",
      "sha256": "76c09d0cbf709e012903269b2d93136ae6def9f6ed034b9ba9cf5ee0ceea5b2e"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/record.json",
      "git_blob": "b66dcb315bd862de1557b48c99cc8742c16a810f",
      "sha256": "db03fb017086a6b572502c253015f4b9ff75254260a840b58998b44666d24bff"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/subject.json",
      "git_blob": "eb4b3a05e0b64de217ed2524a4bffa2d921c2a7b",
      "sha256": "0e372898b60459e6ac3f5530f14edf6fd4309be1899b17ab45a7251c7b586b8a"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/templates.json",
      "git_blob": "50aff2a9ad62b000ea562f0cade71f69ad158cb9",
      "sha256": "105aae8f066e766ba8e76452c651bc8ce0940b6ef86db485c92a5997599c2245"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review-zh/workbook.md",
      "git_blob": "c1164cfe877db4d4338c54cf3fb0e1660335d83f",
      "sha256": "d07cbc071b2e97f1a94c50b6b301343360b3450ef00effb35bfa0ddeb245ab88"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/evidence.md",
      "git_blob": "539bcc57e9957d30d4e616403fc6592a596454e4",
      "sha256": "673870a7ac876f1e514b8d2291f2cf31f2b5d1e54f9185aefa500f0421406b1b"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/generated.json",
      "git_blob": "6a0ac82f97e75a6e8d6a7e00199866131d3e53c1",
      "sha256": "f7fb16b5540de00f35719ca614aeb1dbd1e4c3ac12f423fbcfbccc87f0546a8c"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/human-review.md",
      "git_blob": "9997bc9843e252fab5f6daaa5b4ab5f392f23058",
      "sha256": "c31050d05b0625125a8bc31eba5b72b1db130f197c501208fef99daaf4bb8207"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/inventory.json",
      "git_blob": "ec17831f5eca745cb22bf45c4f22014cbcbe1c1c",
      "sha256": "d85149f120972ca1b9461d6bc9ab041fb2be3d6a6be7ff6323bd37c14dd09c65"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/matrix.md",
      "git_blob": "e373f15bd50bb488cfce313a231e83c908ef5c9b",
      "sha256": "e7906dd52adcb145eb28d8cfc6cf0f9d37cdefa94fed9a8966ebc3c4bfbc3123"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/packet.md",
      "git_blob": "64837da745326e5e7562d1d77ea76e67562c9f18",
      "sha256": "a324392a3da5c95d7e225878e89486107f2d4eecba6ce28c511864fb616c3dff"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/record.json",
      "git_blob": "c2dc96234d315359e6f61a3d61df13ec3e1dcd78",
      "sha256": "e5cf8cb463ff767e687b6d24ec416a4d0d10c085a50e62aa407db469aeae3fdd"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/subject.json",
      "git_blob": "831a6c4e242761296192ff4245e53f0a53d5cba9",
      "sha256": "d3fd158e502a4db212d6302030d776296bb6694cfa251187aa784e398a5eb346"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/templates.json",
      "git_blob": "285b323758b63504db4793446a96a4235f72107b",
      "sha256": "28d06cfd7d4e439791ffe3c9e92f9fa8a6e34682ec3c1e70f103fd5125c30b37"
    },
    {
      "path": "data/reviews/cases/RV-20261017-contract-review/workbook.md",
      "git_blob": "999e0739e94bb42a4c92c6de5e6e54032f941884",
      "sha256": "64e4dba20ff145d5791043b022b8709583fac65a3289ecb4d3489553cfdb0de4"
    }
  ]
}
```

`credential_refs` 保持 main 的空表。未知授权、事实、法源适用、法规时效及运行条件仍为阻塞，不用兼容适配解除。新增不适用理由必须逐文件逐检查项留证；未作任何实际不适用专业决定。

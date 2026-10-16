# LexRouter 开源项目路线图（V3.3）

LexRouter Open-Source Project Roadmap

* 文档状态：V3.3 正式版（Active）
* 更新日期：2026-10-15
* 项目定位：面向法律行业的 AI 能力发现（Discovery）、测评（Evaluation）与路由（Routing）基础设施
* 开源策略：单一主仓库（Monorepo） · 静态优先（Static-First） · 证据可溯源（Traceable）

---

## 01｜核心愿景与产品边界

LexRouter 旨在建立开放、透明、抗幻觉的法律 AI 能力标准，解决法律实务中 AI 工具“能力黑盒、变量混杂、法域与新旧法时效错配”的选型痛点。

四条刚性边界（Guardrails）：

1. 控制变量归因：严格剥离技能（Skill）、数据（Data）与模型（Model），每次测评仅放开单一变量。
2. 法律专业红线：强制标注法域（默认中国大陆 CN-Mainland）与法规生效时间锚点；虚构法条或引用已废止旧法实行一票否决（0 分）。
3. 合规与免责底线：测试集真实卷宗必须完成主体与敏感金额脱敏；全站明确声明**“测评与路由结果仅供技术选型参考，不构成执业法律意见”**。
4. 有所不为（Non-Goals）：不面向 C 端当事人提供法律咨询、不做重度律所 SaaS 系统、Phase 1 仅做静态选型路由（推荐 + 配置导出/CLI），不做实时流量代理网关。

---

## 02｜三阶段演进路线

| 阶段 | 模块名称 | 核心对象 | 核心目标 | 启动状态 |
| --- | --- | --- | --- | --- |
| Phase 1 | Lex-Skill-Router | 法律工作流与规则 (Skills / Rules / Prompts) | 整合原 Awesome-LegalSkills-CN，固定标准底座模型，评测并推荐最优法律实务工作流 | 进行中 (2026.10.15 - 11.25) |
| Phase 2 | Lex-Data-Router | 法律数据与工具 (法规/案例 API、MCP) | 固定底座与指令，评测外部法律数据源的权威度、召回率与新法更新延迟 | 待触发 (Phase 1 验收后启动) |
| Phase 3 | Lex-Model-Router | 通用与垂直大模型 (LLMs) | 固定黄金测试集，评测底层模型的原生法理推理能力、幻觉率与 Token 性价比 | 待触发 (前两阶段成熟后启动) |

---

## 03｜Phase 1：Lex-Skill-Router 核心交付（当前聚焦）

围绕中文法律高频场景（合同审查、民商事诉讼、公司并购、企业合规、刑事/行政、法律检索），交付三大核心模块：

1. Discovery（结构化目录）：收录并标准化首批核心法律 Skills，统一标注法域、业务域、法规时效基准日与运行载体（Claude/Codex Skills、Cursor Rules、Dify 工作流等）。
2. Evaluation（控制变量测评与四类榜单）：
    * 标准试验台：锁定统一底座模型与参数运行所有参评 Skills。
    * 明暗集隔离：测试集拆分为公开自测集（Public）与盲测保留集（Holdout），防止刷榜过拟合；每次评分公开完整运行快照（Run Artifacts）供复现。
    * 四类榜单：综合能力总榜、垂直业务专项榜、Token 性价比榜、社区热门榜。
3. Routing（静态路由与 Skills Hub 站点）：上线静态 Web 站点，支持按案件特征匹配推荐 Top Skills、查看真实输入输出 Diff 溯源证据，并提供一键复制或 CLI 安装。

---

## 04｜Phase 1：42 天冲刺里程碑（2026-10-15 至 2026-11-25）

| 里程碑 | 周期 | 核心交付物 | 验收标准（DoD） |
| --- | --- | --- | --- |
| P0：仓库与规范 | Day 1 - 5 (10.15 - 10.19) | Monorepo 骨架、能力元数据 Schema、控制变量测评协议 | GitHub Actions 可自动校验提交的 Skill 元数据必填字段 |
| P1：目录整合 | Day 6 - 14 (10.20 - 10.28) | 整合 Awesome-LegalSkills-CN，首批 30~50 个法律 Skills 结构化入库 | 100% 入库 Skills 补齐法域、业务分类与法规时效锚点 |
| P2：基准与引擎 | Day 15 - 26 (10.29 - 11.09) | 脱敏黄金测试集（Public + Holdout）、自动化评测执行脚本 | 单条命令可跑通固定底座模型评测并输出完整溯源快照 |
| P3：榜单与校准 | Day 27 - 34 (11.10 - 11.17) | 人类法律专家盲测校准、首批四类排行榜与深度测评报告 | 机器评分与专家评分高度一致（相关系数达标），全量分数可溯源 |
| P4：MVP 发布 | Day 35 - 42 (11.18 - 11.25) | Skills Hub 静态网站、静态选型推荐器、LexRouter V1.0 发布 | 用户可在 30 秒内完成“场景选型 → 查验评测证据 → 一键获取”闭环 |

---

## 05｜协同规范与关联文档

本项目采用人类专家把关（Legal-in-the-Loop）与多 AI Agents（ChatGPT / Gemini / Codex）协同开发模式，实施细节拆分至以下独立文档维护：

* 架构与 AI 协同规范：AGENTS.md
* 能力元数据标准：docs/SCHEMA.md
* 控制变量测评协议：docs/EVAL_PROTOCOL.md
* 案件脱敏与合规指南：docs/ANONYMIZATION.md
* 每日开发任务书：docs/daily-specs/

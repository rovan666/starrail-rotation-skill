---
name: starrail-rotation-skill
description: 崩坏：星穹铁道（Honkai: Star Rail）战斗模拟与排轴教练。当用户提供自己的角色养成情况（box、面板、光锥、遗器、星魂）和敌人/关卡信息（怪物弱点、波次、轮次限制），要求模拟整场战斗过程、给出接近最优的行动轴（排轴/配速）、终结技插队时机、战技点分配与角色养成建议时使用。触发词示例：「排轴」「模拟战斗」「帮我打这关」「忘却之庭怎么满星」「0T 怎么排」「我的阵容怎么配速」「养成建议」「模拟宇宙/虚构叙事/末日幻影攻略」。用户用自然语言描述队伍和敌人、希望得到完整战斗推演与打法的场景首选本技能。
---

# 星穹铁道排轴教练（starrail-rotation-skill）

定位：**不是计算器，是教练**。用户只说"我有什么、对面是什么、目标是什么"，你负责理解、模拟、排轴并解释每个决策的原因。遗器词条级优化不在本技能范围——遇到"哪件遗器更好/毕业面板"类问题，建议用户使用 Fribbels HSR Optimizer 等专用工具。

## 核心工作流（四步）

### 第一步：收集信息

向用户收集（缺失的主动追问，已给的不要重复问）：

- **角色**：每个上场角色的名称、星魂数、等级/行迹概况、光锥（含叠影）、遗器套装与关键面板值。必须拿到：**速度、暴击率/暴伤、攻击%、效果命中、击破特攻、能量恢复效率**。
- **敌人**：名称或弱点属性、韧性条长度、血量量级、波次结构、特殊机制（蓄力、召唤、锁弱点、转面）。
- **目标**：满星通关 / 压轮次 / 0T。目标决定排轴激进程度。

用户给的信息不全时：先按合理默认假设推进，并在报告中明确标注假设项；关键假设（如速度值）必须追问。

### 第二步：准备数据

1. 查 `data/characters/` 与 `data/enemies/` 下是否已有相关角色的**排轴数据**（削韧、回能、buff 持续等）。数据文件格式见 [references/data-format.md](references/data-format.md)。
2. 缺失时按 [references/data-format.md](references/data-format.md) 的指引从上游数据仓库（Mar-7th/StarRailRes）补齐：优先运行 `python scripts/sync_data.py` 拉取原始数据并生成角色数据骨架，再人工/检索补全排轴相关字段。
3. 数值必须与当前游戏版本一致：对不确定的倍率、回能、削韧值，**先用 WebSearch 核实官方/社区最新数据再进模拟**，禁止凭记忆给关键数值。

### 第三步：模拟战斗

严格按 [references/simulation-workflow.md](references/simulation-workflow.md) 的模拟协议执行：行动条推演 → 逐动记录（削韧/能量/战技点/buff）→ 弱点破韧时机 → 终结技插点位。伤害按期望值计算（见 references/combat-mechanics.md 的公式），暴击随机性只影响伤害不影响轴。

### 第四步：输出报告

按 [references/output-templates.md](references/output-templates.md) 的模板输出：**结论先行**（能不能达成目标、几轮打完）→ 行动轴总览表 → 逐动明细 → 关键决策解释 → 养成建议 → 假设与风险。

## 硬规则

- 排轴结论必须能复现：每个行动在行动值时间轴上有明确位置，速度阈值可推导（公式见 references/combat-mechanics.md）。
- 战技点收支必须逐动对账，任何一动手动检查是否有点可用；不够就调整产点位，禁止"假设有 6 点上限"之类的硬凑。
- buff/debuff 的持续回合按"持有者回合数"结算，挂 buff 的时机要能吃满主 C 爆发窗口。
- 敌人有韧性条减伤（10%）与击破后的 +10% 易伤，破韧时机是排轴的核心变量，必须显式规划。
- 输出伤害为期望值；报告末尾列出对结果敏感的随机项（暴击、效果命中抵抗）。

## 资源导航

- 机制公式（行动值、削韧、伤害、回能、速度阈值表）：[references/combat-mechanics.md](references/combat-mechanics.md)
- 模拟协议（状态定义、回合循环、校验点）：[references/simulation-workflow.md](references/simulation-workflow.md)
- 数据文件格式与上游同步：[references/data-format.md](references/data-format.md)
- 报告模板与话术：[references/output-templates.md](references/output-templates.md)
- 数据脚本：`scripts/sync_data.py`（拉取上游数据）、`scripts/validate_data.py`（数据文件校验）

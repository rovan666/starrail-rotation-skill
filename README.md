# starrail-rotation-skill · 星穹铁道排轴教练

一个 [Kimi](https://www.kimi.com/) 技能：用自然语言描述你的角色养成和关卡敌人，AI 帮你**完整模拟战斗过程**，给出接近最优的**行动轴（排轴）**、终结技插队时机、战技点分配和**养成建议**。

定位一句话：**不是计算器，是教练**。现有工具（如 [Fribbels HSR Optimizer](https://github.com/fribbels/hsr-optimizer)、网页排轴器）需要你手动填表、自己理解数字；本技能负责策略——你只说"我有什么、对面是什么"，它负责模拟、排轴并解释每一步为什么。

## 使用方式（示例）

> 你：我有一队流萤 0+1、阮·梅 0+0、同谐主满魂、加拉赫满魂，流萤 154 速，打忘却之庭这期的萨姆，弱点量子雷虚数，帮我排轴满星。
>
> 技能：（读取 `data/characters/流萤.yaml` 等数据 → 按 `references/simulation-workflow.md` 模拟整场战斗 → 输出行动轴总览、逐动明细、关键决策解释、养成建议）

## 仓库结构

```
├── SKILL.md                  # 技能主文档（触发描述 + 四步工作流）
├── references/
│   ├── combat-mechanics.md   # 机制公式：行动值/削韧/伤害/回能/速度阈值表
│   ├── simulation-workflow.md# 模拟协议：状态定义、回合循环、校验点
│   ├── data-format.md        # 数据文件格式 + 版本更新流程
│   └── output-templates.md   # 报告模板与话术规范
├── data/
│   ├── characters/           # 排轴角色数据（YAML，示例：流萤）
│   ├── enemies/              # 敌人数据（YAML，示例：萨姆）
│   └── upstream/             # 上游原始 JSON（git 忽略，脚本拉取）
└── scripts/
    ├── sync_data.py          # 从 Mar-7th/StarRailRes 拉取数据/生成角色骨架
    └── validate_data.py      # 数据文件校验
```

## 版本更新流程（约 42 天一个版本）

```bash
python scripts/sync_data.py                 # 1. 拉取最新上游数据
python scripts/sync_data.py --character 新角色 # 2. 生成新角色骨架
# 3. 人工核对补全 TODO 字段（倍率/削韧/回能）
python scripts/validate_data.py             # 4. 校验
```

上游数据源：[Mar-7th/StarRailRes](https://github.com/Mar-7th/StarRailRes)（开源结构化游戏数据，数据源 Dimbreath/StarRailData）。敌人数据上游覆盖不全，以社区 wiki + 实测为准。

## 边界

- ✅ 战斗模拟、行动轴、配速、破韧规划、养成方向建议
- ❌ 遗器词条级最优解 → 请用 [Fribbels HSR Optimizer](https://fribbels.github.io/hsr-optimizer/)
- ❌ 手动微调行动值时间轴 → 网页排轴工具更适合

## 安装

将整个仓库作为 Kimi 技能目录加载（`SKILL.md` 位于仓库根目录）。详见 Kimi 技能的安装文档。

## 许可证与免责声明

[MIT](LICENSE)。本项目为非官方粉丝工具，游戏数据版权归米哈游所有，数据来源于公开社区仓库，仅供学习交流。

---

# starrail-rotation-skill (English)

A [Kimi](https://www.kimi.com/) skill that acts as a **battle coach** for Honkai: Star Rail: describe your roster and the enemy stage in natural language, and it simulates the full battle — turn order, weakness breaks, energy and skill-point economy — then produces a near-optimal action rotation with explanations and build advice.

- Not a relic optimizer → use [Fribbels HSR Optimizer](https://github.com/fribbels/hsr-optimizer) for that.
- Game data is synced from the open-source repo [Mar-7th/StarRailRes](https://github.com/Mar-7th/StarRailRes); run `python scripts/sync_data.py` after each game patch.
- MIT licensed. Unofficial fan project; game data belongs to HoYoverse.

# 数据文件格式与上游同步

本技能的数值分两层：

- **上游原始数据**：来自开源仓库 [Mar-7th/StarRailRes](https://github.com/Mar-7th/StarRailRes)（数据源 Dimbreath/StarRailData），含角色/光锥/遗器/技能全量 JSON。通过 `scripts/sync_data.py` 拉取到 `data/upstream/`。
- **排轴派生数据**：`data/characters/*.yaml`、`data/enemies/*.yaml`，从上游提取排轴必需字段并人工校对，是本技能模拟时直接读取的文件。

版本更新（约 42 天/版本）时的更新流程：

1. 运行 `python scripts/sync_data.py` 拉取最新上游索引。
2. 对新角色运行 `python scripts/sync_data.py --character <游戏内ID或名称>` 生成数据骨架。
3. 用 WebSearch 核对技能倍率/回能/削韧（上游 JSON 的文本为参数化模板，排轴字段必须人工确认），补全 YAML。
4. 运行 `python scripts/validate_data.py` 校验全部数据文件。

## 角色数据文件（data/characters/<名称>.yaml）

```yaml
id: 1310                  # 游戏内角色 ID（与上游一致）
name: 流萤
name_en: Firefly
version: "2.3"            # 首次登场版本
element: 火               # 物理/火/雷/冰/风/虚数/量子
path: 毁灭                # 毁灭/巡猎/智识/同谐/虚无/存护/丰饶
base_speed: 104           # 基础速度（1 级面板，无遗器）
energy_max: 240           # 终结技能量上限
skill_points:             # 战技点特例（默认普攻+1/战技-1）
  basic_gain: 1
  skill_cost: 0           # 该角色战技不耗点时标注 0
energy:                   # 各技能回能（默认 basic 20 / skill 30 / ult 5）
  basic: 20
  skill: 0                # 流萤战技不回能
  ult: 5
skills:
  basic:
    type: 单攻            # 单攻/群攻/扩散/弹射/辅助/治疗/护盾
    scaling: 攻击         # 攻击/生命/防御
    multiplier: 1.0       # 倍率（100% = 1.0），可写表达式如 "2.0+0.2*强化等级"
    toughness: 1          # 削韧基础值（对每个命中目标）
  skill:
    type: 扩散
    multiplier: "3.0 主目标 / 1.2 相邻"
    toughness: "2 主 / 1 相邻"
  ult:
    type: 变身            # 特殊机制类型，见 ult_mode
    toughness: 0
ult_mode: 变身            # 充能型(默认)/激活型/特殊（流萤类）
talent:                   # 天赋与排轴相关的核心效果，文字简述
  - "进入强化状态：速度+60，攻击+72%，强化战技耗点 0"
buffs:                    # 我方 buff，排轴关心持续时间与效果
  - name: 强化状态
    duration: 3           # 持有者回合数
    effect: "速度+60，攻击+72%"
    granted_by: ult
eidolons:                 # 影响排轴的星魂（只列关键魂）
  1: "强化战技削韧效率+50%"
  2: "击破后再动"
notes: "来源：版本 2.3 实测+社区核对"
```

必填字段：`id, name, element, path, base_speed, energy_max, skills（basic/skill/ult 至少一项的 toughness 与回能）`。其余按需补充。

## 敌人数据文件（data/enemies/<名称>.yaml）

```yaml
name: 萨姆（完整）
type: boss                # 小怪/精英/boss
version: "2.3"            # 数据所对应的游戏版本
speed: 158.4
toughness: 160            # 主韧性条（多个部位分别列出）
weakness: [虚数, 雷, 量子]
mechanics:                # 行动模式与特殊机制，按顺序
  - "第 1 动：单体攻击"
  - "第 2 动：解除弱点并单体攻击，累计自烧血 5%"
resistance: { 物理: 0.2, 火: 0.2 }   # 非弱点抗性（默认 0.2）
phases: 1                 # 阶段数，转阶段机制另述
notes: "来源：忘却之庭 XX 层实测"
```

## 上游同步脚本

`scripts/sync_data.py`：

- 无参数：拉取 `index_new/cn/` 下全部索引 JSON 到 `data/upstream/`。
- `--character <ID或名称>`：生成/更新对应角色 YAML 骨架（自动填基础速度、能量上限、技能类型占位），排轴字段留空待补。
- 脚本只读上游仓库的 raw 文件，不需要任何凭据。

上游数据已覆盖：角色基础信息/星魂/技能/行迹/晋阶、光锥、遗器套装与主副词条组。敌人数据上游索引不完整，敌人 YAML 以社区 wiki + 实测为准。

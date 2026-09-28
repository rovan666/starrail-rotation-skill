#!/usr/bin/env python3
"""从 Mar-7th/StarRailRes 拉取上游数据并生成角色排轴数据骨架。

用法：
    python scripts/sync_data.py                 # 拉取全部索引 JSON 到 data/upstream/
    python scripts/sync_data.py --character 流萤 # 生成/更新单个角色 YAML 骨架

上游数据结构（已核对，2026-09）：
    characters.json         按 ID 索引：name/path/element/max_sp/ranks/skills
    character_skills.json   按技能 ID：type(Normal/Skill/Ultimate/Talent/Technique)/
                            effect(SingleAttack/Blast/AoE/Bounce/Enhance/...)/params
    character_promotions.json  按角色 ID：values[晋阶].spd.base 为基础速度
    paths.json / elements.json 代码到中文名的映射
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/index_new/cn"
INDEX_FILES = [
    "characters.json",
    "character_skills.json",
    "character_ranks.json",
    "character_promotions.json",
    "light_cones.json",
    "light_cone_ranks.json",
    "relics.json",
    "relic_sets.json",
    "paths.json",
    "elements.json",
    "properties.json",
]

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = ROOT / "data" / "upstream"
CHAR_DIR = ROOT / "data" / "characters"

SKILL_TYPE_MAP = {"Normal": "普攻", "BPSkill": "战技", "Ultra": "终结技",
                  "Talent": "天赋", "Maze": "秘技", "ElationDamage": "欢愉技"}
# 跳过地图普攻等战斗外技能；带 "11" 前缀的为重复形态（与后 6 位相同 ID 重复）
SKIP_TYPES = {"MazeNormal", ""}


def fetch(name: str) -> dict:
    url = f"{BASE}/{name}"
    print(f"  下载 {url}")
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def sync_upstream() -> None:
    UPSTREAM_DIR.mkdir(parents=True, exist_ok=True)
    for name in INDEX_FILES:
        data = fetch(name)
        (UPSTREAM_DIR / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  已保存 data/upstream/{name}（{len(data)} 条）")


def load_upstream() -> dict:
    return {n: json.load(open(UPSTREAM_DIR / n, encoding="utf-8"))
            for n in INDEX_FILES if (UPSTREAM_DIR / n).exists()}


def gen_character(query: str) -> Path:
    data = load_upstream()
    chars, skills, promos = data["characters.json"], data["character_skills.json"], \
        data["character_promotions.json"]
    paths, elements = data["paths.json"], data["elements.json"]

    char = None
    for c in chars.values():
        if query == c["id"] or query in (c.get("name"), c.get("name") or ""):
            char = c
            break
    if char is None:
        sys.exit(f"未找到角色：{query}（可先运行不带参数的命令拉取最新数据）")

    spd = promos[char["id"]]["values"][0]["spd"]["base"]

    def skill_block(slot: str, s: dict) -> str:
        # 上游 params 含溢出等级：普攻数组 10 级取 Lv6，战技/终结技/天赋 15 级取 Lv10
        params = s.get("params") or []
        idx = 5 if len(params) == 10 else 9 if len(params) >= 15 else len(params) - 1
        mult = params[idx][0] if params else None
        lines = [
            f"  {slot}:",
            f"    type: {s.get('effect_text', 'TODO')}",
            f"    multiplier: {mult if mult is not None else 'TODO'}   # 满级倍率",
            f"    toughness: TODO    # 削韧基础值，需人工核对（references/combat-mechanics.md 有默认表）",
            f"    desc: \"{s.get('desc', '')}\"",
        ]
        return "\n".join(lines)

    # 去重：跳过带 11 前缀的镜像形态 ID；同名槽位（如强化普攻）加后缀区分
    seen_suffix = set()
    slot_count: dict = {}
    skill_sections = []
    for sid in char["skills"]:
        suffix = sid[-6:]
        if suffix in seen_suffix:
            continue
        seen_suffix.add(suffix)
        s = skills.get(sid)
        if not s or s.get("type") in SKIP_TYPES or s.get("type") not in SKILL_TYPE_MAP:
            continue
        base = SKILL_TYPE_MAP[s["type"]]
        slot_count[base] = slot_count.get(base, 0) + 1
        slot = base if slot_count[base] == 1 else f"{base}_强化{slot_count[base] - 1 if slot_count[base] > 2 else ''}"
        skill_sections.append(skill_block(slot, s))

    name = char["name"]
    element = elements[char["element"]]["name"]
    path = paths[char["path"]]["name"]

    yaml_text = f"""# 排轴数据：{name}（骨架由 sync_data.py 生成，TODO 字段需人工核对后填写）
id: {char["id"]}
name: {name}
element: {element}
path: {path}
rarity: {char["rarity"]}
base_speed: {spd}
energy_max: {char["max_sp"]}
skill_points:
  basic_gain: 1
  skill_cost: 1
energy:
  basic: 20
  skill: 30
  ult: 5
skills:
{chr(10).join(skill_sections)}
talent: []
buffs: []
eidolons: {{}}
version: TODO
notes: TODO（来源与核对日期）
"""
    CHAR_DIR.mkdir(parents=True, exist_ok=True)
    out = CHAR_DIR / f"{name}.yaml"
    out.write_text(yaml_text, encoding="utf-8")
    print(f"  已生成 {out}（TODO 字段待人工补全）")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--character", help="游戏内角色名或 ID，生成排轴数据骨架")
    args = ap.parse_args()
    if args.character:
        print(f"生成角色骨架：{args.character}")
        gen_character(args.character)
    else:
        print("同步上游数据...")
        sync_upstream()


if __name__ == "__main__":
    main()

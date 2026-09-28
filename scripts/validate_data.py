#!/usr/bin/env python3
"""校验 data/characters/ 与 data/enemies/ 下的 YAML 数据文件。

用法：
    python scripts/validate_data.py            # 校验全部
    python scripts/validate_data.py 流萤        # 校验单个角色

规则见 references/data-format.md。退出码 0 = 全部通过，1 = 存在错误。
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHAR_REQUIRED = ["id", "name", "element", "path", "base_speed", "energy_max", "skills"]
ENEMY_REQUIRED = ["name", "speed", "toughness", "weakness"]
ELEMENTS = {"物理", "火", "雷", "冰", "风", "虚数", "量子"}


def check_file(path: Path, required: list, is_char: bool) -> list:
    errors = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"{path.name}: YAML 解析失败：{e}"]
    if not isinstance(doc, dict):
        return [f"{path.name}: 顶层必须是 mapping"]
    for field in required:
        if field not in doc:
            errors.append(f"{path.name}: 缺少必填字段 {field}")
    if is_char and "element" in doc and doc["element"] not in ELEMENTS:
        errors.append(f"{path.name}: element={doc['element']} 不在七属性内")
    if is_char and "skills" in doc and isinstance(doc["skills"], dict):
        for slot, sk in doc["skills"].items():
            if isinstance(sk, dict) and "TODO" in str(sk.get("toughness", "")):
                errors.append(f"{path.name}: skills.{slot}.toughness 仍为 TODO（需人工核对）")
    if not is_char and "version" not in doc:
        errors.append(f"{path.name}: 缺少 version 字段（数据版本追踪）")
    return errors


def main() -> None:
    args = sys.argv[1:]
    char_dir, enemy_dir = ROOT / "data" / "characters", ROOT / "data" / "enemies"
    char_files = sorted(char_dir.glob("*.yaml")) if char_dir.exists() else []
    enemy_files = sorted(enemy_dir.glob("*.yaml")) if enemy_dir.exists() else []

    if args:
        char_files = [f for f in char_files if args[0] in f.stem]
        enemy_files = [f for f in enemy_files if args[0] in f.stem]

    all_errors = []
    for f in char_files:
        all_errors += check_file(f, CHAR_REQUIRED, True)
    for f in enemy_files:
        all_errors += check_file(f, ENEMY_REQUIRED, False)

    checked = len(char_files) + len(enemy_files)
    if all_errors:
        print(f"校验失败（{checked} 个文件，{len(all_errors)} 个问题）：")
        for e in all_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print(f"校验通过：{checked} 个数据文件。")


if __name__ == "__main__":
    main()

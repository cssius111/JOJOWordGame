from gpt_logic import (
    generate_stand_description,
    generate_stand_description_simple,
    generate_stand_stats,
)
from stand_utils import modify_description, parse_stats
from player_utils import generate_player_physical
from encounter_engine import generate_encounter
from battle_system import stat_to_value
from turn_engine import run_battle_loop

import random
import time
import threading


def clean_input(text):
    return text.encode("utf-8", "ignore").decode("utf-8").strip()

# 替换并增强 smart_edit，使其支持查看原文、插入、删除、替换操作

def smart_edit(text):
    """
    允许玩家选择：查看原文 / 替换 / 删除 / 插入 一个字，并持续修改，直到确认
    """
    original_text = text
    print(f"\n📖 当前能力描述：\n{text}")

    while True:
        print("\n你可以执行以下操作：")
        print("1. 替换一个字（原字 → 新字）")
        print("2. 删除一个字（输入原字）")
        print("3. 插入一个字（在某个字前插入新字）")
        print("4. 查看当前描述")
        print("5. 完成修改并继续游戏")

        choice = input("✏️ 请输入选项编号（1-5）：").strip()

        if choice == "1":
            old_char = input("🔁 要替换哪个字：").strip()
            new_char = input("🆕 替换成什么字：").strip()
            if old_char in text:
                idx = text.index(old_char)
                text = text[:idx] + new_char + text[idx + 1:]
                print(f"✅ 替换成功！\n{text}")
            else:
                print("❌ 输入的字不在描述中。")

        elif choice == "2":
            target_char = input("❌ 要删除哪个字：").strip()
            if target_char in text:
                idx = text.index(target_char)
                text = text[:idx] + text[idx + 1:]
                print(f"✅ 删除成功！\n{text}")
            else:
                print("❌ 输入的字不在描述中。")

        elif choice == "3":
            before_char = input("🧩 想在哪个字前插入新字：").strip()
            insert_char = input("🔠 插入哪个字：").strip()
            if before_char in text:
                idx = text.index(before_char)
                text = text[:idx] + insert_char + text[idx:]
                print(f"✅ 插入成功！\n{text}")
            else:
                print("❌ 输入的字不在描述中。")

        elif choice == "4":
            print(f"\n📖 当前描述：\n{text}")

        elif choice == "5":
            print(f"\n✅ 修改完成：\n「{text}」")
            return text

        else:
            print("⚠️ 无效输入，请选择 1-5。")




def main():
    stand_result = {"desc": None}

    def gpt_background_task():
        print("请选择替身生成风格：")
        print("1. 普通清晰型（适合互动与改字）")
        print("2. 创意灵感型（多段能力 + 灵感扰动）")
        choice = input("请输入 1 或 2：").strip()
        if choice == "1":
            stand_result["desc"] = generate_stand_description_simple()
        else:
            stand_result["desc"] = generate_stand_description()

    # 异步生成替身
    thread = threading.Thread(target=gpt_background_task)
    thread.start()

    # 加载动画
    print("🎮 欢迎来到 JOJO 替身文字战斗系统")
    print("请耐心等待...")
    time.sleep(2)
    print("替身生成中...")
    time.sleep(3)
    print("灵魂灌注入身体...")
    time.sleep(2)
    print("白蛇正在重制你的记忆...")
    time.sleep(3)
    print("黑蚊子豆正在撰写你的记录日志...")

    thread.join()
    stand_data = stand_result["desc"]
    if not stand_data:
        print("❌ 替身生成失败，可能是 API 错误或网络异常。")
        return

    ability_text = stand_data["ability"]
    print(f"\n🌀 替身名：『{stand_data['name']}』")
    print(f"📖 替身能力：{ability_text}")
    print(f"🗣️ 名言：「{stand_data['quote']}」")

    # 玩家修改能力描述
    edited_desc = smart_edit(ability_text)
    if not modify_description(ability_text, edited_desc):
        print("❌ 修改超过一个字，不合法！游戏失败。")
        return

    # 六维属性生成
    raw_stats = generate_stand_stats(edited_desc)
    player_stand_stats = parse_stats(raw_stats)
    if len(player_stand_stats) < 6:
        print("⚠️ 替身能力解析失败，六维属性不足。请检查描述格式。")
        return

    # 生成玩家身体属性
    player_body = generate_player_physical()
    print("\n🧍‍♂️ 你的替身属性：", player_stand_stats)
    print("🩺 你的身体属性：", player_body)

    # 敌人替身生成
    enemy_stand = generate_stand_description()

    # 遭遇信息生成
    encounter = generate_encounter()
    scene = encounter["scene"]
    attitude = encounter["enemy_attitude"]

    # ⚔️ 启动 GPT 回合制战斗系统
    run_battle_loop(
        player_stand={
            "name": stand_data["name"],
            "ability": edited_desc,
            "quote": stand_data["quote"]
        },
        enemy_stand={
            "name": enemy_stand["name"],
            "ability": enemy_stand["ability"],
            "quote": enemy_stand["quote"]
        },
        scene=scene,
        attitude=attitude
    )


if __name__ == "__main__":
    main()

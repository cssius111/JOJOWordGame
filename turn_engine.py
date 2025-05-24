from battle_judge import gpt_judge_turn
from battle_state import initialize_battle_state

def run_battle_loop(player_stand, enemy_stand, scene, attitude):
    state = initialize_battle_state(player_stand, enemy_stand, scene, attitude)

    print(f"\n🌍 场景：{scene}")
    print(f"🎭 敌人态度：{attitude}")
    print(f"\n🧍 你的替身：『{player_stand['name']}』")
    print(f"📖 能力：{player_stand['ability']}")
    print(f"🎤 名言：{player_stand['quote']}")
    print(f"\n😈 敌人替身：『{enemy_stand['name']}』")
    print(f"📖 敌人能力：{enemy_stand['ability']}")
    print("⚔️ 战斗开始！\n")

    while True:
        print(f"\n🕓 当前回合：第 {state['turn']} 回合")
        print(f"你 HP：{state['player']['HP']}   敌人 HP：{state['enemy']['HP']}")
        action = input("📝 请输入你的行动：").strip()

        if not action:
            print("⚠️ 行动不能为空，请重新输入。")
            continue

        state['flags']['player_action'] = action
        result = gpt_judge_turn(state)

        print("\n📡 GPT 判定结果：")
        print(result)

        lines = result.splitlines()

        # 提取伤害数值并减少敌人 HP
        for line in lines:
            if "HP-" in line:
                import re
                match = re.search(r"HP-(\d+)", line)
                if match:
                    dmg = int(match.group(1))
                    state["enemy"]["HP"] = max(0, state["enemy"]["HP"] - dmg)
                    print(f"💥 敌人受到 {dmg} 点伤害，剩余 HP：{state['enemy']['HP']}")

        # 回合总结
        summary_line = next((line for line in lines if line.startswith("回合总结：")), "回合总结：无内容")
        state["log"].append(f"第{state['turn']}回合：{summary_line.replace('回合总结：', '')}")

        # 更安全的结束判断
        end_flag = next((line for line in lines if line.startswith("是否结束战斗：")), "")
        enemy_dead = next((line for line in lines if line.startswith("敌人是否死亡：")), "")

        if end_flag.strip().endswith("是") or enemy_dead.strip().endswith("是"):
            print("\n🏁 战斗结束。")
            break

        state["turn"] += 1

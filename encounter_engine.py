# 创建 encounter_engine.py v2，加入自由行为输入 + GPT 判定结构（mock）
import random


scene_pool = [
    "废弃游乐园", "下水道深处", "电车车厢", "校园屋顶", "便利店", "断桥边",
    "旧图书馆", "列车控制室", "沉没码头", "山间吊桥"
]

encounter_modes = [
    "突然出现", "尾随你多时", "主动打招呼", "悄无声息地注视你", "坐在你对面"
]

enemy_attitudes = ["友好", "中立", "敌意"]

def generate_encounter():
    return {
        "scene": random.choice(scene_pool),
        "encounter": random.choice(encounter_modes),
        "enemy_attitude": random.choice(enemy_attitudes)
    }

def mock_gpt_judge_action(action, ability, scene, attitude):
    keywords = ["攻击", "逃", "对话", "假装", "观察"]
    risky_words = ["掏出", "拔刀", "猛扑", "抢先", "冲刺"]
    if any(word in action for word in keywords + risky_words):
        if "梦" in ability or "记忆" in ability or "控制" in ability:
            return True, "敌人似乎陷入了你的能力构建的幻觉中，暂时失去了行动力。"
        if "攻击" in action and attitude == "敌意":
            return True, "你先发制人，对方被你的气势震慑住了。"
        if "逃" in action and attitude != "敌意":
            return True, "你悄悄溜走了，敌人并未追击。"
        return False, "对方警觉地盯着你，这种行为无法成功。"
    return False, "你的行为太含糊，无法判断是否合理。"

def run_encounter_loop(stand_ability_text):
    encounter = generate_encounter()
    print(f"\n📍 你现在在：{encounter['scene']}")
    print(f"🧍 遭遇方式：{encounter['encounter']}")
    print(f"😈 敌人态度：{encounter['enemy_attitude']}")

    while True:
        action = input("💬 你打算怎么做？\n> ").strip()
        if not action:
            print("⚠️ 行动不能为空，请重新输入。")
            continue
        ok, result = mock_gpt_judge_action(action, stand_ability_text, encounter["scene"], encounter["enemy_attitude"])
        print(f"\n🤖 GPT 判断：{result}")
        if ok:
            break

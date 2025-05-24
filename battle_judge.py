# 整合版 battle_judge.py：GPT驱动的战斗判定逻辑

from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.deepseek.com"
)
def clean_input(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

def gpt_judge_turn(state):
    scene = state["scene"]
    turn = state["turn"]
    player = state["player"]
    enemy = state["enemy"]
    flags = state["flags"]
    log = "\n".join(state["log"][-3:])  # 最近3条行为记录

    player_action = clean_input(flags.get("player_action", "无"))
    enemy_attitude = enemy.get("attitude", "未知")

    prompt = f"""
你是JOJO替身世界的战斗裁定AI。

⚠️ 输出规范要求（必须遵守）：
- 每一项都必须输出，不允许遗漏
- 如果有造成伤害，务必写出明确格式：HP-数字（如：HP-15），否则系统无法识别扣血
- 如果没有造成伤害，也请写：未造成 HP 伤害
- 不要输出多余的解释或换行格式，严格按以下6项输出

以下是当前战斗状态：
- 场景：{scene}
- 当前回合：第 {turn} 回合
- 玩家替身：『{player['stand']['name']}』
- 玩家能力：{player['stand']['ability']}
- 玩家状态：HP={player['HP']}，状态={player['status']}，LUCK={player['LUCK']}
- 敌人态度：{enemy_attitude}
- 敌人替身：『{enemy['stand']['name']}』
- 敌人能力：{enemy['stand']['ability']}
- 敌人状态：HP={enemy['HP']}，状态={enemy['status']}，LUCK={enemy['LUCK']}
- 历史行为记录（最后3条）：\n{log}

当前玩家的动作是：「{player_action}」

请你判断以下问题，并按格式作答：
1. 此行为是否成功？（是/否）
2. 是否对敌人造成实质性影响？（如伤害、压制、改变状态）
3. 敌人是否立即反击或做出反应？
4. 敌人是否死亡或失去战斗能力？
5. 战斗是否应该结束？
6. 请用简洁语言叙述这一回合的结果（1~2句话）

输出格式如下：

成功：是/否  
效果：简述影响  
敌人反应：简述或无  
敌人是否死亡：是/否  
是否结束战斗：是/否  
回合总结：xxxx
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=0.9,
            top_p=0.95,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ GPT 判定失败：{e}"


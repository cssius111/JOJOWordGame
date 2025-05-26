# 整合版 battle_judge.py：GPT驱动的战斗判定逻辑

from openai import OpenAI

client = OpenAI(
    api_key="sk-15e3638d218d4e448365fb53fe011db7",
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
    你是JOJO替身世界的战斗裁定AI，负责在每回合内，根据玩家与敌人的能力和行为判断战斗发展。你必须合理解释每个动作的效果，并确保系统能识别血量变化与敌人行为。

    📌 **指令行为处理说明：**
    - 玩家指令可能是攻击、防御、干扰、心理战、道具使用、交涉、奇怪行为（如烧烤、表演等）。请尝试赋予其战术意义（例如迷惑、拖延、挑衅、误导、奇袭等），不要直接判定为“无效”或“否”。
    - 敌人每回合必须有反应：攻击、防御、躲避、观察、反击、释放替身能力等，不能重复“无”。
    - 如果连续多回合未分胜负，敌人将尝试主动施压或发起强攻。
    - 如果行为造成伤害，**务必明确格式输出：HP-数字（如 HP-20），否则系统不会扣血**。
    - 如果没有造成伤害，也必须写明：“未造成 HP 伤害”。
    - 这是系统唯一识别血量的方式。你输出的“敌人死亡”不会自动生效，必须同时给出 HP-100伤害。

    🧠 当前战斗状态：
    - 场景：{scene}
    - 当前回合：第 {turn} 回合
    - 玩家替身：『{player['stand']['name']}』
    - 玩家能力（请以这个文本为准，完整理解其潜力与使用方式）：{player['stand']['ability']}
    请将玩家能力作为核心依据，充分利用其逻辑/隐喻/物理特性进行判断，避免只表面使用一个能力词汇。
    例子：如果能力涉及“千倍重量”，请思考其应用在武器、场景、敌人弱点上的物理后果。
    - 玩家状态：HP={player['HP']}，状态={player['status']}，LUCK={player['LUCK']}
    - 敌人态度：{enemy_attitude}
    - 敌人替身：『{enemy['stand']['name']}』
    - 敌人能力：{enemy['stand']['ability']}
    - 敌人状态：HP={enemy['HP']}，状态={enemy['status']}，LUCK={enemy['LUCK']}
    - 历史行为记录（最后3条）：\n{log}

    当前玩家的动作是：「{player_action}」
    请结合玩家替身能力，对该动作进行“能力驱动”的解释和推理，而不是仅凭字面意义判断。


    请严格按以下格式输出：
    1. 此行为是否成功？（是 / 否）
    2. 是否对敌人造成实质性影响？（如伤害、压制、改变状态）
    3. 敌人是否立即反击或做出反应？（不可空）
    4. 敌人是否死亡或失去战斗能力？（是 / 否）
    5. 战斗是否应该结束？（是 / 否）
    6. 回合总结：简洁描述整体发展（3～4句话）
    7. 若有伤害，务必额外列出：HP-数字伤害（如 HP-25 伤害）

    ✳️ 输出格式（每项必须出现）：

    成功：是/否  
    效果：xxxx  
    敌人反应：xxxx  
    敌人是否死亡：是/否  
    是否结束战斗：是/否  
    回合总结：xxxx  
    HP-xx伤害（如未造成伤害请写：未造成 HP 伤害）
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


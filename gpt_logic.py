import random
from openai import OpenAI

# 初始化 API 客户端
client = OpenAI(
    api_key="请替换成你自己的 API Key",  # 请替换成你自己的 API Key
    base_url="https://api.deepseek.com"
)

# 名称风格池
name_style = [
    "简短英文单词，比如 Punch、Burn、Hook",
    "动词+名词组合，比如 Break Line、Lock Step",
    "武器或工具名，比如 Blade、Siren、Screwdriver",
    "带攻击意图的拟声词，比如 Boom、Zap、Buzzkill",
    "数字与颜色组合，比如 Black Seven、Red Zone",
    "常见物品名，但听起来很酷，比如 Mirror、Switch、Sticker",
    "街头感强的词汇，比如 Dropkick、Tagout、Spinback",
    "和动作有关的短语，比如 Fast Draw、Blind Spot、Quick Trap",
    "略带中二但可理解的外语词汇，比如 Domino、Alarma、Crucifix",
    "和声音/视觉/触觉相关的词，比如 Glare、Echo、Flicker"
]


# 能力风格池（语气）
concept_style = [
    "像游戏技能一样一看就知道怎么用",
    "能力简单但有威胁，比如定身、燃烧、复制",
    "听起来是日常行为，但实际上很致命",
    "一句话能概括战斗用法，不要解释太多机制",
    "不是控制时间、空间，而是控制具体东西",
    "适合小范围近战，动作清晰，直觉上能理解",
    "强度可以高，但不能靠概念设定赢，必须有物理方式实现",
    "可以和现实物品互动，比如水、影子、声音、衣服",
    "最好有副作用，这样听起来更真实",
    "一读就能想象出来战斗场面，不需要思考"
]


inspiration = [
    "请设计一个在战斗中能立刻生效的能力，最好有物理或视觉表现。",
    "让这个替身适合在打架时用，能主动干扰或压制敌人。",
    "设计一个一听就知道怎么打人的能力。",
    "这个能力可以弱，但必须很明确，比如『碰到就打断动作』。",
    "这个替身一定要有『战斗用法』，不要是纯日常娱乐。",
    "试着让能力和环境互动，比如水、光、声音、温度、衣服等。",
    "设计一个能逼迫敌人做出反应的能力，比如恐惧、移动、闪避。",
    "加入一个副作用，比如每次使用后使用者也会流鼻血、变迟钝等。",
    "设想它在近距离混战中使用的效果。",
    "这个能力需要够直接，不要模糊，不要哲学，只要能打。"
]


def generate_stand_description():
    theme = random.choice(name_style)
    tone = random.choice(concept_style)
    inspire_hint = random.choice(inspiration)

    prompt = f"""
你是一位 JOJO 替身设计师，请你设计一个强一点的替身能力，可以参考jojo里面的替身，但是不要太多。

🧠 要求如下：
- 替身名字（风格：{theme}）
- 能力描述（风格：{tone}，（最多 2 句话，必须有明确用途或威胁，不能废））
- 加入这个创作灵感参考：{inspire_hint}
- 使用者名言（个性化、简洁、酷，但不需要解释）

✍️ 输出格式如下：

替身名：『xxxx』

能力：
能力：
第一句清楚描述核心能力。
第二句说明它带来的影响或结果（强调实际效果）。

"xxx"
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=1.2,       # 🔥 更高创造力
        top_p=0.95,            # 🔥 更开放采样
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        name_line = next(line for line in lines if line.startswith("替身名："))
        name = name_line.replace("替身名：", "").replace("『", "").replace("』", "").strip()

        # 找到“能力：”段落并提取多行能力描述
        ability_index = lines.index("能力：")
        quote_index = next((i for i, line in enumerate(lines) if line.startswith('"') and line.endswith('"')), None)
        ability_lines = lines[ability_index + 1: quote_index if quote_index is not None else len(lines)]
        ability = "\n".join(ability_lines).strip()  # ✅ 多行换行输出

        quote = lines[quote_index].strip('"') if quote_index is not None else "……"

    except Exception as e:
        print("⚠️ 无法解析替身内容，原始内容如下：")
        print(content)
        return {
            "raw": content,
            "name": "解析失败",
            "ability": "无法提取能力",
            "quote": "……"
        }

    return {
        "name": name,
        "ability": ability,
        "quote": quote,
        "raw": content
    }


def generate_stand_stats(description):
    """
    给定替身描述，生成六维属性（破坏力、速度、射程、持续力、精密性、成长性）
    """
    prompt = f"""
以下是一个JOJO风格的替身能力描述，请你为它生成六维属性。
只返回一行属性，格式如下：
破坏力: A 速度: B 射程: C 持续力: C 精密性: D 成长性: A

替身描述如下：
{description}
"""
    response = client.chat.completions.create(
        model="deepseek-chat",  # 或 gpt-4
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def generate_stand_description_simple():
    """
    更适合日常展示的简洁版本，能力为一句话，具体且可修改
    """
    prompt = """
请你以 JOJO 替身风格创作一个替身角色，要求如下：

1. 替身名（请放在『』中，风格可以是英文、情绪、或生活中的普通词汇）
2. 能力描述：只写一句话，具体、有逻辑、有生活感，不能玄学或太抽象。
   示例：他走过的地面在5秒后会变成镜面。
3. 一句角色台词（个性化、简洁、有趣、可中二）

格式如下：

替身名：『xxx』
能力：xxx（只一句）
台词："xxx"
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=1.1,
        top_p=0.9,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        lines = [line for line in content.splitlines() if line.strip()]
        name = lines[0].replace("替身名：", "").strip("『』")
        ability = lines[1].replace("能力：", "").strip()
        quote = lines[2].replace("台词：", "").strip('"')
    except Exception:
        return {
            "name": "未命名替身",
            "ability": "每次他看向镜子，镜子里的世界都会慢一秒。",
            "quote": "你先看到的是影子，不是我。",
            "raw": content
        }

    return {
        "name": name,
        "ability": ability,
        "quote": quote,
        "raw": content
    }

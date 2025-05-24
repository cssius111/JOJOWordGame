# player_utils.py
import random

def random_stat():
    """返回一个随机属性等级，S 极小概率"""
    roll = random.randint(1, 100)
    if roll <= 3:
        return 'S'
    elif roll <= 20:
        return 'B'
    elif roll <= 70:
        return 'C'
    else:
        return 'D'

def generate_player_physical():
    """生成玩家的身体属性"""
    return {
        "HP": random.randint(80, 120),
        "ATK": random.randint(10, 30),
        "DEF": random.randint(5, 20),
        "LUCK": random_stat()
    }

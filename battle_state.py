# 整合版 battle_state.py：用于初始化和存储完整战斗状态，包括 LUCK 随机化

import random

def random_luck():
    return random.choice(["A", "B", "C", "D", "E"])

def initialize_battle_state(player_stand, enemy_stand, scene, attitude):
    return {
        "scene": scene,
        "turn": 1,
        "log": [],
        "player": {
            "HP": 100,
            "ATK": 25,
            "DEF": 15,
            "LUCK": random_luck(),
            "stand": player_stand,  # dict: name, ability, quote
            "status": "正常",
        },
        "enemy": {
            "HP": 100,
            "ATK": 22,
            "DEF": 18,
            "LUCK": random_luck(),
            "stand": enemy_stand,
            "attitude": attitude,
            "status": "正常",
        },
        "flags": {
            "ambush": False,
            "player_action": None,
            "enemy_action": None,
        }
    }


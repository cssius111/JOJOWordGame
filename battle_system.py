# battle_system.py：保留基本工具函数，例如六维能力值转换

def stat_to_value(stat):
    return {
        "S": 70,
        "A": 50,
        "B": 35,
        "C": 25,
        "D": 15,
        "E": 5
    }.get(stat.upper(), 20)

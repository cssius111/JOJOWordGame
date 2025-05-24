import re

def modify_description(original, edited):
    """
    判断玩家是否只修改了一个字符（包括：删除、替换、添加）。
    """
    if original == edited:
        return True

    # 快速判断长度差异
    length_diff = abs(len(original) - len(edited))
    if length_diff > 1:
        return False

    # 如果长度一样，检查替换了几个字
    if len(original) == len(edited):
        diff_count = sum(1 for a, b in zip(original, edited) if a != b)
        return diff_count <= 1

    # 如果长度不一样，判断是添加还是删除一个字
    # 保证 shorter 是短字符串
    shorter, longer = (original, edited) if len(original) < len(edited) else (edited, original)
    for i in range(len(longer)):
        if shorter == longer[:i] + longer[i+1:]:
            return True
    return False

def parse_stats(raw_text):
    """
    从一段文本中提取 JOJO 替身的六维属性，返回一个字典。
    支持中英文冒号、换行、大小写混排。
    示例返回：
        {
            '破坏力': 'B',
            '速度': 'A',
            '射程': 'C',
            '持续力': 'B',
            '精密性': 'C',
            '成长性': 'D'
        }
    """
    pattern = r"(破坏力|速度|射程|持续力|精密性|成长性)[：:]\s*([A-E])"
    matches = re.findall(pattern, raw_text)
    return {k: v for k, v in matches}

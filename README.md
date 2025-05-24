# 🎮 JOJO 替身文字战斗系统

一个基于 GPT 驱动的 JOJO 风格文字游戏，你可以生成独特的替身、修改能力描述、遭遇敌人并通过 GPT 判定进行回合制战斗！

---

## ✨ 功能亮点

- 🌀 **替身能力生成**：从“日常细节”到“哲学隐喻”，创造你自己的替身能力。
- 🧠 **一字改命**：只允许修改一个字，改变能力的命运。
- 🎭 **动态遭遇系统**：每次战斗敌人不同，场景不同，态度也不同。
- ⚔️ **GPT 回合制战斗**：由 GPT 判断你行动是否成功、是否造成伤害，以及战斗是否结束。
- 📜 **战斗日志追踪**：每一回合的结果都会记录，形成完整的战斗叙述。

---

## 🧩 安装方式

### 🔗 克隆项目

```bash
git clone https://github.com/your-username/jojo-stand-battle.git
cd jojo-stand-battle
```

### 📦 安装依赖

```bash
pip install -r requirements.txt
```

或单独安装：

```bash
pip install openai
```

---

## 🔑 设置 API Key

请前往 [DeepSeek](https://deepseek.com) 或 [OpenAI](https://platform.openai.com) 获取 API Key，并在 `gpt_logic.py` 中设置你的 `api_key`：

```python
client = OpenAI(
    api_key="sk-你的APIKEY",
    base_url="https://api.deepseek.com"
)
```

---

## 🚀 启动游戏

```bash
python main.py
```

按照终端提示输入即可游玩。

---

## 📁 项目结构

```plaintext
JOJOGame/
├── main.py               # 游戏主入口
├── gpt_logic.py          # 替身生成 & 六维属性
├── battle_judge.py       # GPT 战斗判定
├── battle_state.py       # 战斗状态数据结构
├── battle_system.py      # 普通替身战斗处理
├── turn_engine.py        # 回合流程控制
├── player_utils.py       # 玩家身体属性生成
├── stand_utils.py        # 替身属性解析与描述修改
├── encounter_engine.py   # 场景与敌人生成
├── requirements.txt      # 依赖库列表
```

---

## 📋 示例截图

```
🌀 替身名：『Ripwire』
📖 替身能力：能将触碰到的任何固体表面转化为隐形超音速切割线。

🎭 敌人态度：中立
🌍 场景：校园屋顶

📝 你的行动：布置天罗地网
📡 GPT 判定结果：
成功：是  
效果：敌人行动被限制  
敌人是否死亡：否  
是否结束战斗：否  
```

---

## 🤖 免责声明

- 本项目为学习与娱乐用途，不得用于商业用途。
- 若使用 GPT 服务，请遵守相关平台条款。
- 请勿将 API Key 暴露给他人。

---

## 💬 欢迎交流

有趣的替身设定？脑洞对战想法？欢迎发 issue 或 PR！

---

Made with ❤️ & 替身能量 by Me,lol

# 猫叫声类型详细说明

## 文件夹结构

系统支持16种猫叫声类型，按4大类分类，需要在服务器上创建对应的文件夹：

```
config/cat_sounds/
├── 01_positive_greeting/          # 😊 积极与亲昵 - 打招呼
├── 01_positive_affectionate/        # 😊 积极与亲昵 - 对主人撒娇
├── 01_positive_loving/              # 😊 积极与亲昵 - 表达喜欢爱你
├── 01_positive_inviting_play/       # 😊 积极与亲昵 - 邀请一起玩
├── 01_positive_awake_stretch/       # 😊 积极与亲昵 - 睡醒慵懒叫
├── 02_demand_missing/               # 🗣️ 需求与沟通 - 思念主人
├── 02_demand_curious/               # 🗣️ 需求与沟通 - 发出疑问
├── 02_demand_eating_happily/        # 🗣️ 需求与沟通 - 吃饭满足叫
├── 03_warning_annoyed/              # ⚠️ 警告与不适 - 不耐烦/责怪
├── 03_warning_angry_growl/          # ⚠️ 警告与不适 - 生气叫骂
├── 03_warning_aggressive_hiss/      # ⚠️ 警告与不适 - 生气想打人
├── 03_warning_mating_call/           # ⚠️ 警告与不适 - 求偶叫声
├── 04_stress_concerned_inquiry/     # 😿 压力与痛苦 - 关心/好奇询问
├── 04_stress_sneeze/                # 😿 压力与痛苦 - 打喷嚏
├── 04_stress_whining/               # 😿 压力与痛苦 - 委屈叫声
└── 04_stress_scared_scream/         # 😿 压力与痛苦 - 害怕尖叫
```

## 各类型详细说明

### 😊 积极与亲昵 (01_positive)

#### 1. 打招呼 (01_positive_greeting)

**具体叫声描述：**
- 短促、轻盈的问候叫声
- 友好、轻快的音调

**识别关键词：**
- 中文：打招呼、问候、你好、回来、见面、欢迎、友好、轻快、短促、轻盈
- 英文：greeting, hello, hi, welcome, friendly, light, short, quick

#### 2. 对主人撒娇 (01_positive_affectionate)

**具体叫声描述：**
- 声音拐弯、温柔的撒娇声
- 亲昵、依恋的表达

**识别关键词：**
- 中文：撒娇、亲昵、温柔、拐弯、黏人、卖萌、可爱、亲热、依恋
- 英文：affectionate, cute, sweet, gentle, loving, cuddly, adorable, tender

#### 3. 表达喜欢爱你 (01_positive_loving)

**具体叫声描述：**
- 表达爱意和满足的叫声
- 幸福、开心的音调

**识别关键词：**
- 中文：喜欢、爱你、爱意、满足、幸福、开心、快乐、满足、表达爱
- 英文：loving, love, affection, happy, content, satisfied, joyful, pleased

#### 4. 邀请一起玩 (01_positive_inviting_play)

**具体叫声描述：**
- 邀请玩耍的轻快叫声
- 活泼、兴奋的音调

**识别关键词：**
- 中文：邀请、一起玩、玩耍、游戏、轻快、活泼、兴奋、互动、想玩
- 英文：inviting, play, game, playful, active, excited, interactive, fun

#### 5. 睡醒慵懒叫 (01_positive_awake_stretch)

**具体叫声描述：**
- 睡醒后舒服、慵懒的叫声
- 联想伸懒腰的场景

**识别关键词：**
- 中文：睡醒、慵懒、伸懒腰、舒服、放松、醒来、打哈欠、舒展
- 英文：awake, stretch, lazy, comfortable, relaxed, waking, yawn, stretching

### 🗣️ 需求与沟通 (02_demand)

#### 6. 思念主人 (02_demand_missing)

**具体叫声描述：**
- 激动、拉长的叫声
- 表达思念或强烈需求

**识别关键词：**
- 中文：思念、想念、想你、主人、激动、拉长、强烈需求、渴望、呼唤
- 英文：missing, miss, longing, owner, excited, long, demand, craving, call

#### 7. 发出疑问 (02_demand_curious)

**具体叫声描述：**
- 表达好奇和疑问的叫声
- 询问、探索的音调

**识别关键词：**
- 中文：疑问、好奇、询问、什么、为什么、疑惑、想知道、探索
- 英文：curious, question, wonder, what, why, inquiry, explore, ask

#### 8. 吃饭满足叫 (02_demand_eating_happily)

**具体叫声描述：**
- 边吃边发出的满意叫声
- 享受、满足的音调

**识别关键词：**
- 中文：吃饭、满足、满意、好吃、享受、进食、用餐、饱足、美味
- 英文：eating, happily, satisfied, delicious, enjoy, meal, food, yummy, tasty

### ⚠️ 警告与不适 (03_warning)

#### 9. 不耐烦/责怪 (03_warning_annoyed)

**具体叫声描述：**
- 短促、重音，类似"啂"的不满叫声
- 烦躁、抗议的音调

**识别关键词：**
- 中文：不耐烦、责怪、不满、啂、短促、重音、烦躁、抱怨、抗议
- 英文：annoyed, impatient, complaint, short, heavy, irritated, protest, grumble

#### 10. 生气叫骂 (03_warning_angry_growl)

**具体叫声描述：**
- 连续、喉咙发出的警告声
- 未到攻击程度，但表达愤怒

**识别关键词：**
- 中文：生气、叫骂、愤怒、警告、低吼、连续、喉咙、威胁、不满
- 英文：angry, growl, warning, threat, continuous, throat, mad, furious

#### 11. 生气想打人 (03_warning_aggressive_hiss)

**具体叫声描述：**
- 尖利、持续哈气的攻击前最后警告
- 谨慎使用，表示强烈攻击性

**识别关键词：**
- 中文：想打人、攻击、尖利、持续、哈气、防御、危险、警告、攻击性
- 英文：aggressive, hiss, attack, sharp, continuous, defense, danger, hostile

#### 12. 求偶叫声 (03_warning_mating_call)

**具体叫声描述：**
- 发情期粗粝、不好听的长鸣
- 归类为"不适"更合适

**识别关键词：**
- 中文：求偶、发情、粗粝、长鸣、不好听、交配、繁殖、发情期
- 英文：mating, call, heat, rough, long, breeding, reproduction, estrus

### 😿 压力与痛苦 (04_stress)

#### 13. 关心/好奇询问 (04_stress_concerned_inquiry)

**具体叫声描述：**
- 拐弯拉长、带询问语调的叫声
- 表达谨慎关心

**识别关键词：**
- 中文：关心、好奇询问、拐弯、拉长、询问、谨慎、担心、关切、询问
- 英文：concerned, inquiry, question, careful, worried, care, ask, inquire

#### 14. 打喷嚏 (04_stress_sneeze)

**具体叫声描述：**
- 对刺激物（如胡椒）的生理反应声音
- 作为特殊反应归此类

**识别关键词：**
- 中文：打喷嚏、喷嚏、刺激、过敏、反应、阿嚏
- 英文：sneeze, sneezing, irritation, allergy, reaction, achoo

#### 15. 委屈叫声 (04_stress_whining)

**具体叫声描述：**
- 短促带试探的委屈、讨好声
- 可怜、哀求的音调

**识别关键词：**
- 中文：委屈、讨好、短促、试探、可怜、哀求、诉苦、抱怨
- 英文：whining, pleading, short, tentative, pitiful, begging, complaining

#### 16. 害怕尖叫 (04_stress_scared_scream)

**具体叫声描述：**
- 受惊吓时的极高音调短促尖叫
- 恐惧、惊恐的音调

**识别关键词：**
- 中文：害怕、尖叫、惊吓、受惊、恐惧、极高音调、短促、惊恐
- 英文：scared, scream, frightened, fear, high pitch, short, terrified, panic

## 识别优先级

系统按以下优先级识别猫叫声类型：

1. **标签格式**（最高优先级）
   - `[sound:01_positive_greeting]` 或 `<sound>02_demand_missing</sound>`
   - `猫叫:03_warning_annoyed` 或 `叫声:04_stress_scared_scream`
   - 也支持简写格式：`[sound:greeting]` 会自动匹配 `01_positive_greeting`

2. **关键词匹配**（按严重程度）
   - 最严重：压力与痛苦 (04_stress) → 警告与不适 (03_warning)
   - 中等：需求与沟通 (02_demand)
   - 积极：积极与亲昵 (01_positive)（默认）

3. **默认类型**
   - 如果无法识别，使用默认类型：`01_positive_greeting`

## 文件选择机制

每个文件夹中可以放置多个音频文件，系统会：
1. 扫描文件夹中的所有音频文件（.wav, .mp3, .ogg, .m4a）
2. **随机选择**其中一个文件播放
3. 每次对话可能播放不同的文件，增加变化性

## 使用建议

1. **每个类型至少准备3-5个文件**，增加随机性和自然度
2. **文件命名**：可以任意命名，系统会自动识别格式
3. **文件时长**：建议1-5秒，过长可能影响响应速度
4. **文件质量**：使用清晰的猫叫声音频

## 配置示例

在Web界面配置时：
- **猫叫声文件夹路径**：`config/cat_sounds`
- **默认猫叫声类型**：`01_positive_greeting`（当无法识别时使用）

## 大语言模型提示词建议

为了让系统准确识别猫叫声类型，可以在系统提示词中添加：

```
你是一只可爱的小猫。请根据你的情绪和状态，在回复中使用以下格式之一：

1. 使用标签格式：[sound:01_positive_greeting] 或 <sound>02_demand_missing</sound>
2. 或在回复中包含对应的关键词

可用的猫叫声类型（按情感分类）：

😊 积极与亲昵 (01_positive):
- 01_positive_greeting: 打招呼、问候、你好
- 01_positive_affectionate: 撒娇、亲昵、温柔
- 01_positive_loving: 喜欢、爱你、满足
- 01_positive_inviting_play: 邀请、一起玩、游戏
- 01_positive_awake_stretch: 睡醒、慵懒、伸懒腰

🗣️ 需求与沟通 (02_demand):
- 02_demand_missing: 思念、想念、想你
- 02_demand_curious: 疑问、好奇、询问
- 02_demand_eating_happily: 吃饭、满足、享受

⚠️ 警告与不适 (03_warning):
- 03_warning_annoyed: 不耐烦、责怪、不满
- 03_warning_angry_growl: 生气、叫骂、愤怒
- 03_warning_aggressive_hiss: 想打人、攻击、危险
- 03_warning_mating_call: 求偶、发情

😿 压力与痛苦 (04_stress):
- 04_stress_concerned_inquiry: 关心、好奇询问
- 04_stress_sneeze: 打喷嚏
- 04_stress_whining: 委屈、讨好
- 04_stress_scared_scream: 害怕、尖叫、惊吓
```

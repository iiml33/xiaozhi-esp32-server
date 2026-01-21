# 犬叫声音频文件目录

此目录用于存放犬叫声的音频文件，用于"犬语TTS"模式。

## 文件夹结构

系统支持16种犬叫声类型，按4大类分类：

```
config/dog_sounds/
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

## 分类说明

### 😊 积极与亲昵 (01_positive)
- **01_positive_greeting** - 打招呼：短促、轻盈的问候叫声
- **01_positive_affectionate** - 对主人撒娇：声音拐弯、温柔的撒娇声
- **01_positive_loving** - 表达喜欢爱你：表达爱意和满足的叫声
- **01_positive_inviting_play** - 邀请一起玩：邀请玩耍的轻快叫声
- **01_positive_awake_stretch** - 睡醒慵懒叫：睡醒后舒服、慵懒的叫声

### 🗣️ 需求与沟通 (02_demand)
- **02_demand_missing** - 思念主人：激动、拉长的叫声，表达思念或强烈需求
- **02_demand_curious** - 发出疑问：表达好奇和疑问的叫声
- **02_demand_eating_happily** - 吃饭满足叫：边吃边发出的满意叫声

### ⚠️ 警告与不适 (03_warning)
- **03_warning_annoyed** - 不耐烦/责怪：短促、重音的不满叫声
- **03_warning_angry_growl** - 生气叫骂：连续、喉咙发出的警告声、咆哮
- **03_warning_aggressive_hiss** - 生气想打人：尖利、持续的攻击前最后警告、狂吠
- **03_warning_mating_call** - 求偶叫声：发情期粗粝、不好听的长鸣

### 😿 压力与痛苦 (04_stress)
- **04_stress_concerned_inquiry** - 关心/好奇询问：拐弯拉长、带询问语调的叫声
- **04_stress_sneeze** - 打喷嚏：对刺激物的生理反应声音
- **04_stress_whining** - 委屈叫声：短促带试探的委屈、讨好声、呜咽
- **04_stress_scared_scream** - 害怕尖叫：受惊吓时的极高音调短促尖叫

## 音频文件要求

- **格式**：.wav, .mp3, .ogg, .m4a
- **采样率**：建议 16kHz
- **声道**：单声道（mono）
- **比特率**：建议 16-bit
- **时长**：建议1-5秒，过长可能影响响应速度
- **数量**：每个类型文件夹至少准备3-5个不同的音频文件，以增加随机性和自然度

## 文件命名

音频文件可以任意命名，系统会自动识别支持的格式。建议使用有意义的文件名，例如：
- `greeting_01.wav`
- `affectionate_soft.wav`
- `missing_long.wav`

## 使用说明

1. 将准备好的音频文件放入对应的类型文件夹
2. 在智控台的TTS模型配置中选择"犬语"模型
3. 确保LLM输出的文本中包含情绪关键词，系统会自动匹配对应的音频文件
4. 如果找不到对应类型的音频，会使用默认类型（`01_positive_greeting`）

## 识别方式

系统支持以下识别方式（按优先级排序）：

1. **标签格式**（最高优先级）
   - `[sound:01_positive_greeting]`
   - `<sound>02_demand_missing</sound>`
   - `犬叫:03_warning_annoyed` 或 `狗叫:04_stress_scared_scream`
   - 也支持简写：`[sound:greeting]` 会自动匹配 `01_positive_greeting`

2. **关键词匹配**
   - 系统会根据文本中的中英文关键词自动识别类型
   - 详细关键词列表请查看各文件夹中的 README.md 文件

3. **默认类型**
   - 如果无法识别，使用默认类型：`01_positive_greeting`

## 注意事项

1. **文件夹名称**：必须使用下划线格式（如 `01_positive_greeting`），不要使用空格或中文字符
2. **文件权限**：确保服务器有读取这些文件夹的权限
3. **文件质量**：使用清晰的犬叫声音频，避免噪音和失真
4. **文件大小**：建议使用较小的音频文件，避免影响响应速度

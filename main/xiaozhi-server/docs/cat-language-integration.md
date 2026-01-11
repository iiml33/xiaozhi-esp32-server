# 猫语TTS集成说明

## 功能概述

猫语TTS是一个特殊的TTS提供者，它不会将文本转换为语音，而是根据大语言模型返回的文本中的情绪，返回预先录制好的猫叫声。这让小智客户端以为在与一只猫交流。

## 猫叫声类型识别

系统支持识别以下16种猫叫声类型，按4大类分类：

### 😊 积极与亲昵 (01_positive)
1. **打招呼 (01_positive_greeting)** - 短促、轻盈的问候叫声
2. **对主人撒娇 (01_positive_affectionate)** - 声音拐弯、温柔的撒娇声
3. **表达喜欢爱你 (01_positive_loving)** - 表达爱意和满足的叫声
4. **邀请一起玩 (01_positive_inviting_play)** - 邀请玩耍的轻快叫声
5. **睡醒慵懒叫 (01_positive_awake_stretch)** - 睡醒后舒服、慵懒的叫声

### 🗣️ 需求与沟通 (02_demand)
6. **思念主人 (02_demand_missing)** - 激动、拉长的叫声，表达思念或强烈需求
7. **发出疑问 (02_demand_curious)** - 表达好奇和疑问的叫声
8. **吃饭满足叫 (02_demand_eating_happily)** - 边吃边发出的满意叫声

### ⚠️ 警告与不适 (03_warning)
9. **不耐烦/责怪 (03_warning_annoyed)** - 短促、重音，类似"啂"的不满叫声
10. **生气叫骂 (03_warning_angry_growl)** - 连续、喉咙发出的警告声
11. **生气想打人 (03_warning_aggressive_hiss)** - 尖利、持续哈气的攻击前最后警告
12. **求偶叫声 (03_warning_mating_call)** - 发情期粗粝、不好听的长鸣

### 😿 压力与痛苦 (04_stress)
13. **关心/好奇询问 (04_stress_concerned_inquiry)** - 拐弯拉长、带询问语调的叫声
14. **打喷嚏 (04_stress_sneeze)** - 对刺激物的生理反应声音
15. **委屈叫声 (04_stress_whining)** - 短促带试探的委屈、讨好声
16. **害怕尖叫 (04_stress_scared_scream)** - 受惊吓时的极高音调短促尖叫

详细说明和关键词列表请参考：[猫叫声类型详细说明](./cat-language-sound-types.md)

## 猫叫声类型标签格式

除了关键词识别，系统还支持以下格式的标签（优先级最高）：

- `[sound:01_positive_greeting]` - 打招呼
- `[sound:02_demand_missing]` - 思念主人
- `<sound>03_warning_annoyed</sound>` - 不耐烦/责怪
- `猫叫:04_stress_scared_scream` - 害怕尖叫
- `叫声:01_positive_affectionate` - 对主人撒娇

也支持简写格式（系统会自动匹配完整名称）：
- `[sound:greeting]` → 自动匹配 `01_positive_greeting`
- `[sound:missing]` → 自动匹配 `02_demand_missing`

支持的16种类型完整列表请参考：[猫叫声类型详细说明](./cat-language-sound-types.md)

## 文件夹结构

在服务器上创建以下文件夹结构来存放猫叫声文件：

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

详细说明请参考：[猫叫声类型详细说明](./cat-language-sound-types.md)

## 支持的音频格式

- `.wav`
- `.mp3`
- `.ogg`
- `.m4a`

## 配置说明

### 在Web界面配置

1. 登录小智服务器Web管理界面
2. 进入"模型配置" -> "TTS"
3. 点击"新增"按钮
4. 在"供应器"下拉菜单中选择"猫语"
5. 配置以下参数：
   - **猫叫声文件夹路径** (`cat_sounds_dir`): 默认为 `config/cat_sounds`
   - **默认猫叫声类型** (`default_sound_type`): 当无法识别时使用的默认类型，默认为 `01_positive_greeting`

### 在配置文件中配置

在 `config.yaml` 中添加以下配置：

```yaml
TTS:
  CatLanguage:
    type: cat_language
    cat_sounds_dir: config/cat_sounds
    default_sound_type: 01_positive_greeting
    output_dir: tmp/

selected_module:
  TTS: CatLanguage
```

## 工作原理

1. 当大语言模型返回文本时，猫语TTS提供者会分析文本内容
2. 从文本中提取情绪信息（通过关键词或标签）
3. 根据识别到的情绪，从对应的文件夹中随机选择一个音频文件
4. 将选中的猫叫声文件返回给客户端播放

## 使用建议

1. **准备猫叫声文件**：
   - 为每种猫叫声类型准备多个不同的音频文件，以增加变化性
   - 建议每个类型文件夹至少准备3-5个不同的音频文件
   - 音频文件时长建议在1-5秒之间

2. **大语言模型配置**：
   - 在提示词中要求大语言模型在回复中包含猫叫声类型信息
   - 可以使用标签格式，例如：`[sound:01_positive_greeting]` 或 `<sound>02_demand_missing</sound>`
   - 或者在回复文本中包含对应的关键词（如：打招呼、思念、撒娇等）

3. **测试**：
   - 测试不同情绪的识别是否准确
   - 确保所有情绪文件夹中都有音频文件
   - 验证音频文件格式是否支持

## 故障排除

### 问题：无法找到猫叫声文件

**解决方案**：
- 检查 `cat_sounds_dir` 配置的路径是否正确
- 确保文件夹结构正确（16个子文件夹存在）
- 检查音频文件格式是否支持

### 问题：猫叫声类型识别不准确

**解决方案**：
- 在文本中使用明确的标签格式：`[sound:01_positive_greeting]` 或 `<sound>02_demand_missing</sound>`
- 确保文本中包含对应的关键词（参考[猫叫声类型详细说明](./cat-language-sound-types.md)）
- 如果无法识别，系统会使用默认类型（01_positive_greeting）

### 问题：没有播放声音

**解决方案**：
- 检查对应情绪文件夹中是否有音频文件
- 检查音频文件是否损坏
- 查看服务器日志了解详细错误信息

## 示例

### 示例1：使用标签格式

大语言模型返回：
```
[sound:01_positive_affectionate] 主人，我好想你呀！
```

系统会识别到"01_positive_affectionate"类型，从 `config/cat_sounds/01_positive_affectionate/` 文件夹中随机选择一个音频文件播放。

### 示例2：使用关键词

大语言模型返回：
```
我很思念主人，想你了。
```

系统会识别到"思念"、"想你"关键词，对应"02_demand_missing"类型，从 `config/cat_sounds/02_demand_missing/` 文件夹中随机选择一个音频文件播放。

### 示例3：使用简写标签

大语言模型返回：
```
[sound:greeting] 你好！
```

系统会识别到简写"greeting"，自动匹配为"01_positive_greeting"类型，从 `config/cat_sounds/01_positive_greeting/` 文件夹中随机选择一个音频文件播放。

### 示例4：无法识别类型

大语言模型返回：
```
今天是个普通的日子。
```

系统无法识别到明确的类型，会使用默认类型（01_positive_greeting），从 `config/cat_sounds/01_positive_greeting/` 文件夹中随机选择一个音频文件播放。

# 猫语模式使用指南

## 快速开始：让系统进入猫语模式

### 步骤1：准备猫叫声文件

在服务器上创建猫叫声文件夹并添加音频文件。系统支持16种猫叫声类型，按4大类分类：

```bash
# 在xiaozhi-server目录下创建文件夹结构

# 😊 积极与亲昵 (01_positive)
mkdir -p config/cat_sounds/01_positive_greeting
mkdir -p config/cat_sounds/01_positive_affectionate
mkdir -p config/cat_sounds/01_positive_loving
mkdir -p config/cat_sounds/01_positive_inviting_play
mkdir -p config/cat_sounds/01_positive_awake_stretch

# 🗣️ 需求与沟通 (02_demand)
mkdir -p config/cat_sounds/02_demand_missing
mkdir -p config/cat_sounds/02_demand_curious
mkdir -p config/cat_sounds/02_demand_eating_happily

# ⚠️ 警告与不适 (03_warning)
mkdir -p config/cat_sounds/03_warning_annoyed
mkdir -p config/cat_sounds/03_warning_angry_growl
mkdir -p config/cat_sounds/03_warning_aggressive_hiss
mkdir -p config/cat_sounds/03_warning_mating_call

# 😿 压力与痛苦 (04_stress)
mkdir -p config/cat_sounds/04_stress_concerned_inquiry
mkdir -p config/cat_sounds/04_stress_sneeze
mkdir -p config/cat_sounds/04_stress_whining
mkdir -p config/cat_sounds/04_stress_scared_scream
```

然后将对应的猫叫声文件放入各个文件夹（.wav, .mp3, .ogg, .m4a格式）：

- `config/cat_sounds/01_positive_greeting/` - 打招呼的叫声
- `config/cat_sounds/01_positive_affectionate/` - 撒娇的叫声
- `config/cat_sounds/01_positive_loving/` - 表达爱意的叫声
- `config/cat_sounds/01_positive_inviting_play/` - 邀请玩耍的叫声
- `config/cat_sounds/01_positive_awake_stretch/` - 睡醒慵懒的叫声
- `config/cat_sounds/02_demand_missing/` - 思念主人的叫声
- `config/cat_sounds/02_demand_curious/` - 发出疑问的叫声
- `config/cat_sounds/02_demand_eating_happily/` - 吃饭满足的叫声
- `config/cat_sounds/03_warning_annoyed/` - 不耐烦/责怪的叫声
- `config/cat_sounds/03_warning_angry_growl/` - 生气叫骂的叫声
- `config/cat_sounds/03_warning_aggressive_hiss/` - 生气想打人的叫声
- `config/cat_sounds/03_warning_mating_call/` - 求偶的叫声
- `config/cat_sounds/04_stress_concerned_inquiry/` - 关心/好奇询问的叫声
- `config/cat_sounds/04_stress_sneeze/` - 打喷嚏的声音
- `config/cat_sounds/04_stress_whining/` - 委屈的叫声
- `config/cat_sounds/04_stress_scared_scream/` - 害怕尖叫的叫声

**建议**：每个类型文件夹至少准备3-5个不同的音频文件，以增加变化性。

### 步骤2：在Web界面创建猫语TTS模型配置

1. **登录Web管理界面**
   - 打开浏览器访问小智服务器Web管理界面

2. **进入模型配置页面**
   - 点击左侧菜单 "模型配置"
   - 选择 "TTS" 标签页

3. **添加猫语TTS模型**
   - 点击页面上的 "新增" 按钮
   - 在弹出的对话框中填写：
     - **模型ID**: `CatLanguage`（或自定义）
     - **模型名称**: `猫语`（或自定义）
     - **模型编码**: `CatLanguage`（或自定义）
     - **供应器**: 在下拉菜单中选择 **"猫语"**
     - **排序号**: 填写数字（如：1）
   
4. **配置猫语参数**
   - 在"调用信息"部分配置：
     - **猫叫声文件夹路径** (`cat_sounds_dir`): `config/cat_sounds`（默认值，可根据实际情况修改）
     - **默认猫叫声类型** (`default_sound_type`): `01_positive_greeting`（默认值，当无法识别时使用）

5. **保存配置**
   - 点击 "保存" 按钮
   - 确认模型已成功创建并显示在列表中

### 步骤3：在角色配置中选择猫语TTS

1. **进入角色配置页面**
   - 点击左侧菜单 "角色配置"（或"Agent配置"）

2. **选择或创建角色**
   - 选择一个现有角色进行编辑，或创建新角色

3. **选择TTS模型**
   - 在配置表单中找到 "TTS" 选项
   - 在下拉菜单中选择刚才创建的 **"猫语"** TTS模型
   - 注意：猫语模式不需要选择音色（Voice），因为使用的是预录制的猫叫声

4. **保存角色配置**
   - 点击 "保存" 按钮保存配置

### 步骤4：配置大语言模型以输出情绪信息

为了让系统能够正确识别情绪并播放对应的猫叫声，需要配置大语言模型在回复中包含情绪信息。

#### 方法1：在系统提示词中添加情绪要求

在角色配置的"系统提示词"中添加类似以下内容：

```
你是一只可爱的小猫。请根据你的情绪和状态，在回复中使用以下格式之一：

1. 使用标签格式：[sound:01_positive_greeting] 或 <sound>02_demand_missing</sound>
2. 或在回复中包含对应的关键词

可用的猫叫声类型（按情感分类）：

😊 积极与亲昵 (01_positive):
- 打招呼: 打招呼、问候、你好
- 撒娇: 撒娇、亲昵、温柔
- 表达爱意: 喜欢、爱你、满足
- 邀请玩耍: 邀请、一起玩、游戏
- 睡醒慵懒: 睡醒、慵懒、伸懒腰

🗣️ 需求与沟通 (02_demand):
- 思念主人: 思念、想念、想你
- 发出疑问: 疑问、好奇、询问
- 吃饭满足: 吃饭、满足、享受

⚠️ 警告与不适 (03_warning):
- 不耐烦: 不耐烦、责怪、不满
- 生气叫骂: 生气、叫骂、愤怒
- 生气想打人: 想打人、攻击、危险
- 求偶: 求偶、发情

😿 压力与痛苦 (04_stress):
- 关心询问: 关心、好奇询问
- 打喷嚏: 打喷嚏
- 委屈: 委屈、讨好
- 害怕尖叫: 害怕、尖叫、惊吓
```

#### 方法2：使用声音标签格式

要求大语言模型在回复中使用标签格式，例如：

```
[sound:01_positive_affectionate] 主人，我好想你呀！
```

或使用简写格式：

```
[sound:greeting] 你好！
```

#### 方法3：在回复中包含情绪关键词

大语言模型可以在回复中直接包含情绪关键词，例如：

```
我很思念主人，想你了。
```

系统会自动识别"思念"、"想你"关键词，并播放 `02_demand_missing` 文件夹中的猫叫声。

### 步骤5：测试猫语模式

1. **连接小智客户端**
   - 使用小智客户端连接到服务器

2. **开始对话**
   - 向小智发送消息，例如："你好，今天心情怎么样？"

3. **验证猫叫声**
   - 如果大语言模型回复中包含"打招呼"、"你好"等关键词，系统应该播放 `01_positive_greeting` 文件夹中的猫叫声
   - 如果回复中包含"思念"、"想你"等词，系统应该播放 `02_demand_missing` 文件夹中的猫叫声
   - 如果回复中包含"撒娇"、"亲昵"等词，系统应该播放 `01_positive_affectionate` 文件夹中的猫叫声

## 猫叫声类型识别规则

系统会按以下优先级识别猫叫声类型：

1. **声音标签格式**（优先级最高）
   - `[sound:01_positive_greeting]`
   - `<sound>02_demand_missing</sound>`
   - `猫叫:03_warning_annoyed`
   - `叫声:04_stress_scared_scream`
   - 也支持简写：`[sound:greeting]` 会自动匹配 `01_positive_greeting`

2. **中文关键词匹配**（按严重程度）
   - 最严重：压力与痛苦 (04_stress) → 警告与不适 (03_warning)
   - 中等：需求与沟通 (02_demand)
   - 积极：积极与亲昵 (01_positive)（默认）

3. **英文关键词匹配**
   - 系统也会识别英文关键词

4. **默认类型**（如果无法识别）
   - 使用配置的默认类型（默认：`01_positive_greeting`）

详细的关键词列表请参考：[猫叫声类型详细说明](./cat-language-sound-types.md)

## 常见问题

### Q1: 为什么没有播放猫叫声？

**检查清单**：
- ✅ 确认在角色配置中选择了"猫语"TTS模型
- ✅ 确认猫叫声文件夹路径正确，且文件夹中存在音频文件
- ✅ 确认音频文件格式支持（.wav, .mp3, .ogg, .m4a）
- ✅ 查看服务器日志，检查是否有错误信息

### Q2: 为什么总是播放同一个猫叫声？

**原因**：可能是该类型文件夹中只有一个音频文件。

**解决方案**：在对应类型文件夹中添加多个不同的猫叫声文件，系统会随机选择。

### Q3: 猫叫声类型识别不准确怎么办？

**解决方案**：
1. 使用明确的标签格式：`[sound:01_positive_greeting]`
2. 在系统提示词中明确要求大语言模型输出猫叫声类型信息
3. 检查大语言模型的回复是否包含对应的关键词
4. 参考[猫叫声类型详细说明](./cat-language-sound-types.md)了解各类型的关键词

### Q4: 可以添加更多类型吗？

**当前支持的类型**：16种类型，分为4大类

如需添加更多类型，需要修改 `cat_language.py` 文件中的关键词映射和文件夹结构。

### Q5: 如何切换回普通TTS？

**方法**：
1. 进入角色配置页面
2. 将TTS模型从"猫语"改为其他TTS模型（如EdgeTTS、讯飞TTS等）
3. 保存配置

### Q6: 文件夹名称必须使用下划线格式吗？

**是的**，系统使用下划线格式的文件夹名称（如 `01_positive_greeting`），这样可以：
- 保持文件夹排序的一致性
- 清晰标识分类层级
- 兼容Linux文件系统

## 配置示例

### 完整的角色配置示例（使用猫语）：

```json
{
  "agentCode": "cat_agent",
  "agentName": "小猫助手",
  "ttsModelId": "TTS_CatLanguage",  // 使用猫语TTS
  "llmModelId": "LLM_ChatGLM",
  "systemPrompt": "你是一只可爱的小猫。请根据你的情绪和状态，在回复中使用标签格式：[sound:01_positive_greeting] 或在回复中包含对应的关键词。"
}
```

## 注意事项

1. **音频文件质量**：建议使用清晰的猫叫声音频，时长在1-5秒之间
2. **文件命名**：音频文件可以任意命名，系统会自动识别支持的格式
3. **文件夹权限**：确保服务器有读取猫叫声文件夹的权限
4. **性能考虑**：如果音频文件很大，可能会影响响应速度，建议使用较小的音频文件
5. **文件夹结构**：必须使用下划线格式的文件夹名称（如 `01_positive_greeting`）

## 下一步

- 查看 [猫语TTS集成说明](./cat-language-integration.md) 了解技术细节
- 查看 [猫叫声类型详细说明](./cat-language-sound-types.md) 了解所有16种类型的详细信息和关键词
- 根据需要调整情绪识别关键词
- 优化大语言模型的提示词以获得更好的情绪识别效果

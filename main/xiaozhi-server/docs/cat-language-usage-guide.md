# 猫语模式使用指南

## 快速开始：让系统进入猫语模式

### 步骤1：准备猫叫声文件

在服务器上创建猫叫声文件夹并添加音频文件。系统支持19种猫叫声类型，按4大类分类（使用拼音命名）：

```bash
# 在xiaozhi-server目录下创建文件夹结构（拼音命名）

# 😊 友好满足 (01_youhao_*)
mkdir -p config/cat_sounds/01_youhao_sajiao
mkdir -p config/cat_sounds/01_youhao_manzu
mkdir -p config/cat_sounds/01_youhao_zhenhaochi
mkdir -p config/cat_sounds/01_youhao_shufu
mkdir -p config/cat_sounds/01_youhao_huhuan_wanyou
mkdir -p config/cat_sounds/01_youhao_dahulu

# 📣 吸引注意 (02_xiyin_*)
mkdir -p config/cat_sounds/02_xiyin_dazhaohu
mkdir -p config/cat_sounds/02_xiyin_xiangni
mkdir -p config/cat_sounds/02_xiyin_ele
mkdir -p config/cat_sounds/02_xiyin_xingfen
mkdir -p config/cat_sounds/02_xiyin_weiqu
mkdir -p config/cat_sounds/02_xiyin_qiujiumama
mkdir -p config/cat_sounds/02_xiyin_jiaolv_haipa
mkdir -p config/cat_sounds/02_xiyin_qiuou
mkdir -p config/cat_sounds/02_xiyin_fuyan

# ⚠️ 威胁警告 (03_weixie_*)
mkdir -p config/cat_sounds/03_weixie_qingdu_buman
mkdir -p config/cat_sounds/03_weixie_zhongdu_buman
mkdir -p config/cat_sounds/03_weixie_yanzhong_buman

# 📢 呼唤猫的叫声 (04_huhuan_*)
mkdir -p config/cat_sounds/04_huhuan_maojiao
```

然后将对应的猫叫声文件放入各个文件夹（.wav, .mp3, .ogg, .m4a格式）：

- `config/cat_sounds/01_youhao_sajiao/` - 撒娇的叫声
- `config/cat_sounds/01_youhao_manzu/` - 满足的叫声
- `config/cat_sounds/01_youhao_zhenhaochi/` - 真好吃的叫声
- `config/cat_sounds/01_youhao_shufu/` - 舒服放松的叫声
- `config/cat_sounds/01_youhao_huhuan_wanyou/` - 友好呼唤/邀请玩耍的叫声
- `config/cat_sounds/01_youhao_dahulu/` - 打呼噜的声音
- `config/cat_sounds/02_xiyin_dazhaohu/` - 打招呼的叫声
- `config/cat_sounds/02_xiyin_xiangni/` - 想你的叫声
- `config/cat_sounds/02_xiyin_ele/` - 饿了催饭的叫声
- `config/cat_sounds/02_xiyin_xingfen/` - 兴奋的叫声
- `config/cat_sounds/02_xiyin_weiqu/` - 委屈的叫声
- `config/cat_sounds/02_xiyin_qiujiumama/` - 求救/找妈妈的叫声
- `config/cat_sounds/02_xiyin_jiaolv_haipa/` - 焦虑/害怕的叫声
- `config/cat_sounds/02_xiyin_qiuou/` - 求偶的叫声
- `config/cat_sounds/02_xiyin_fuyan/` - 敷衍回应的叫声
- `config/cat_sounds/03_weixie_qingdu_buman/` - 轻度不满的叫声
- `config/cat_sounds/03_weixie_zhongdu_buman/` - 中度不满的叫声
- `config/cat_sounds/03_weixie_yanzhong_buman/` - 重度不满/强烈警告的叫声
- `config/cat_sounds/04_huhuan_maojiao/` - 呼唤猫的叫声

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
     - **默认猫叫声类型** (`default_sound_type`): `02_xiyin_fuyan`（默认值，当无法识别时使用，表示“敷衍”）

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
你是一只可爱的小猫。请根据你的情绪和状态，只输出一个或多个声音标签：

[sound:01_youhao_sajiao]
[sound:02_xiyin_dazhaohu] [sound:01_youhao_sajiao]

可用的猫叫声类型（按情感分类，使用拼音标识）：

😊 友好满足 (01_youhao_*):
- 撒娇: 01_youhao_sajiao
- 满足: 01_youhao_manzu
- 真好吃: 01_youhao_zhenhaochi
- 舒服: 01_youhao_shufu
- 邀请玩耍/呼唤: 01_youhao_huhuan_wanyou
- 打呼噜: 01_youhao_dahulu

📣 吸引注意 (02_xiyin_*):
- 打招呼: 02_xiyin_dazhaohu
- 想你: 02_xiyin_xiangni
- 饿了: 02_xiyin_ele
- 兴奋: 02_xiyin_xingfen
- 委屈: 02_xiyin_weiqu
- 求救/找妈妈: 02_xiyin_qiujiumama
- 焦虑/害怕: 02_xiyin_jiaolv_haipa
- 求偶: 02_xiyin_qiuou
- 敷衍: 02_xiyin_fuyan

⚠️ 威胁警告 (03_weixie_*):
- 轻度不满: 03_weixie_qingdu_buman
- 中度不满: 03_weixie_zhongdu_buman
- 重度不满: 03_weixie_yanzhong_buman

📢 呼唤猫的叫声 (04_huhuan_*):
- 呼唤猫的叫声: 04_huhuan_maojiao
```

请不要输出自然语言正文，也不要使用旧的简写标签、关键词识别或“猫翻译”式映射。

### 步骤5：测试猫语模式

1. **连接小智客户端**
   - 使用小智客户端连接到服务器

2. **开始对话**
   - 向小智发送消息，例如："你好，今天心情怎么样？"

3. **验证猫叫声**
   - 如果大语言模型回复中包含"撒娇"等词，建议在标签中使用 `01_youhao_sajiao`
   - 如果回复中包含"饿了"、"吃饭"等词，建议在标签中使用 `02_xiyin_ele`
   - 如果回复中包含"不准"、"不可以"等强烈否定词，建议在标签中使用 `03_weixie_zhongdu_buman` 或 `03_weixie_yanzhong_buman`

## 猫叫声类型识别规则

系统会按以下优先级识别猫叫声类型：

1. **声音标签格式**（优先级最高）
   - `[sound:01_youhao_sajiao]`
   - `[sound:02_xiyin_dazhaohu]`
   - `[sound:03_weixie_qingdu_buman]`
   - `[sound:04_huhuan_maojiao]`

2. **默认类型**（如果无法识别）
   - 使用配置的默认类型（默认：`02_xiyin_fuyan`，敷衍）

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
1. 使用明确的标签格式：`[sound:01_youhao_sajiao]`
2. 在系统提示词中明确要求大语言模型只输出猫叫声标签
3. 检查大语言模型的回复是否使用当前的拼音类型名
4. 检查对应类型文件夹内是否存在可播放音频

### Q4: 可以添加更多类型吗？

**当前支持的类型**：19种类型，分为4大类

如需添加更多类型，需要修改 `cat_language.py` 文件中的有效类型列表和文件夹结构。

### Q5: 如何切换回普通TTS？

**方法**：
1. 进入角色配置页面
2. 将TTS模型从"猫语"改为其他TTS模型（如EdgeTTS、讯飞TTS等）
3. 保存配置

### Q6: 文件夹名称必须使用下划线格式吗？

**是的**，系统使用下划线格式的文件夹名称（如 `01_youhao_sajiao`），这样可以：
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
  "systemPrompt": "你是一只可爱的小猫。请只输出一个或多个猫叫声标签，例如：[sound:01_youhao_sajiao]。不要输出任何自然语言正文。"
}
```

## 注意事项

1. **音频文件质量**：建议使用清晰的猫叫声音频，时长在1-5秒之间
2. **文件命名**：音频文件可以任意命名，系统会自动识别支持的格式
3. **文件夹权限**：确保服务器有读取猫叫声文件夹的权限
4. **性能考虑**：如果音频文件很大，可能会影响响应速度，建议使用较小的音频文件
5. **文件夹结构**：必须使用下划线格式的文件夹名称（如 `01_youhao_sajiao`）

## 下一步

- 查看 [猫语TTS集成说明](./cat-language-integration.md) 了解技术细节
- 根据需要补充各类型音频素材
- 优化大语言模型的提示词以稳定输出 `sound` 标签

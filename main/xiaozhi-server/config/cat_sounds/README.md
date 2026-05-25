# 猫叫声音频文件目录

此目录用于存放猫叫声的音频文件，用于"猫语TTS"模式。

## 文件夹结构

系统支持19种猫叫声类型，按4大类分类（使用拼音命名）：

```
config/cat_sounds/
├── 01_youhao_sajiao/              # 😊 友好满足 - 撒娇
├── 01_youhao_manzu/               # 😊 友好满足 - 满足
├── 01_youhao_zhenhaochi/          # 😊 友好满足 - 真好吃
├── 01_youhao_shufu/               # 😊 友好满足 - 舒服
├── 01_youhao_huhuan_wanyou/       # 😊 友好满足 - 友好呼唤/邀请玩耍
├── 01_youhao_dahulu/              # 😊 友好满足 - 打呼噜
├── 02_xiyin_dazhaohu/             # 📣 吸引注意 - 打招呼
├── 02_xiyin_xiangni/              # 📣 吸引注意 - 想你
├── 02_xiyin_ele/                  # 📣 吸引注意 - 饿了
├── 02_xiyin_xingfen/              # 📣 吸引注意 - 兴奋
├── 02_xiyin_weiqu/                # 📣 吸引注意 - 委屈
├── 02_xiyin_qiujiumama/           # 📣 吸引注意 - 求救/找妈妈
├── 02_xiyin_jiaolv_haipa/         # 📣 吸引注意 - 焦虑/害怕
├── 02_xiyin_qiuou/                # 📣 吸引注意 - 求偶
├── 02_xiyin_fuyan/                # 📣 吸引注意 - 敷衍
├── 03_weixie_qingdu_buman/        # ⚠️ 威胁警告 - 轻度不满
├── 03_weixie_zhongdu_buman/       # ⚠️ 威胁警告 - 中度不满
├── 03_weixie_yanzhong_buman/      # ⚠️ 威胁警告 - 重度不满
└── 04_huhuan_maojiao/             # 📢 呼唤猫的叫声 - 呼唤猫的叫声
```

## 分类说明

### 😊 友好满足 (01_youhao_*)
- **01_youhao_sajiao** - 撒娇：有求于人、情感亲密时的撒娇叫声
- **01_youhao_manzu** - 满足：生理愉悦、心理满足、感官享受时的愉悦叫声
- **01_youhao_zhenhaochi** - 真好吃：吃到美味食物时的开心叫声
- **01_youhao_shufu** - 舒服：身体放松、被抚摸或休息时的舒服叫声
- **01_youhao_huhuan_wanyou** - 友好呼唤/邀请玩耍：猫感到无聊、想邀请一起玩时的呼唤叫声
- **01_youhao_dahulu** - 打呼噜：满足、放松时发出的“咕噜咕噜”声

### 📣 吸引注意 (02_xiyin_*)
- **02_xiyin_dazhaohu** - 打招呼：看到主人或熟悉的人时的问候叫声
- **02_xiyin_xiangni** - 想你：思念主人、想被陪伴时的呼唤叫声
- **02_xiyin_ele** - 饿了：接近饭点或看到食物时的催促叫声
- **02_xiyin_xingfen** - 兴奋：收到好消息、获得胜利或发现有趣事物时的兴奋叫声
- **02_xiyin_weiqu** - 委屈：觉得受了委屈、希望被安慰时的委屈叫声
- **02_xiyin_qiujiumama** - 求救/找妈妈：特别是幼猫寻求安全感、找人的时候
- **02_xiyin_jiaolv_haipa** - 焦虑/害怕：感到失控、紧张或害怕时的叫声
- **02_xiyin_qiuou** - 求偶：发情期持续、略刺耳的叫声
- **02_xiyin_fuyan** - 敷衍：不太感兴趣、只是勉强回应一下的叫声

### ⚠️ 威胁警告 (03_weixie_*)
- **03_weixie_qingdu_buman** - 轻度不满：被持续打扰、被做了不太喜欢的事情时的轻微警告
- **03_weixie_zhongdu_buman** - 中度不满：轻度警告无效后、被强行抱住或控制时的更强烈抗议
- **03_weixie_yanzhong_buman** - 重度不满：感到严重威胁或疼痛、被逼到角落或准备战斗时的强烈警告叫

### 📢 呼唤猫的叫声 (04_huhuan_*)
- **04_huhuan_maojiao** - 呼唤猫的叫声

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
2. 在智控台的TTS模型配置中选择"猫语"模型
3. 确保LLM输出的文本中包含情绪关键词，系统会自动匹配对应的音频文件
4. 如果找不到对应类型的音频，会使用默认类型（`02_xiyin_fuyan`，敷衍）

## 识别方式

系统支持以下识别方式（按优先级排序）：

1. **标签格式**（最高优先级）
   - `[sound:02_xiyin_fuyan]`
   - `<sound>02_xiyin_dazhaohu</sound>`

2. **默认类型**
   - 如果无法识别，使用默认类型：`02_xiyin_fuyan`（敷衍）

## 详细文档

- 详细类型说明和关键词列表：`docs/cat-language-sound-types.md`
- 集成说明：`docs/cat-language-integration.md`
- 使用指南：`docs/cat-language-usage-guide.md`

## 注意事项

1. **文件夹名称**：必须使用下划线格式（如 `01_youhao_sajiao`），不要使用空格或中文字符
2. **文件权限**：确保服务器有读取这些文件夹的权限
3. **文件质量**：使用清晰的猫叫声音频，避免噪音和失真
4. **文件大小**：建议使用较小的音频文件，避免影响响应速度
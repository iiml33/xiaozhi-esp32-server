# 猫语TTS集成说明

## 功能概述

猫语TTS是一个特殊的TTS提供者，它不会将文本转换为语音，而是根据大语言模型返回的 `sound` 标签，返回预先录制好的猫叫声。这让小智客户端以为在与一只猫交流。

## 猫叫声类型识别

系统支持识别以下19种猫叫声类型，按4大类分类（使用中文拼音标识）：

### 😊 友好满足 (01_youhao_*)
1. **撒娇 (01_youhao_sajiao)** - 有求于人、情感亲密时的撒娇叫声
2. **满足 (01_youhao_manzu)** - 生理或心理都很满足时的愉悦叫声
3. **真好吃 (01_youhao_zhenhaochi)** - 品尝美味食物时发出的满足叫声
4. **舒服 (01_youhao_shufu)** - 身体放松、被抚摸或休息时的舒服叫声
5. **友好呼唤/邀请玩耍 (01_youhao_huhuan_wanyou)** - 感到无聊、想邀请一起玩时的呼唤声
6. **打呼噜 (01_youhao_dahulu)** - 猫放松、半睡或睡觉时的呼噜声

### 📣 吸引注意 (02_xiyin_*)
7. **打招呼 (02_xiyin_dazhaohu)** - 主动和人打招呼时的短促叫声
8. **想你 (02_xiyin_xiangni)** - 思念主人、想被陪伴时的呼唤叫声
9. **饿了 (02_xiyin_ele)** - 想吃饭、催促喂食时的叫声
10. **兴奋 (02_xiyin_xingfen)** - 收到好消息、获得奖励或发现有趣事物时的兴奋叫声
11. **委屈 (02_xiyin_weiqu)** - 感到不公、被忽视或想要安慰时的委屈叫声
12. **求救/找妈妈 (02_xiyin_qiujiumama)** - 特别是幼猫找安全感或遇到困难时的叫声
13. **焦虑/害怕 (02_xiyin_jiaolv_haipa)** - 面对陌生环境、噪音或压力时的紧张叫声
14. **求偶 (02_xiyin_qiuou)** - 发情期持续、粗粝的叫声
15. **敷衍 (02_xiyin_fuyan)** - 不太想理人、只是勉强回应一下时的叫声

### ⚠️ 威胁警告 (03_weixie_*)
16. **轻度不满 (03_weixie_qingdu_buman)** - 被稍微打扰或做了不太喜欢的事时的低声警告
17. **中度不满 (03_weixie_zhongdu_buman)** - 轻度警告被无视、被强行控制或被弄疼时的更明显抗议
18. **重度不满 (03_weixie_yanzhong_buman)** - 感到严重威胁、被逼到角落或准备战斗时的强烈警告叫

### 📢 呼唤猫的叫声 (04_huhuan_*)
19. **呼唤猫的叫声 (04_huhuan_maojiao)** - 呼唤猫的叫声

## 猫叫声类型标签格式

系统仅根据标准 `sound` 标签识别猫叫声类型：

- `[sound:01_youhao_sajiao]` - 撒娇
- `[sound:02_xiyin_dazhaohu]` - 打招呼
- `[sound:03_weixie_qingdu_buman]` - 轻度不满
- `[sound:04_huhuan_maojiao]` - 呼唤其他猫

## 文件夹结构

在服务器上创建以下文件夹结构来存放猫叫声文件（拼音命名）：

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
   - **默认猫叫声类型** (`default_sound_type`): 当无法识别时使用的默认类型，默认为 `02_xiyin_fuyan`（敷衍）

### 在配置文件中配置

在 `config.yaml` 中添加以下配置：

```yaml
TTS:
  CatLanguage:
    type: cat_language
    cat_sounds_dir: config/cat_sounds
    default_sound_type: 02_xiyin_fuyan
    output_dir: tmp/

selected_module:
  TTS: CatLanguage
```

## 工作原理

1. 当大语言模型返回文本时，猫语TTS提供者会分析文本内容
2. 从文本中提取一个或多个 `[sound:类型]` 标签
3. 根据识别到的情绪，从对应的文件夹中随机选择一个音频文件
4. 将选中的猫叫声文件返回给客户端播放

## 使用建议

1. **准备猫叫声文件**：
   - 为每种猫叫声类型准备多个不同的音频文件，以增加变化性
   - 建议每个类型文件夹至少准备3-5个不同的音频文件
   - 音频文件时长建议在1-5秒之间

2. **大语言模型配置**：
   - 在提示词中要求大语言模型只输出猫叫声标签
   - 使用标准标签格式，例如：`[sound:01_youhao_sajiao]`

3. **测试**：
   - 测试不同情绪的识别是否准确
   - 确保所有情绪文件夹中都有音频文件
   - 验证音频文件格式是否支持

## 故障排除

### 问题：无法找到猫叫声文件

**解决方案**：
- 检查 `cat_sounds_dir` 配置的路径是否正确
- 确保文件夹结构正确（19个子文件夹存在）
- 检查音频文件格式是否支持

### 问题：猫叫声类型识别不准确

**解决方案**：
- 在文本中使用明确的标签格式：`[sound:01_youhao_sajiao]`
- 确保标签使用当前拼音类型名，例如：`[sound:01_youhao_sajiao]`
- 如果无法识别，系统会使用默认类型（`02_xiyin_fuyan`）

### 问题：没有播放声音

**解决方案**：
- 检查对应情绪文件夹中是否有音频文件
- 检查音频文件是否损坏
- 查看服务器日志了解详细错误信息

## 示例

### 示例1：使用标签格式

大语言模型返回：
```
[sound:01_youhao_sajiao]
```

系统会识别到 `01_youhao_sajiao` 类型，从 `config/cat_sounds/01_youhao_sajiao/` 文件夹中随机选择一个音频文件播放。

### 示例2：使用多标签

大语言模型返回：
```
[sound:02_xiyin_dazhaohu] [sound:01_youhao_sajiao]
```

系统会依次选择 `02_xiyin_dazhaohu` 和 `01_youhao_sajiao` 对应的音频，并按顺序拼接播放。

### 示例3：无法识别类型

大语言模型返回：
```
今天是个普通的日子。
```

系统无法识别到有效标签，会使用默认类型 `02_xiyin_fuyan`，从 `config/cat_sounds/02_xiyin_fuyan/` 文件夹中随机选择一个音频文件播放。

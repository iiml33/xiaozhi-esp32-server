# 猫翻译声音文件夹

此文件夹用于存储猫翻译TTS提供者使用的猫叫声音频文件。

## 文件夹结构

```
cat_translator_sounds/
├── 01_positive_greeting/          # 打招呼/召唤类
│   # 指令：过来、跟我走、这里、到这儿、回去、进房间、你好呀
│   # 示例音频文件：meow_greeting_01.wav, meow_greeting_02.wav
│
├── 01_positive_affectionate/      # 夸奖/安抚类
│   # 指令：乖、真棒、没事、不怕
│   # 示例音频文件：meow_affectionate_01.wav, meow_affectionate_02.wav
│
├── 01_positive_inviting_play/     # 邀请玩耍类
│   # 指令：来玩、把玩具拿来
│   # 示例音频文件：meow_play_01.wav, meow_play_02.wav
│
├── 02_demand_eating_happily/      # 吃饭类
│   # 指令：吃饭啦
│   # 示例音频文件：meow_eating_01.wav, meow_eating_02.wav
│
├── 02_demand_curious/             # 疑问/喝水类
│   # 指令：喝水、过来喝水
│   # 示例音频文件：meow_curious_01.wav, meow_curious_02.wav
│
└── 03_warning_annoyed/            # 制止/边界类
    # 指令：不可以、不要、停、下来
    # 示例音频文件：meow_warning_01.wav, meow_warning_02.wav
```

## 支持的音频格式

- `.wav` (推荐)
- `.mp3`
- `.ogg`
- `.m4a`

## 使用方法

1. 在每个类型文件夹中放入对应的猫叫声音频文件
2. 系统会从对应类型文件夹中随机选择一个音频文件播放
3. 建议每个类型文件夹至少包含2-3个不同的音频文件，以增加随机性

## 指令类型映射

| 用户指令 | 文件夹 | 说明 |
|---------|--------|------|
| 过来、跟我走、这里、到这儿、回去、进房间、你好呀 | 01_positive_greeting | 召唤类 |
| 乖、真棒、没事、不怕 | 01_positive_affectionate | 夸奖/安抚类 |
| 来玩、把玩具拿来 | 01_positive_inviting_play | 邀请玩耍类 |
| 吃饭啦 | 02_demand_eating_happily | 吃饭类 |
| 喝水、过来喝水 | 02_demand_curious | 疑问/喝水类 |
| 不可以、不要、停、下来 | 03_warning_annoyed | 制止/边界类 |

## Docker 挂载方式

在 Docker 部署时，此目录通过 `docker-compose_all.yml` 挂载到容器内：

```yaml
- ./main/xiaozhi-server/config/cat_translator_sounds:/opt/xiaozhi-server/cat_translator_sounds
```

配置时，将 `cat_sounds_dir` 设置为容器内的绝对路径：
```json
{
  "cat_sounds_dir": "/opt/xiaozhi-server/cat_translator_sounds"
}
```

## 注意事项

- 此文件夹独立于 `cat_sounds`（猫语TTS），两者互不干扰
- 音频文件建议使用16kHz采样率，单声道，WAV格式以获得最佳兼容性
- 如果某个类型文件夹为空，系统会使用默认类型（01_positive_greeting）
- **挂载方式**：配置为绝对路径时，适用于Docker挂载，系统不会自动创建目录，请确保挂载目录存在
- **相对路径**：配置为相对路径时，系统会自动创建目录（如果不存在）
-- liquibase formatted sql

-- changeset xiaozhi:202601100000
-- 添加犬语TTS供应器
delete from `ai_model_provider` where id = 'SYSTEM_TTS_DogLanguage';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_DogLanguage', 'TTS', 'dog_language', '犬语', '[{"key":"dog_sounds_dir","label":"犬叫声文件夹路径","type":"string"},{"key":"default_sound_type","label":"默认犬叫声类型","type":"string"}]', 25, 1, NOW(), 1, NOW());

-- 添加犬语TTS模型配置
delete from `ai_model_config` where id = 'TTS_DogLanguage';
INSERT INTO `ai_model_config` VALUES ('TTS_DogLanguage', 'TTS', 'DogLanguage', '犬语', 0, 1, '{\"type\": \"dog_language\", \"dog_sounds_dir\": \"config/dog_sounds\", \"default_sound_type\": \"01_positive_greeting\"}', NULL, NULL, 25, NULL, NULL, NULL, NULL);

-- 更新犬语TTS配置说明
UPDATE `ai_model_config` SET 
`doc_link` = '',
`remark` = '犬语TTS说明：
1. 此TTS提供者会根据大语言模型返回的文本中的情绪和上下文返回对应的犬叫声
2. 需要在服务器上创建犬叫声文件夹，结构如下：
   config/dog_sounds/
   ├── 01_positive_greeting/          (打招呼)
   ├── 01_positive_affectionate/        (对主人撒娇)
   ├── 01_positive_loving/              (表达喜欢爱你)
   ├── 01_positive_inviting_play/       (邀请一起玩)
   ├── 01_positive_awake_stretch/       (睡醒慵懒叫)
   ├── 02_demand_missing/               (思念主人)
   ├── 02_demand_curious/               (发出疑问)
   ├── 02_demand_eating_happily/        (吃饭满足叫)
   ├── 03_warning_annoyed/              (不耐烦/责怪)
   ├── 03_warning_angry_growl/          (生气叫骂)
   ├── 03_warning_aggressive_hiss/      (生气想打人)
   ├── 03_warning_mating_call/           (求偶叫声)
   ├── 04_stress_concerned_inquiry/     (关心/好奇询问)
   ├── 04_stress_sneeze/                (打喷嚏)
   ├── 04_stress_whining/               (委屈叫声)
   └── 04_stress_scared_scream/         (害怕尖叫)
3. 支持的音频格式：.wav, .mp3, .ogg, .m4a
4. 系统会从对应类型文件夹中随机选择一个音频文件播放
5. 犬叫声类型识别方式（按优先级）：
   - 犬叫声类型标签：[sound:01_positive_greeting] 或 <sound>02_demand_missing</sound>
   - 标签格式：犬叫:greeting 或 狗叫:missing
   - 从文本中查找关键词（支持中英文）
   - 如果无法识别，将使用默认类型（默认：01_positive_greeting）
' WHERE `id` = 'TTS_DogLanguage';

-- 添加默认音色（虽然犬语不需要音色，但为了兼容性添加）
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_DogLanguage';
INSERT INTO `ai_tts_voice` VALUES ('TTS_DogLanguage_0000', 'TTS_DogLanguage', '默认', 'default', '中文', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);

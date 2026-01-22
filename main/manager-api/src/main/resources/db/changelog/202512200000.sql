-- 添加猫语TTS供应器
delete from `ai_model_provider` where id = 'SYSTEM_TTS_CatLanguage';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_CatLanguage', 'TTS', 'cat_language', '猫语', '[{"key":"cat_sounds_dir","label":"猫叫声文件夹路径","type":"string"},{"key":"default_sound_type","label":"默认猫叫声类型","type":"string"}]', 0, 1, NOW(), 1, NOW());

-- 添加猫语TTS模型配置
delete from `ai_model_config` where id = 'TTS_CatLanguage';
INSERT INTO `ai_model_config` VALUES ('TTS_CatLanguage', 'TTS', 'CatLanguage', '猫语', 0, 1, '{\"type\": \"cat_language\", \"cat_sounds_dir\": \"config/cat_sounds\", \"default_sound_type\": \"01_positive_greeting\"}', NULL, NULL, 0, NULL, NULL, NULL, NULL);

-- 更新猫语TTS配置说明
UPDATE `ai_model_config` SET 
`doc_link` = '',
`remark` = '猫语TTS说明：
1. 此TTS提供者会根据大语言模型返回的文本中的情绪和上下文返回对应的猫叫声
2. 需要在服务器上创建猫叫声文件夹，结构如下（16种类型，按4大类分类）：
   config/cat_sounds/
   ├── 01_positive_greeting/          (😊 积极与亲昵 - 打招呼)
   ├── 01_positive_affectionate/        (😊 积极与亲昵 - 对主人撒娇)
   ├── 01_positive_loving/              (😊 积极与亲昵 - 表达喜欢爱你)
   ├── 01_positive_inviting_play/       (😊 积极与亲昵 - 邀请一起玩)
   ├── 01_positive_awake_stretch/       (😊 积极与亲昵 - 睡醒慵懒叫)
   ├── 02_demand_missing/               (🗣️ 需求与沟通 - 思念主人)
   ├── 02_demand_curious/               (🗣️ 需求与沟通 - 发出疑问)
   ├── 02_demand_eating_happily/        (🗣️ 需求与沟通 - 吃饭满足叫)
   ├── 03_warning_annoyed/              (⚠️ 警告与不适 - 不耐烦/责怪)
   ├── 03_warning_angry_growl/          (⚠️ 警告与不适 - 生气叫骂)
   ├── 03_warning_aggressive_hiss/      (⚠️ 警告与不适 - 生气想打人)
   ├── 03_warning_mating_call/           (⚠️ 警告与不适 - 求偶叫声)
   ├── 04_stress_concerned_inquiry/     (😿 压力与痛苦 - 关心/好奇询问)
   ├── 04_stress_sneeze/                (😿 压力与痛苦 - 打喷嚏)
   ├── 04_stress_whining/               (😿 压力与痛苦 - 委屈叫声)
   └── 04_stress_scared_scream/         (😿 压力与痛苦 - 害怕尖叫)
3. 支持的音频格式：.wav, .mp3, .ogg, .m4a
4. 系统会从对应类型文件夹中随机选择一个音频文件播放
5. 猫叫声类型识别方式：
   - 仅通过标准标签格式识别：[sound:01_positive_greeting] 或 <sound>02_demand_missing</sound>
   - 支持简写格式：[sound:greeting] 会自动匹配 01_positive_greeting
   - 如果无法识别，将使用默认类型（默认：01_positive_greeting）
   - 注意：系统不再使用关键词匹配，LLM必须在回复中包含标签格式
' WHERE `id` = 'TTS_CatLanguage';

-- 添加默认音色（虽然猫语不需要音色，但为了兼容性添加）
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_CatLanguage';
INSERT INTO `ai_tts_voice` VALUES ('TTS_CatLanguage_0000', 'TTS_CatLanguage', '默认', 'default', '中文', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);

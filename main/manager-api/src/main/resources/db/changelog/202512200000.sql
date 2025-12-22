-- 添加猫语TTS供应器
delete from `ai_model_provider` where id = 'SYSTEM_TTS_CatLanguage';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_CatLanguage', 'TTS', 'cat_language', '猫语', '[{"key":"cat_sounds_dir","label":"猫叫声文件夹路径","type":"string"},{"key":"default_sound_type","label":"默认猫叫声类型","type":"string"}]', 24, 1, NOW(), 1, NOW());

-- 添加猫语TTS模型配置
delete from `ai_model_config` where id = 'TTS_CatLanguage';
INSERT INTO `ai_model_config` VALUES ('TTS_CatLanguage', 'TTS', 'CatLanguage', '猫语', 0, 1, '{\"type\": \"cat_language\", \"cat_sounds_dir\": \"config/cat_sounds\", \"default_sound_type\": \"meow\"}', NULL, NULL, 24, NULL, NULL, NULL, NULL);

-- 更新猫语TTS配置说明
UPDATE `ai_model_config` SET 
`doc_link` = '',
`remark` = '猫语TTS说明：
1. 此TTS提供者会根据大语言模型返回的文本中的情绪和上下文返回对应的猫叫声
2. 需要在服务器上创建猫叫声文件夹，结构如下：
   config/cat_sounds/
   ├── meow/        (喵 - 求关注、撒娇、期待、轻微抱怨)
   ├── purr/        (呼噜 - 放松、满足、安全感)
   ├── trill/       (咕噜咕噜/颤音 - 友好、欢迎)
   ├── chattering/  (咔咔/啾啾 - 兴奋、专注、略挫败)
   ├── hiss/        (哈气 - 恐惧、防御、警告)
   ├── growl/       (低吼/咆哮 - 威胁、愤怒、防御升级)
   ├── yowl/        (嚎叫/长嗷 - 发情、压力、焦虑、疼痛)
   ├── scream/      (尖叫/惨叫 - 突然疼痛、强烈惊吓)
   └── mutter/      (嘟嘟嘟不满声/咕哝 - 不耐烦、轻度烦躁)
3. 支持的音频格式：.wav, .mp3, .ogg, .m4a
4. 系统会从对应类型文件夹中随机选择一个音频文件播放
5. 猫叫声类型识别方式（按优先级）：
   - 猫叫声类型标签：[sound:meow] 或 <sound>purr</sound>
   - 从文本中查找关键词（支持中英文）
   - 如果无法识别，将使用默认类型（默认：meow）
' WHERE `id` = 'TTS_CatLanguage';


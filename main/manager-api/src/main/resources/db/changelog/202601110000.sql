-- liquibase formatted sql

-- changeset xiaozhi:202601110000
-- 添加猫翻译TTS供应器
delete from `ai_model_provider` where id = 'SYSTEM_TTS_CatTranslator';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_CatTranslator', 'TTS', 'cat_translator', '猫翻译', '[{"key":"cat_sounds_dir","label":"猫叫声文件夹路径","type":"string"},{"key":"llm_config","label":"LLM配置（用于判断用户指令类型）","type":"dict","dict_name":"llm_config"},{"key":"default_sound_type","label":"默认猫叫声类型","type":"string"}]', 1, 1, NOW(), 1, NOW());

-- 添加猫翻译TTS模型配置
delete from `ai_model_config` where id = 'TTS_CatTranslator';
INSERT INTO `ai_model_config` VALUES ('TTS_CatTranslator', 'TTS', 'CatTranslator', '猫翻译', 0, 1, '{\"type\": \"cat_translator\", \"cat_sounds_dir\": \"config/cat_translator_sounds\", \"llm_config\": {\"type\": \"openai\", \"api_key\": \"你的LLM API密钥\", \"model_name\": \"gpt-3.5-turbo\", \"base_url\": \"https://api.openai.com/v1\"}, \"default_sound_type\": \"01_positive_greeting\"}', NULL, NULL, 1, NULL, NULL, NULL, NULL);

-- 更新猫翻译TTS配置说明
UPDATE `ai_model_config` SET 
`doc_link` = '',
`remark` = '猫翻译TTS说明：
1. 此TTS提供者根据用户的语音输入（ASR转文本后），使用LLM判断用户想下达的指令类型，然后调用相应的猫叫声音频文件
2. 配置说明：
   - cat_sounds_dir: 猫翻译声音文件夹路径（默认：config/cat_translator_sounds，独立于cat_language）
     * 支持挂载方式：配置为绝对路径（如：/opt/xiaozhi-server/cat_translator_sounds）时，适用于Docker挂载
     * 相对路径：基于项目根目录（如：config/cat_translator_sounds）
   - llm_config: LLM配置，用于判断用户指令类型
     * type: LLM类型（如：openai、ollama、dify等）
     * api_key: LLM API密钥
     * model_name: 模型名称（根据LLM类型调整）
     * base_url: API地址（根据LLM类型调整）
   - default_sound_type: 默认猫叫声类型（默认：01_positive_greeting）
3. 需要在服务器上创建猫翻译声音文件夹，结构如下（独立于cat_language）：
   - Docker部署：通过docker-compose挂载，容器内路径为 /opt/xiaozhi-server/cat_translator_sounds
   - 本地部署：在项目根目录下创建 config/cat_translator_sounds/
   文件夹结构：
   ├── 01_positive_greeting/          (打招呼/召唤：过来、跟我走、这里、到这儿、回去、进房间、你好呀)
   ├── 01_positive_affectionate/        (夸奖/安抚：乖、真棒、没事、不怕)
   ├── 01_positive_inviting_play/       (邀请玩耍：来玩、把玩具拿来)
   ├── 02_demand_eating_happily/        (吃饭：吃饭啦)
   ├── 02_demand_curious/               (疑问/喝水：喝水、过来喝水)
   ├── 03_warning_annoyed/              (制止/边界：不可以、不要、停、下来)
   └── 其他类型...
4. 支持的音频格式：.wav, .mp3, .ogg, .m4a
5. 系统会从对应类型文件夹中随机选择一个音频文件播放
6. 指令识别规则（根据台词表）：
   - 召唤类：过来、跟我走、这里、到这儿、回去、进房间、你好呀 → 01_positive_greeting
   - 夸奖与安抚：乖、真棒、没事、不怕 → 01_positive_affectionate
   - 制止与边界：不可以、不要、停、下来 → 03_warning_annoyed
   - 生活指令：吃饭啦 → 02_demand_eating_happily，喝水、过来喝水 → 02_demand_curious
   - 互动与玩耍：来玩、把玩具拿来 → 01_positive_inviting_play
7. LLM提示词设计：
   - LLM会直接返回文件夹名称（如：01_positive_greeting）
   - 输出格式严格：只包含文件夹名称，无解释、无标点、无换行
   - 如果无法判断，返回：default（将使用默认类型）
8. 如果LLM无法识别指令类型，会使用关键词匹配作为备用方案，如果仍然无法识别，则使用默认类型
9. 注意：猫翻译使用独立的声音文件夹（config/cat_translator_sounds），与猫语（config/cat_sounds）分开管理
' WHERE `id` = 'TTS_CatTranslator';

-- 添加默认音色（虽然猫翻译不需要音色，但为了兼容性添加）
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_CatTranslator';
INSERT INTO `ai_tts_voice` VALUES ('TTS_CatTranslator_0000', 'TTS_CatTranslator', '默认', 'default', '中文', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);

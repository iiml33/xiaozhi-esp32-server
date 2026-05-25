-- 添加猫语TTS供应器
delete from `ai_model_provider` where id = 'SYSTEM_TTS_CatLanguage';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_CatLanguage', 'TTS', 'cat_language', '猫语', '[{"key":"cat_sounds_dir","label":"猫叫声文件夹路径","type":"string"},{"key":"default_sound_type","label":"默认猫叫声类型","type":"string"}]', 0, 1, NOW(), 1, NOW());

-- 添加猫语TTS模型配置
delete from `ai_model_config` where id = 'TTS_CatLanguage';
INSERT INTO `ai_model_config` VALUES ('TTS_CatLanguage', 'TTS', 'CatLanguage', '猫语', 0, 1, '{\"type\": \"cat_language\", \"cat_sounds_dir\": \"config/cat_sounds\", \"default_sound_type\": \"02_xiyin_fuyan\"}', NULL, NULL, 0, NULL, NULL, NULL, NULL);

-- 更新猫语TTS配置说明
UPDATE `ai_model_config` SET 
`doc_link` = '',
`remark` = '猫语TTS说明：
1. 此TTS提供者会根据大语言模型返回的文本中的情绪和上下文返回对应的猫叫声
2. 需要在服务器上创建猫叫声文件夹，结构如下（19种类型，按4大类分类，使用拼音命名）：
   config/cat_sounds/
   ├── 01_youhao_sajiao/              (😊 友好满足 - 撒娇)
   ├── 01_youhao_manzu/               (😊 友好满足 - 满足)
   ├── 01_youhao_zhenhaochi/          (😊 友好满足 - 真好吃)
   ├── 01_youhao_shufu/               (😊 友好满足 - 舒服)
   ├── 01_youhao_huhuan_wanyou/       (😊 友好满足 - 友好呼唤/邀请玩耍)
   ├── 01_youhao_dahulu/              (😊 友好满足 - 打呼噜)
   ├── 02_xiyin_dazhaohu/             (📣 吸引注意 - 打招呼)
   ├── 02_xiyin_xiangni/              (📣 吸引注意 - 想你)
   ├── 02_xiyin_ele/                  (📣 吸引注意 - 饿了)
   ├── 02_xiyin_xingfen/              (📣 吸引注意 - 兴奋)
   ├── 02_xiyin_weiqu/                (📣 吸引注意 - 委屈)
   ├── 02_xiyin_qiujiumama/           (📣 吸引注意 - 求救/找妈妈)
   ├── 02_xiyin_jiaolv_haipa/         (📣 吸引注意 - 焦虑/害怕)
   ├── 02_xiyin_qiuou/                (📣 吸引注意 - 求偶)
   ├── 02_xiyin_fuyan/                (📣 吸引注意 - 敷衍)
   ├── 03_weixie_qingdu_buman/        (⚠️ 威胁警告 - 轻度不满)
   ├── 03_weixie_zhongdu_buman/       (⚠️ 威胁警告 - 中度不满)
   ├── 03_weixie_yanzhong_buman/      (⚠️ 威胁警告 - 重度不满)
   └── 04_huhuan_maojiao/             (📢 呼唤猫的叫声 - 呼唤猫的叫声)
3. 支持的音频格式：.wav, .mp3, .ogg, .m4a
4. 系统会从对应类型文件夹中随机选择一个音频文件播放
5. 猫叫声类型识别方式：
   - 仅通过标准标签格式识别：[sound:02_xiyin_fuyan] 等
   - 如果无法识别，将使用默认类型（默认：02_xiyin_fuyan，敷衍）
   - 注意：系统不再使用关键词匹配，LLM必须在回复中包含标签格式
' WHERE `id` = 'TTS_CatLanguage';

-- 添加默认音色（虽然猫语不需要音色，但为了兼容性添加）
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_CatLanguage';
INSERT INTO `ai_tts_voice` VALUES ('TTS_CatLanguage_0000', 'TTS_CatLanguage', '默认', 'default', '中文', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);

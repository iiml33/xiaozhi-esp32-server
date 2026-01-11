-- liquibase formatted sql

-- changeset xiaozhi:202512120922
-- 注意：动物叫声TTS已废弃，相关配置已删除
-- 请使用猫语(CatLanguage)或犬语(DogLanguage)替代

-- 删除 AnimalSound 动物叫声 TTS 供应器（已废弃）
DELETE FROM `ai_model_provider` WHERE id = 'SYSTEM_TTS_AnimalSound';

-- 删除 AnimalSound TTS 模型配置（已废弃）
DELETE FROM `ai_model_config` WHERE id = 'TTS_AnimalSound';

-- 删除 AnimalSound 默认音色（已废弃）
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_AnimalSound';


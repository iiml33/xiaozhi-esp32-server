-- liquibase formatted sql

-- changeset xiaozhi:202603121200
-- 移除猫翻译TTS供应器，统一使用猫语标签TTS
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_CatTranslator';
DELETE FROM `ai_model_config` WHERE id = 'TTS_CatTranslator' OR model_code = 'CatTranslator';
DELETE FROM `ai_model_provider` WHERE id = 'SYSTEM_TTS_CatTranslator' OR provider_code = 'cat_translator';

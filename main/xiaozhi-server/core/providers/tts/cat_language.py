import os
import re
import random
from config.logger import setup_logging
from config.config_loader import get_project_dir
from core.providers.tts.base import TTSProviderBase

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        # 猫叫声文件夹路径（相对于项目根目录）
        cat_sounds_dir_rel = config.get("cat_sounds_dir", "config/cat_sounds")
        # 将相对路径转换为绝对路径（基于项目根目录）
        if os.path.isabs(cat_sounds_dir_rel):
            self.cat_sounds_dir = cat_sounds_dir_rel
        else:
            self.cat_sounds_dir = os.path.join(get_project_dir(), cat_sounds_dir_rel)
        # 确保文件夹存在
        if not os.path.exists(self.cat_sounds_dir):
            os.makedirs(self.cat_sounds_dir)
            logger.bind(tag=TAG).warning(
                f"猫叫声文件夹不存在，已创建: {self.cat_sounds_dir}，请添加猫叫声文件"
            )
        
        # 根据提示词模板：4大类16种具体类型
        # 😊 积极与亲昵 (01_positive)
        # 🗣️ 需求与沟通 (02_demand)
        # ⚠️ 警告与不适 (03_warning)
        # 😿 压力与痛苦 (04_stress)
        # 注意：实际识别仅通过标准标签格式 [sound:类型]，不再使用关键词映射
        
        # 默认猫叫声类型（如果无法识别）
        # 固定使用 01_positive_greeting 作为默认类型，确保始终有效
        config_default_type = config.get("default_sound_type", "01_positive_greeting")
        valid_default_types = [
            "01_positive_greeting", "01_positive_affectionate", "01_positive_loving",
            "01_positive_inviting_play", "01_positive_awake_stretch",
            "02_demand_missing", "02_demand_curious", "02_demand_eating_happily",
            "03_warning_annoyed", "03_warning_angry_growl", "03_warning_aggressive_hiss",
            "03_warning_mating_call",
            "04_stress_concerned_inquiry", "04_stress_sneeze", "04_stress_whining",
            "04_stress_scared_scream"
        ]
        
        # 验证配置的默认类型是否有效
        if config_default_type and config_default_type.lower() in [t.lower() for t in valid_default_types]:
            # 找到匹配的有效类型
            for valid_type in valid_default_types:
                if config_default_type.lower() == valid_type.lower():
                    self.default_sound_type = valid_type
                    logger.bind(tag=TAG).info(f"使用配置的默认类型: {valid_type}")
                    break
        else:
            # 如果配置的默认类型无效或为空，强制使用01_positive_greeting
            if config_default_type and config_default_type.lower() != "01_positive_greeting":
                logger.bind(tag=TAG).warning(
                    f"配置的默认类型 '{config_default_type}' 无效，强制使用 '01_positive_greeting'"
                )
            self.default_sound_type = "01_positive_greeting"
        
        # 支持的音频格式
        self.supported_formats = [".wav", ".mp3", ".ogg", ".m4a"]

    def extract_sound_type_from_text(self, text):
        """
        从文本中提取猫叫声类型
        根据提示词模板，只通过标准标签格式识别：[sound:类型]
        LLM应该在回复中包含标签，且只包含标签，不包含其他内容
        回答总长度不超过35个字符
        
        返回: 16种分类之一或默认类型
        """
        if not isinstance(text, str) or not text:
            logger.bind(tag=TAG).debug(
                f"无法识别猫叫声类型，使用默认类型: {self.default_sound_type}"
            )
            return self.default_sound_type
        
        # 验证文本长度（根据提示词模板：回答总长度不超过35个字符）
        if len(text) > 35:
            logger.bind(tag=TAG).warning(
                f"文本长度超过35个字符（实际长度: {len(text)}），可能不符合提示词要求"
            )
        
        # 根据提示词模板，只支持标准格式：[sound:01_positive_greeting]
        # 格式：方括号内 sound: 后跟类型名称（下划线分隔）
        # 注意：提示词要求每个回复必须包含且只包含一个声音类型标签，不包含其他内容
        # 支持多种格式以容错：标准格式、缺少开头括号、缺少下划线等
        sound_patterns = [
            r'\[sound[:\s]+([\w_]+)\]',  # 标准格式：[sound:01_positive_greeting]
            r'sound[:\s]+([\w_]+)\]',    # 缺少开头括号：sound:01_positive_greeting]
            r'\[sound[:\s]+([\w_]+)',    # 缺少结尾括号：[sound:01_positive_greeting
            r'sound[:\s]+([\w_]+)',      # 缺少两个括号：sound:01_positive_greeting
        ]
        
        valid_types = [
            "01_positive_greeting", "01_positive_affectionate", "01_positive_loving",
            "01_positive_inviting_play", "01_positive_awake_stretch",
            "02_demand_missing", "02_demand_curious", "02_demand_eating_happily",
            "03_warning_annoyed", "03_warning_angry_growl", "03_warning_aggressive_hiss",
            "03_warning_mating_call",
            "04_stress_concerned_inquiry", "04_stress_sneeze", "04_stress_whining",
            "04_stress_scared_scream"
        ]
        
        # 尝试多种格式查找标签
        matches = []
        for pattern in sound_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                break
        
        if matches:
            # 检查是否有多个标签（提示词要求只包含一个标签）
            if len(matches) > 1:
                logger.bind(tag=TAG).warning(
                    f"发现多个声音类型标签（共{len(matches)}个），提示词要求只包含一个标签"
                )
            
            sound_type_raw = matches[0].strip()
            
            # 尝试修复常见的格式问题：缺少下划线的情况
            # 例如：01positivegreeting -> 01_positive_greeting
            sound_type_fixed = sound_type_raw
            if not '_' in sound_type_raw and len(sound_type_raw) > 2:
                # 尝试匹配：01positivegreeting -> 01_positive_greeting
                # 查找以数字开头的模式
                number_match = re.match(r'^(\d{2})([a-z]+)([a-z_]+)?$', sound_type_raw, re.IGNORECASE)
                if number_match:
                    prefix = number_match.group(1)
                    # 尝试在常见位置插入下划线
                    for valid_type in valid_types:
                        if valid_type.startswith(prefix) and valid_type.replace('_', '').lower() == sound_type_raw.lower():
                            sound_type_fixed = valid_type
                            logger.bind(tag=TAG).info(
                                f"自动修复标签格式: {sound_type_raw} -> {sound_type_fixed}"
                            )
                            break
            
            # 验证是否为有效的16种类型之一
            sound_type_to_check = sound_type_fixed
            if sound_type_to_check.lower() in [t.lower() for t in valid_types]:
                # 返回标准格式（保持大小写一致）
                for valid_type in valid_types:
                    if sound_type_to_check.lower() == valid_type.lower():
                        logger.bind(tag=TAG).debug(f"从文本中识别到猫叫声类型标签: {valid_type}")
                        return valid_type
            else:
                logger.bind(tag=TAG).warning(
                    f"识别到无效的声音类型标签: {sound_type_raw}（修复后: {sound_type_fixed}），使用默认类型"
                )
        else:
            # 如果没有找到标签，检查文本是否为空或只包含空白字符
            text_stripped = text.strip()
            if text_stripped:
                logger.bind(tag=TAG).warning(
                    f"未找到声音类型标签，文本内容: '{text_stripped[:50]}...'，使用默认类型"
                )
            else:
                logger.bind(tag=TAG).debug(f"文本为空，使用默认类型: {self.default_sound_type}")
        
        # 如果没有找到有效标签，使用默认类型
        logger.bind(tag=TAG).debug(f"使用默认类型: {self.default_sound_type}")
        return self.default_sound_type

    def get_cat_sound_file(self, sound_type):
        """
        根据猫叫声类型获取猫叫声文件
        返回: 音频文件路径，如果找不到则返回None
        """
        # 尝试多种文件夹名称格式（原样、小写、首字母大写、全大写）
        # 新格式使用下划线，如：01_positive_greeting
        possible_dirs = [
            os.path.join(self.cat_sounds_dir, sound_type),  # 原样：01_positive_greeting
            os.path.join(self.cat_sounds_dir, sound_type.lower()),  # 全小写
            os.path.join(self.cat_sounds_dir, sound_type.upper()),  # 全大写
        ]
        
        sound_dir = None
        for dir_path in possible_dirs:
            if os.path.exists(dir_path):
                sound_dir = dir_path
                logger.bind(tag=TAG).debug(f"找到猫叫声文件夹: {dir_path}")
                break
        
        if not sound_dir:
            logger.bind(tag=TAG).warning(
                f"猫叫声类型文件夹不存在（已尝试: {', '.join(possible_dirs)}），尝试使用默认类型"
            )
            # 尝试使用默认类型
            if sound_type != self.default_sound_type:
                default_possible_dirs = [
                    os.path.join(self.cat_sounds_dir, self.default_sound_type),  # 原样
                    os.path.join(self.cat_sounds_dir, self.default_sound_type.lower()),  # 全小写
                    os.path.join(self.cat_sounds_dir, self.default_sound_type.upper()),  # 全大写
                ]
                for dir_path in default_possible_dirs:
                    if os.path.exists(dir_path):
                        sound_dir = dir_path
                        logger.bind(tag=TAG).info(
                            f"使用默认猫叫声文件夹: {dir_path}（原请求类型: {sound_type}）"
                        )
                        break
            
            # 如果默认类型也找不到，返回None
            if not sound_dir:
                logger.bind(tag=TAG).error(
                    f"猫叫声类型文件夹不存在（已尝试: {', '.join(possible_dirs)}），"
                    f"默认类型文件夹也不存在（已尝试: {', '.join(default_possible_dirs) if sound_type != self.default_sound_type else 'N/A'}）"
                )
                return None
        
        # 获取该猫叫声类型文件夹下的所有音频文件
        audio_files = []
        for file in os.listdir(sound_dir):
            file_path = os.path.join(sound_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in self.supported_formats:
                    audio_files.append(file_path)
        
        if not audio_files:
            logger.bind(tag=TAG).warning(
                f"猫叫声类型文件夹 {sound_dir} 中没有找到音频文件"
            )
            return None
        
        # 随机选择一个音频文件
        selected_file = random.choice(audio_files)
        logger.bind(tag=TAG).info(
            f"为猫叫声类型 {sound_type} 选择了文件: {selected_file}"
        )
        return selected_file

    async def text_to_speak(self, text, output_file):
        """
        将文本转换为猫叫声
        根据提示词模板，从文本中提取声音类型标签 [sound:类型]，
        然后返回对应的猫叫声文件
        
        提示词要求：
        - 每个回复必须包含且只包含一个声音类型标签，不包含其他内容
        - 标签必须使用正确的格式，系统才能识别
        - 如果无法确定情绪，使用默认类型：01_positive_greeting
        - 回答总长度不超过35个字符
        """
        # 从文本中提取猫叫声类型
        sound_type = self.extract_sound_type_from_text(text)
        
        # 获取对应的猫叫声文件
        cat_sound_file = self.get_cat_sound_file(sound_type)
        
        if not cat_sound_file:
            logger.bind(tag=TAG).error(
                f"无法找到猫叫声类型 {sound_type} 对应的文件"
            )
            raise FileNotFoundError(
                f"无法找到猫叫声类型 {sound_type} 对应的文件，"
                f"请确保在 {os.path.join(self.cat_sounds_dir, sound_type)} 文件夹中添加音频文件"
            )
        
        # 如果指定了输出文件，复制猫叫声文件到输出位置
        if output_file:
            import shutil
            shutil.copy2(cat_sound_file, output_file)
            logger.bind(tag=TAG).info(
                f"已将猫叫声文件复制到: {output_file}"
            )
            return None
        else:
            # 返回音频文件的字节数据
            with open(cat_sound_file, "rb") as f:
                audio_data = f.read()
            logger.bind(tag=TAG).info(
                f"返回猫叫声音频数据，大小: {len(audio_data)} 字节"
            )
            return audio_data


import os
import re
import random
import tempfile
from pydub import AudioSegment
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

    def extract_sound_types_from_text(self, text):
        """
        从文本中提取猫叫声类型（支持多个标签）
        根据提示词模板，通过标准标签格式识别：[sound:类型]
        现在支持多个标签，可以组合多个音频文件，让猫的情感更丰富
        
        返回: 标签类型列表，如果未找到则返回包含默认类型的列表
        """
        if not isinstance(text, str) or not text:
            logger.bind(tag=TAG).debug(
                f"无法识别猫叫声类型，使用默认类型: {self.default_sound_type}"
            )
            return [self.default_sound_type]
        
        valid_types = [
            "01_positive_greeting", "01_positive_affectionate", "01_positive_loving",
            "01_positive_inviting_play", "01_positive_awake_stretch",
            "02_demand_missing", "02_demand_curious", "02_demand_eating_happily",
            "03_warning_annoyed", "03_warning_angry_growl", "03_warning_aggressive_hiss",
            "03_warning_mating_call",
            "04_stress_concerned_inquiry", "04_stress_sneeze", "04_stress_whining",
            "04_stress_scared_scream"
        ]
        
        # 根据提示词模板，支持标准格式：[sound:01_positive_greeting]
        # 格式：方括号内 sound: 后跟类型名称（下划线分隔）
        # 支持多种格式以容错：标准格式、缺少开头括号、缺少下划线等
        sound_patterns = [
            r'\[sound[:\s]+([\w_]+)\]',  # 标准格式：[sound:01_positive_greeting]
            r'sound[:\s]+([\w_]+)\]',    # 缺少开头括号：sound:01_positive_greeting]
            r'\[sound[:\s]+([\w_]+)',    # 缺少结尾括号：[sound:01_positive_greeting
            r'sound[:\s]+([\w_]+)',      # 缺少两个括号：sound:01_positive_greeting
        ]
        
        # 使用所有格式查找所有标签，确保不遗漏任何标签
        all_matches = []
        for pattern in sound_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                all_matches.extend(matches)
        
        # 去重并保持顺序
        unique_matches = []
        seen = set()
        for match in all_matches:
            match_lower = match.strip().lower()
            if match_lower not in seen:
                seen.add(match_lower)
                unique_matches.append(match.strip())
        
        if unique_matches:
            logger.bind(tag=TAG).info(
                f"从文本中识别到 {len(unique_matches)} 个声音类型标签: {unique_matches}"
            )
            
            # 验证并修复所有标签
            valid_sound_types = []
            for sound_type_raw in unique_matches:
                # 尝试修复常见的格式问题：缺少下划线的情况
                sound_type_fixed = sound_type_raw
                if not '_' in sound_type_raw and len(sound_type_raw) > 2:
                    number_match = re.match(r'^(\d{2})([a-z]+)([a-z_]+)?$', sound_type_raw, re.IGNORECASE)
                    if number_match:
                        prefix = number_match.group(1)
                        for valid_type in valid_types:
                            if valid_type.startswith(prefix) and valid_type.replace('_', '').lower() == sound_type_raw.lower():
                                sound_type_fixed = valid_type
                                logger.bind(tag=TAG).info(
                                    f"自动修复标签格式: {sound_type_raw} -> {sound_type_fixed}"
                                )
                                break
                
                # 验证是否为有效的16种类型之一
                if sound_type_fixed.lower() in [t.lower() for t in valid_types]:
                    for valid_type in valid_types:
                        if sound_type_fixed.lower() == valid_type.lower():
                            valid_sound_types.append(valid_type)
                            break
                else:
                    logger.bind(tag=TAG).warning(
                        f"识别到无效的声音类型标签: {sound_type_raw}（修复后: {sound_type_fixed}），跳过"
                    )
            
            if valid_sound_types:
                logger.bind(tag=TAG).debug(
                    f"提取到 {len(valid_sound_types)} 个有效标签: {valid_sound_types}"
                )
                return valid_sound_types
            else:
                logger.bind(tag=TAG).warning("所有标签都无效，使用默认类型")
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
        return [self.default_sound_type]

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

    def merge_audio_files(self, audio_files):
        """
        合并多个音频文件
        
        参数:
            audio_files: 音频文件路径列表
        
        返回:
            合并后的音频数据（字节）
        """
        if not audio_files:
            raise ValueError("音频文件列表为空")
        
        if len(audio_files) == 1:
            # 如果只有一个文件，直接返回
            with open(audio_files[0], "rb") as f:
                return f.read()
        
        try:
            # 加载第一个音频文件
            combined = AudioSegment.from_file(audio_files[0])
            
            # 依次合并其他音频文件
            for audio_file in audio_files[1:]:
                audio_segment = AudioSegment.from_file(audio_file)
                # 在音频之间添加短暂静音（100毫秒），让过渡更自然
                combined = combined + AudioSegment.silent(duration=100) + audio_segment
            
            # 将合并后的音频导出为临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                combined.export(tmp_file.name, format="wav")
                tmp_path = tmp_file.name
            
            # 读取合并后的音频数据
            with open(tmp_path, "rb") as f:
                audio_data = f.read()
            
            # 删除临时文件
            try:
                os.unlink(tmp_path)
            except Exception as e:
                logger.bind(tag=TAG).warning(f"删除临时文件失败: {e}")
            
            logger.bind(tag=TAG).info(
                f"成功合并 {len(audio_files)} 个音频文件，总大小: {len(audio_data)} 字节"
            )
            return audio_data
            
        except Exception as e:
            logger.bind(tag=TAG).error(f"合并音频文件时出错: {e}")
            # 如果合并失败，尝试返回第一个文件
            logger.bind(tag=TAG).warning("合并失败，返回第一个音频文件")
            with open(audio_files[0], "rb") as f:
                return f.read()

    async def text_to_speak(self, text, output_file):
        """
        将文本转换为猫叫声
        根据提示词模板，从文本中提取声音类型标签 [sound:类型]，
        支持多个标签，可以组合多个音频文件，让猫的情感更丰富
        
        提示词要求：
        - 可以在回复中包含一个或多个声音类型标签
        - 标签必须使用正确的格式：[sound:类型]
        - 多个标签会被依次播放，让情感表达更丰富
        - 如果无法确定情绪，使用默认类型：01_positive_greeting
        """
        # 从文本中提取所有猫叫声类型标签
        sound_types = self.extract_sound_types_from_text(text)
        
        # 获取每个类型对应的猫叫声文件
        cat_sound_files = []
        for sound_type in sound_types:
            cat_sound_file = self.get_cat_sound_file(sound_type)
            if cat_sound_file:
                cat_sound_files.append(cat_sound_file)
            else:
                logger.bind(tag=TAG).error(
                    f"无法找到猫叫声类型 {sound_type} 对应的文件"
                )
                # 如果某个类型找不到文件，尝试使用默认类型
                if sound_type != self.default_sound_type:
                    default_file = self.get_cat_sound_file(self.default_sound_type)
                    if default_file:
                        cat_sound_files.append(default_file)
                        logger.bind(tag=TAG).warning(
                            f"类型 {sound_type} 的文件不存在，使用默认类型 {self.default_sound_type}"
                        )
        
        if not cat_sound_files:
            raise FileNotFoundError(
                f"无法找到任何猫叫声文件，"
                f"请确保在 {self.cat_sounds_dir} 文件夹中添加音频文件"
            )
        
        # 如果只有一个文件，直接处理
        if len(cat_sound_files) == 1:
            if output_file:
                import shutil
                shutil.copy2(cat_sound_files[0], output_file)
                logger.bind(tag=TAG).info(
                    f"已将猫叫声文件复制到: {output_file}"
                )
                return None
            else:
                with open(cat_sound_files[0], "rb") as f:
                    audio_data = f.read()
                logger.bind(tag=TAG).info(
                    f"返回猫叫声音频数据，大小: {len(audio_data)} 字节"
                )
                return audio_data
        else:
            # 合并多个音频文件
            merged_audio_data = self.merge_audio_files(cat_sound_files)
            
            if output_file:
                with open(output_file, "wb") as f:
                    f.write(merged_audio_data)
                logger.bind(tag=TAG).info(
                    f"已将合并后的猫叫声文件保存到: {output_file}"
                )
                return None
            else:
                logger.bind(tag=TAG).info(
                    f"返回合并后的猫叫声音频数据，大小: {len(merged_audio_data)} 字节"
                )
                return merged_audio_data


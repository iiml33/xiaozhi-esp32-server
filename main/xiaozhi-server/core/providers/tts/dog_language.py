import os
import re
import random
from config.logger import setup_logging
from core.providers.tts.base import TTSProviderBase

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        # 犬叫声文件夹路径
        self.dog_sounds_dir = config.get("dog_sounds_dir", "config/dog_sounds")
        # 确保文件夹存在
        if not os.path.exists(self.dog_sounds_dir):
            os.makedirs(self.dog_sounds_dir)
            logger.bind(tag=TAG).warning(
                f"犬叫声文件夹不存在，已创建: {self.dog_sounds_dir}，请添加犬叫声文件"
            )
        
        # 犬叫声类型到情绪关键词的映射
        # 新分类系统：4大类16种具体类型
        # 😊 积极与亲昵 (01_positive)
        # 🗣️ 需求与沟通 (02_demand)
        # ⚠️ 警告与不适 (03_warning)
        # 😿 压力与痛苦 (04_stress)
        
        self.dog_sound_keywords = {
            # 😊 积极与亲昵 (01_positive)
            "01_positive_greeting": {
                "zh": ["打招呼", "问候", "你好", "回来", "见面", "欢迎", "友好", "轻快", "短促", "轻盈"],
                "en": ["greeting", "hello", "hi", "welcome", "friendly", "light", "short", "quick"]
            },
            "01_positive_affectionate": {
                "zh": ["撒娇", "亲昵", "温柔", "拐弯", "黏人", "卖萌", "可爱", "亲热", "依恋"],
                "en": ["affectionate", "cute", "sweet", "gentle", "loving", "cuddly", "adorable", "tender"]
            },
            "01_positive_loving": {
                "zh": ["喜欢", "爱你", "爱意", "满足", "幸福", "开心", "快乐", "满足", "表达爱"],
                "en": ["loving", "love", "affection", "happy", "content", "satisfied", "joyful", "pleased"]
            },
            "01_positive_inviting_play": {
                "zh": ["邀请", "一起玩", "玩耍", "游戏", "轻快", "活泼", "兴奋", "互动", "想玩"],
                "en": ["inviting", "play", "game", "playful", "active", "excited", "interactive", "fun"]
            },
            "01_positive_awake_stretch": {
                "zh": ["睡醒", "慵懒", "伸懒腰", "舒服", "放松", "醒来", "打哈欠", "舒展"],
                "en": ["awake", "stretch", "lazy", "comfortable", "relaxed", "waking", "yawn", "stretching"]
            },
            # 🗣️ 需求与沟通 (02_demand)
            "02_demand_missing": {
                "zh": ["思念", "想念", "想你", "主人", "激动", "拉长", "强烈需求", "渴望", "呼唤"],
                "en": ["missing", "miss", "longing", "owner", "excited", "long", "demand", "craving", "call"]
            },
            "02_demand_curious": {
                "zh": ["疑问", "好奇", "询问", "什么", "为什么", "疑惑", "想知道", "探索"],
                "en": ["curious", "question", "wonder", "what", "why", "inquiry", "explore", "ask"]
            },
            "02_demand_eating_happily": {
                "zh": ["吃饭", "满足", "满意", "好吃", "享受", "进食", "用餐", "饱足", "美味"],
                "en": ["eating", "happily", "satisfied", "delicious", "enjoy", "meal", "food", "yummy", "tasty"]
            },
            # ⚠️ 警告与不适 (03_warning)
            "03_warning_annoyed": {
                "zh": ["不耐烦", "责怪", "不满", "短促", "重音", "烦躁", "抱怨", "抗议"],
                "en": ["annoyed", "impatient", "complaint", "short", "heavy", "irritated", "protest", "grumble"]
            },
            "03_warning_angry_growl": {
                "zh": ["生气", "叫骂", "愤怒", "警告", "低吼", "连续", "喉咙", "威胁", "不满", "咆哮"],
                "en": ["angry", "growl", "warning", "threat", "continuous", "throat", "mad", "furious", "bark"]
            },
            "03_warning_aggressive_hiss": {
                "zh": ["想打人", "攻击", "尖利", "持续", "防御", "危险", "警告", "攻击性", "狂吠"],
                "en": ["aggressive", "attack", "sharp", "continuous", "defense", "danger", "hostile", "bark"]
            },
            "03_warning_mating_call": {
                "zh": ["求偶", "发情", "粗粝", "长鸣", "不好听", "交配", "繁殖", "发情期"],
                "en": ["mating", "call", "heat", "rough", "long", "breeding", "reproduction", "estrus"]
            },
            # 😿 压力与痛苦 (04_stress)
            "04_stress_concerned_inquiry": {
                "zh": ["关心", "好奇询问", "拐弯", "拉长", "询问", "谨慎", "担心", "关切", "询问"],
                "en": ["concerned", "inquiry", "question", "careful", "worried", "care", "ask", "inquire"]
            },
            "04_stress_sneeze": {
                "zh": ["打喷嚏", "喷嚏", "刺激", "过敏", "反应", "阿嚏"],
                "en": ["sneeze", "sneezing", "irritation", "allergy", "reaction", "achoo"]
            },
            "04_stress_whining": {
                "zh": ["委屈", "讨好", "短促", "试探", "可怜", "哀求", "诉苦", "抱怨", "呜咽"],
                "en": ["whining", "pleading", "short", "tentative", "pitiful", "begging", "complaining", "whimper"]
            },
            "04_stress_scared_scream": {
                "zh": ["害怕", "尖叫", "惊吓", "受惊", "恐惧", "极高音调", "短促", "惊恐"],
                "en": ["scared", "scream", "frightened", "fear", "high pitch", "short", "terrified", "panic"]
            }
        }
        
        # 默认犬叫声类型（如果无法识别）
        self.default_sound_type = config.get("default_sound_type", "01_positive_greeting")
        
        # 支持的音频格式
        self.supported_formats = [".wav", ".mp3", ".ogg", ".m4a"]

    def extract_sound_type_from_text(self, text):
        """
        从文本中提取犬叫声类型
        只通过标签格式识别，LLM应该在回复中包含标签
        返回: 新的16种分类之一或默认类型
        """
        if not isinstance(text, str) or not text:
            logger.bind(tag=TAG).debug(
                f"无法识别犬叫声类型，使用默认类型: {self.default_sound_type}"
            )
            return self.default_sound_type
        
        # 检查犬叫声类型标签，例如: [sound:01_positive_greeting] 或 <sound>02_demand_missing</sound>
        sound_patterns = [
            r'\[sound[:\s]+([\w_]+)\]',
            r'<sound>([\w_]+)</sound>',
            r'犬叫[:\s]+([\w_]+)',
            r'狗叫[:\s]+([\w_]+)',
            r'sound[:\s]+([\w_]+)',
            r'叫声[:\s]+([\w_]+)'
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
        
        for pattern in sound_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sound_type = match.group(1).lower()
                # 支持简写格式（不带前缀），如 greeting 自动匹配 01_positive_greeting
                if sound_type in valid_types:
                    logger.bind(tag=TAG).debug(f"从文本中识别到犬叫声类型标签: {sound_type}")
                    return sound_type
                # 尝试简写匹配
                for valid_type in valid_types:
                    if sound_type == valid_type.split('_')[-1]:
                        logger.bind(tag=TAG).debug(f"从文本中识别到犬叫声类型标签（简写）: {sound_type} -> {valid_type}")
                        return valid_type
        
        # 如果没有找到标签，使用默认类型
        logger.bind(tag=TAG).debug(f"未找到犬叫声类型标签，使用默认类型: {self.default_sound_type}")
        return self.default_sound_type

    def get_dog_sound_file(self, sound_type):
        """
        根据犬叫声类型获取犬叫声文件
        返回: 音频文件路径，如果找不到则返回None
        """
        # 尝试多种文件夹名称格式（原样、小写、首字母大写、全大写）
        # 新格式使用下划线，如：01_positive_greeting
        possible_dirs = [
            os.path.join(self.dog_sounds_dir, sound_type),  # 原样：01_positive_greeting
            os.path.join(self.dog_sounds_dir, sound_type.lower()),  # 全小写
            os.path.join(self.dog_sounds_dir, sound_type.upper()),  # 全大写
        ]
        
        sound_dir = None
        for dir_path in possible_dirs:
            if os.path.exists(dir_path):
                sound_dir = dir_path
                logger.bind(tag=TAG).debug(f"找到犬叫声文件夹: {dir_path}")
                break
        
        if not sound_dir:
            logger.bind(tag=TAG).warning(
                f"犬叫声类型文件夹不存在（已尝试: {', '.join(possible_dirs)}），请创建该文件夹并添加犬叫声文件"
            )
            # 尝试使用默认类型
            if sound_type != self.default_sound_type:
                default_possible_dirs = [
                    os.path.join(self.dog_sounds_dir, self.default_sound_type),
                    os.path.join(self.dog_sounds_dir, self.default_sound_type.lower()),
                    os.path.join(self.dog_sounds_dir, self.default_sound_type.upper()),
                ]
                for dir_path in default_possible_dirs:
                    if os.path.exists(dir_path):
                        sound_dir = dir_path
                        logger.bind(tag=TAG).debug(f"使用默认犬叫声文件夹: {dir_path}")
                        break
                
                if not sound_dir:
                    logger.bind(tag=TAG).error(
                        f"默认犬叫声类型文件夹也不存在（已尝试: {', '.join(default_possible_dirs)}）"
                    )
                    return None
        
        # 获取该犬叫声类型文件夹下的所有音频文件
        audio_files = []
        for file in os.listdir(sound_dir):
            file_path = os.path.join(sound_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in self.supported_formats:
                    audio_files.append(file_path)
        
        if not audio_files:
            logger.bind(tag=TAG).warning(
                f"犬叫声类型文件夹 {sound_dir} 中没有找到音频文件"
            )
            return None
        
        # 随机选择一个音频文件
        selected_file = random.choice(audio_files)
        logger.bind(tag=TAG).info(
            f"为犬叫声类型 {sound_type} 选择了文件: {selected_file}"
        )
        return selected_file

    async def text_to_speak(self, text, output_file):
        """
        将文本转换为犬叫声
        实际上是根据文本中的情绪和上下文返回对应的犬叫声文件
        """
        # 从文本中提取犬叫声类型
        sound_type = self.extract_sound_type_from_text(text)
        
        # 获取对应的犬叫声文件
        dog_sound_file = self.get_dog_sound_file(sound_type)
        
        if not dog_sound_file:
            logger.bind(tag=TAG).error(
                f"无法找到犬叫声类型 {sound_type} 对应的文件"
            )
            raise FileNotFoundError(
                f"无法找到犬叫声类型 {sound_type} 对应的文件，"
                f"请确保在 {os.path.join(self.dog_sounds_dir, sound_type)} 文件夹中添加音频文件"
            )
        
        # 如果指定了输出文件，复制犬叫声文件到输出位置
        if output_file:
            import shutil
            shutil.copy2(dog_sound_file, output_file)
            logger.bind(tag=TAG).info(
                f"已将犬叫声文件复制到: {output_file}"
            )
            return None
        else:
            # 返回音频文件的字节数据
            with open(dog_sound_file, "rb") as f:
                audio_data = f.read()
            logger.bind(tag=TAG).info(
                f"返回犬叫声音频数据，大小: {len(audio_data)} 字节"
            )
            return audio_data

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
        # 猫叫声文件夹路径
        self.cat_sounds_dir = config.get("cat_sounds_dir", "config/cat_sounds")
        # 确保文件夹存在
        if not os.path.exists(self.cat_sounds_dir):
            os.makedirs(self.cat_sounds_dir)
            logger.bind(tag=TAG).warning(
                f"猫叫声文件夹不存在，已创建: {self.cat_sounds_dir}，请添加猫叫声文件"
            )
        
        # 猫叫声类型到情绪关键词的映射
        # 1. 喵（Meow）- 求关注、撒娇、期待、轻微抱怨
        # 2. 呼噜（Purr）- 放松、满足、安全感
        # 3. 咕噜咕噜/颤音（Trill）- 友好、欢迎
        # 4. 咔咔/啾啾（Chattering）- 兴奋、专注、略挫败
        # 5. 哈气（Hiss）- 恐惧、防御、警告
        # 6. 低吼/咆哮（Growl）- 威胁、愤怒、防御升级
        # 7. 嚎叫/长嗷（Yowl）- 发情、压力、焦虑、疼痛
        # 8. 尖叫/惨叫（Scream）- 突然疼痛、强烈惊吓
        # 9. 嘟嘟嘟不满声/咕哝（Mutter）- 不耐烦、轻度烦躁
        
        self.cat_sound_keywords = {
            "meow": {
                "zh": ["求关注", "撒娇", "期待", "喂食", "开门", "轻微抱怨", "友好", "打招呼", "想互动", 
                       "不耐烦", "要求", "焦虑", "受惊", "不舒服", "喵", "叫"],
                "en": ["attention", "cute", "expect", "feed", "open", "slight", "friendly", "greet", 
                       "interact", "impatient", "demand", "anxious", "startled", "uncomfortable", "meow"]
            },
            "purr": {
                "zh": ["放松", "满足", "安全感", "舒适", "惬意", "安心", "呼噜"],
                "en": ["relaxed", "satisfied", "safe", "comfortable", "content", "secure", "purr"]
            },
            "trill": {
                "zh": ["友好", "欢迎", "想你", "带路", "回家", "绕", "咕噜", "颤音"],
                "en": ["friendly", "welcome", "miss", "guide", "home", "around", "trill", "chirrup"]
            },
            "chattering": {
                "zh": ["兴奋", "专注", "挫败", "捕猎", "想抓", "咔咔", "啾啾"],
                "en": ["excited", "focused", "frustrated", "hunt", "catch", "chattering", "chirping"]
            },
            "hiss": {
                "zh": ["恐惧", "防御", "警告", "不安全", "别靠近", "哈气"],
                "en": ["fear", "defense", "warning", "unsafe", "away", "hiss"]
            },
            "growl": {
                "zh": ["威胁", "愤怒", "防御升级", "领地", "冲突", "低吼", "咆哮"],
                "en": ["threat", "angry", "defense", "territory", "conflict", "growl"]
            },
            "yowl": {
                "zh": ["发情", "压力", "焦虑", "寻找", "疼痛", "不适", "嚎叫", "长嗷"],
                "en": ["heat", "stress", "anxiety", "search", "pain", "discomfort", "yowl", "howl"]
            },
            "scream": {
                "zh": ["突然疼痛", "强烈惊吓", "受伤", "被卡", "尖叫", "惨叫"],
                "en": ["sudden pain", "strong shock", "injured", "stuck", "scream"]
            },
            "mutter": {
                "zh": ["不耐烦", "烦躁", "抗议", "被打扰", "嘟嘟", "咕哝"],
                "en": ["impatient", "annoyed", "protest", "disturbed", "mutter", "grumble"]
            }
        }
        
        # 默认猫叫声类型（如果无法识别）
        self.default_sound_type = config.get("default_sound_type", "meow")
        
        # 支持的音频格式
        self.supported_formats = [".wav", ".mp3", ".ogg", ".m4a"]

    def extract_sound_type_from_text(self, text):
        """
        从文本中提取猫叫声类型
        返回: "meow", "purr", "trill", "chattering", "hiss", "growl", "yowl", "scream", "mutter" 或默认类型
        """
        if not isinstance(text, str) or not text:
            logger.bind(tag=TAG).debug(
                f"无法识别猫叫声类型，使用默认类型: {self.default_sound_type}"
            )
            return self.default_sound_type
        
        text_lower = text.lower()
        
        # 优先级1: 检查猫叫声类型标签，例如: [sound:meow] 或 <sound>purr</sound>
        sound_patterns = [
            r'\[sound[:\s]+(\w+)\]',
            r'<sound>(\w+)</sound>',
            r'猫叫[:\s]+(\w+)',
            r'sound[:\s]+(\w+)',
            r'叫声[:\s]+(\w+)'
        ]
        
        for pattern in sound_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sound_type = match.group(1).lower()
                valid_types = ["meow", "purr", "trill", "chattering", "hiss", "growl", "yowl", "scream", "mutter"]
                if sound_type in valid_types:
                    logger.bind(tag=TAG).debug(f"从文本中识别到猫叫声类型标签: {sound_type}")
                    return sound_type
        
        # 优先级2: 检查中文关键词（按优先级顺序，从最具体到最通用）
        # 先检查最严重的（scream, yowl, growl, hiss）
        priority_order = ["scream", "yowl", "growl", "hiss", "chattering", "mutter", "trill", "purr", "meow"]
        
        for sound_type in priority_order:
            keywords = self.cat_sound_keywords.get(sound_type, {})
            for keyword in keywords.get("zh", []):
                if keyword in text:
                    logger.bind(tag=TAG).debug(f"从文本中识别到猫叫声类型: {sound_type} (关键词: {keyword})")
                    return sound_type
        
        # 优先级3: 检查英文关键词
        for sound_type in priority_order:
            keywords = self.cat_sound_keywords.get(sound_type, {})
            for keyword in keywords.get("en", []):
                if keyword.lower() in text_lower:
                    logger.bind(tag=TAG).debug(f"从文本中识别到猫叫声类型: {sound_type} (关键词: {keyword})")
                    return sound_type
        
        logger.bind(tag=TAG).debug(f"无法识别猫叫声类型，使用默认类型: {self.default_sound_type}")
        return self.default_sound_type

    def get_cat_sound_file(self, sound_type):
        """
        根据猫叫声类型获取猫叫声文件
        返回: 音频文件路径，如果找不到则返回None
        """
        sound_dir = os.path.join(self.cat_sounds_dir, sound_type)
        
        if not os.path.exists(sound_dir):
            logger.bind(tag=TAG).warning(
                f"猫叫声类型文件夹不存在: {sound_dir}，请创建该文件夹并添加猫叫声文件"
            )
            # 尝试使用默认类型
            if sound_type != self.default_sound_type:
                sound_dir = os.path.join(self.cat_sounds_dir, self.default_sound_type)
                if not os.path.exists(sound_dir):
                    logger.bind(tag=TAG).error(
                        f"默认猫叫声类型文件夹也不存在: {sound_dir}"
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
        实际上是根据文本中的情绪和上下文返回对应的猫叫声文件
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


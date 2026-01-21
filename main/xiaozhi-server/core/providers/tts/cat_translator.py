import os
import re
import random
from config.logger import setup_logging
from config.config_loader import get_project_dir
from core.providers.tts.base import TTSProviderBase
from core.utils import llm

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        
        # 猫翻译声音文件夹路径（独立于cat_language）
        # 支持挂载方式：如果配置为绝对路径，则直接使用（适用于Docker挂载）；否则基于项目根目录
        cat_sounds_dir_rel = config.get("cat_sounds_dir", "config/cat_translator_sounds")
        # 将相对路径转换为绝对路径（基于项目根目录）
        if os.path.isabs(cat_sounds_dir_rel):
            # 绝对路径：直接使用（适用于Docker挂载方式）
            self.cat_sounds_dir = cat_sounds_dir_rel
            # 挂载目录不应该自动创建，只检查是否存在
            if not os.path.exists(self.cat_sounds_dir):
                logger.bind(tag=TAG).warning(
                    f"猫翻译声音挂载目录不存在: {self.cat_sounds_dir}，请检查Docker挂载配置或确保目录存在"
                )
        else:
            # 相对路径：基于项目根目录
            self.cat_sounds_dir = os.path.join(get_project_dir(), cat_sounds_dir_rel)
            # 相对路径目录不存在时自动创建
            if not os.path.exists(self.cat_sounds_dir):
                os.makedirs(self.cat_sounds_dir)
                logger.bind(tag=TAG).warning(
                    f"猫翻译声音文件夹不存在，已创建: {self.cat_sounds_dir}，请添加猫叫声音频文件（独立于cat_language）"
                )
        
        # 获取LLM配置（用于判断用户指令类型）
        llm_config = config.get("llm_config", {})
        if not llm_config:
            raise ValueError("cat_translator需要配置llm_config用于判断指令类型，例如：\n"
                           "llm_config:\n"
                           "  type: openai\n"
                           "  api_key: 你的api_key\n"
                           "  model_name: gpt-3.5-turbo")
        
        llm_type = llm_config.get("type", "openai")
        self.llm = llm.create_instance(llm_type, llm_config)
        logger.bind(tag=TAG).info(f"初始化LLM指令识别器: {llm_type}")
        
        # 默认猫叫声类型（如果无法识别）
        # 固定使用 01_positive_greeting 作为默认类型，确保始终有效
        config_default_type = config.get("default_sound_type", "01_positive_greeting")
        valid_default_types = [
            "01_positive_greeting", "01_positive_affectionate", "01_positive_inviting_play",
            "02_demand_eating_happily", "02_demand_curious", "03_warning_annoyed"
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
        
        # 定义有效的文件夹名称列表（LLM只能返回这7个值之一）
        self.valid_folder_names = [
            "01_positive_greeting", 
            "01_positive_affectionate", 
            "01_positive_inviting_play",
            "02_demand_eating_happily",
            "02_demand_curious",
            "03_warning_annoyed",
            "default"
        ]
        
        # 构建LLM判断提示词
        self.instruction_prompt = self._build_instruction_prompt()
    
    def _build_instruction_prompt(self):
        """构建LLM判断指令类型的提示词"""
        valid_types_str = "、".join(self.valid_folder_names)
        
        prompt = f"""你是一个专业的指令识别器。根据用户对猫说的话，判断应该调用的文件夹名称。

## 核心任务
分析用户对猫说的话，识别指令意图，返回对应的文件夹名称。

## 可选的文件夹名称（只能返回以下7个之一，严格匹配）：

### 1. **01_positive_greeting** - 召唤/打招呼类
**使用场景**：召唤猫咪过来、打招呼、让猫咪到指定位置
**指令特征**：包含位置指示、召唤动作、问候语
**指令示例**：
- "过来"、"跟我走"、"这里"、"到这儿"
- "回去"、"进房间"、"过来这里"
- "你好呀"、"来这边"、"过来一下"
**相似指令**：任何让猫咪移动或靠近的指令

### 2. **01_positive_affectionate** - 夸奖/安抚类
**使用场景**：表扬猫咪、安抚情绪、表达关爱
**指令特征**：包含表扬词、安抚词、温柔语气
**指令示例**：
- "乖"、"真棒"、"好乖"、"真听话"
- "没事"、"不怕"、"别怕"、"没关系"
- "好孩子"、"真乖"、"乖宝宝"
**相似指令**：任何表扬、安慰、鼓励的指令

### 3. **01_positive_inviting_play** - 邀请玩耍类
**使用场景**：邀请猫咪一起玩耍、互动
**指令特征**：包含游戏、玩具、玩耍相关词汇
**指令示例**：
- "来玩"、"一起玩"、"玩玩具"
- "把玩具拿来"、"来玩球"、"玩一下"
**相似指令**：任何邀请玩耍、互动的指令

### 4. **02_demand_eating_happily** - 吃饭类
**使用场景**：叫猫咪吃饭、喂食
**指令特征**：包含吃饭、食物、喂食相关词汇
**指令示例**：
- "吃饭啦"、"吃饭了"、"来吃饭"
- "开饭了"、"吃饭饭"、"来吃"
**相似指令**：任何与吃饭、喂食相关的指令

### 5. **02_demand_curious** - 疑问/喝水类
**使用场景**：让猫咪喝水、询问、引起注意
**指令特征**：包含疑问、喝水、询问相关词汇
**指令示例**：
- "喝水"、"过来喝水"、"去喝水"
- "渴了吗"、"要不要喝水"
**相似指令**：任何与喝水、询问相关的指令

### 6. **03_warning_annoyed** - 制止/边界类
**使用场景**：制止猫咪行为、设定边界、警告
**指令特征**：包含否定词、制止词、警告语气
**指令示例**：
- "不可以"、"不要"、"不行"
- "停"、"停下"、"下来"
- "别动"、"不许"、"禁止"
**相似指令**：任何制止、警告、设定边界的指令

### 7. **default** - 无法判断时使用
**使用场景**：无法明确判断指令类型时
**使用条件**：指令不属于以上6类，或含义模糊不清

## 识别规则

### 优先级判断
1. **关键词匹配**：优先匹配明确的指令关键词
2. **语境理解**：结合上下文理解指令意图
3. **语气判断**：注意指令的语气（温柔/严厉）

### 常见误判避免
- "过来" → 01_positive_greeting（不是02_demand_curious）
- "乖" → 01_positive_affectionate（不是01_positive_greeting）
- "不要" → 03_warning_annoyed（不是01_positive_affectionate）

## 输出要求（严格遵循）：

1. **只能返回以下7个值之一（完全匹配，不区分大小写）：{valid_types_str}**
2. **只输出文件夹名称**，格式：`01_positive_greeting`（下划线分隔，全小写）
3. **不要添加任何解释、说明、标点符号或换行**
4. **不要使用引号包裹**
5. **如果无法判断，输出：`default`**
6. **输出格式示例**：`01_positive_greeting`

## 输出示例

用户输入："过来"
正确输出：01_positive_greeting

用户输入："真乖"
正确输出：01_positive_affectionate

用户输入："来玩球"
正确输出：01_positive_inviting_play

用户输入："吃饭了"
正确输出：02_demand_eating_happily

用户输入："去喝水"
正确输出：02_demand_curious

用户输入："不可以"
正确输出：03_warning_annoyed

用户输入："喵喵"
正确输出：default

## 用户输入："""
        return prompt
    
    async def _identify_command_type(self, user_input):
        """使用LLM判断用户输入的指令类型"""
        try:
            # 构建完整的提示词
            full_prompt = self.instruction_prompt + user_input.strip()
            
            # 调用LLM进行判断（使用类属性中的valid_folder_names）
            valid_types_str = "、".join(self.valid_folder_names)
            system_prompt = f"""你是一个专业的指令识别器，专门识别用户对猫说的话的指令类型。

核心任务：根据用户输入，只输出对应的文件夹名称。

可选的文件夹名称（只能返回以下7个之一，严格匹配）：
1. 01_positive_greeting - 召唤/打招呼类（如：过来、跟我走、这里）
2. 01_positive_affectionate - 夸奖/安抚类（如：乖、真棒、没事）
3. 01_positive_inviting_play - 邀请玩耍类（如：来玩、把玩具拿来）
4. 02_demand_eating_happily - 吃饭类（如：吃饭啦）
5. 02_demand_curious - 疑问/喝水类（如：喝水、过来喝水）
6. 03_warning_annoyed - 制止/边界类（如：不可以、不要、停）
7. default - 无法判断时使用

输出要求：
- 只能返回以下7个值之一（完全匹配，不区分大小写）：{valid_types_str}
- 只输出文件夹名称，格式：01_positive_greeting（下划线分隔，全小写）
- 不要添加任何解释、说明、标点符号或换行
- 不要使用引号包裹
- 如果无法判断，输出：default"""
            
            command_type = self.llm.response_no_stream(
                system_prompt=system_prompt,
                user_prompt=full_prompt
            )
            
            # 清理输出 - 提取文件夹名称
            command_type = command_type.strip()
            
            # 移除可能的解释性前缀和后缀
            prefixes_to_remove = [
                "指令类型：", "类型：", "结果：", "答案是：", "输出：", "文件夹：", "文件夹名称：",
                "Command Type:", "Type:", "Result:", "Answer:", "Output:", "Folder:", "Folder Name:",
                "返回：", "Return:", "识别结果：", "识别："
            ]
            for prefix in prefixes_to_remove:
                if command_type.startswith(prefix):
                    command_type = command_type[len(prefix):].strip()
            
            # 移除引号
            command_type = command_type.strip('"\'`')
            
            # 移除可能的JSON格式包装
            import json
            try:
                # 尝试解析JSON格式
                if command_type.startswith('{'):
                    parsed = json.loads(command_type)
                    if 'folder' in parsed:
                        command_type = parsed['folder']
                    elif 'type' in parsed:
                        command_type = parsed['type']
                    elif 'result' in parsed:
                        command_type = parsed['result']
            except:
                pass
            
            # 移除换行符和多余空格，只保留一行
            command_type = ' '.join(command_type.split()).strip()
            
            # 如果包含多行，只取第一行（文件夹名称应该在第一行）
            if '\n' in command_type:
                command_type = command_type.split('\n')[0].strip()
            
            # 提取可能的文件夹名称（匹配格式：数字_字母_字母或default）
            import re
            folder_pattern = r'\b(\d{2}_[a-z_]+|default)\b'
            match = re.search(folder_pattern, command_type, re.IGNORECASE)
            if match:
                command_type = match.group(1).lower()
            
            # 严格检查：必须是valid_folder_names中的7个值之一（完全匹配，不区分大小写）
            command_type_lower = command_type.lower()
            matched_type = None
            for valid_type in self.valid_folder_names:
                if command_type_lower == valid_type.lower():
                    matched_type = valid_type
                    break
            
            if matched_type:
                # 如果返回default，使用配置的默认类型
                if matched_type.lower() == "default":
                    matched_type = self.default_sound_type
                logger.bind(tag=TAG).info(f"LLM识别结果: {user_input} -> {matched_type}")
                return matched_type
            else:
                # LLM返回了无效值，使用默认类型
                logger.bind(tag=TAG).warning(f"LLM返回了无效的文件夹名称: {command_type}，有效值应为：{', '.join(self.valid_folder_names)}，使用默认类型: {self.default_sound_type}")
                return self.default_sound_type
            
        except Exception as e:
            logger.bind(tag=TAG).error(f"LLM判断指令类型失败: {e}，使用默认类型: {self.default_sound_type}")
            # 如果LLM判断失败，使用默认类型
            return self.default_sound_type
    
    def get_cat_sound_file(self, sound_type):
        """
        根据猫叫声类型获取猫叫声文件
        返回: 音频文件路径，如果找不到则返回None
        """
        # 尝试多种文件夹名称格式
        possible_dirs = [
            os.path.join(self.cat_sounds_dir, sound_type),
            os.path.join(self.cat_sounds_dir, sound_type.lower()),
            os.path.join(self.cat_sounds_dir, sound_type.upper()),
        ]
        
        sound_dir = None
        for dir_path in possible_dirs:
            if os.path.exists(dir_path):
                sound_dir = dir_path
                logger.bind(tag=TAG).debug(f"找到猫叫声文件夹: {dir_path}")
                break
        
        if not sound_dir:
            logger.bind(tag=TAG).warning(
                f"猫叫声类型文件夹不存在（已尝试: {', '.join(possible_dirs)}），请创建该文件夹并添加猫叫声文件"
            )
            # 尝试使用默认类型
            if sound_type != self.default_sound_type:
                default_possible_dirs = [
                    os.path.join(self.cat_sounds_dir, self.default_sound_type),
                    os.path.join(self.cat_sounds_dir, self.default_sound_type.lower()),
                    os.path.join(self.cat_sounds_dir, self.default_sound_type.upper()),
                ]
                for dir_path in default_possible_dirs:
                    if os.path.exists(dir_path):
                        sound_dir = dir_path
                        logger.bind(tag=TAG).debug(f"使用默认猫叫声文件夹: {dir_path}")
                        break
                
                if not sound_dir:
                    logger.bind(tag=TAG).error(
                        f"默认猫叫声类型文件夹也不存在（已尝试: {', '.join(default_possible_dirs)}）"
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
        将用户输入转换为猫叫声
        1. 使用LLM判断用户输入的指令类型
        2. 根据指令类型选择对应的猫叫声音频文件
        """
        try:
            # 步骤1: 使用LLM判断用户输入的指令类型
            sound_type = await self._identify_command_type(text)
            
            # 步骤2: 根据指令类型获取对应的猫叫声文件
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
                
        except Exception as e:
            logger.bind(tag=TAG).error(f"猫翻译TTS失败: {e}")
            raise Exception(f"{__name__}: 猫翻译TTS失败 - {str(e)}")

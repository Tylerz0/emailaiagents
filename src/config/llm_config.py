"""大模型配置模块

此模块包含大模型API的配置信息，使用环境变量保护敏感信息。
"""

import os
from dotenv import load_dotenv

# STEP1: 加载环境变量
load_dotenv()

# STEP2: 从环境变量中读取配置
LLM_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY'),
    'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
    'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
    'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '1000')),
    'system_prompt': os.getenv('OPENAI_SYSTEM_PROMPT', '''你是一个专业的客服代表，负责处理客户邮件。
请遵循以下原则：
1. 保持专业、友好和同理心
2. 回答要简洁明了
3. 如果信息不足，要礼貌地询问更多细节
4. 如果遇到投诉，要表达歉意并积极解决问题
5. 回复要自然流畅，避免机械化的模板语言''')
}

# WHY: 使用环境变量可以：
# 1. 保护API密钥等敏感信息
# 2. 方便在不同环境中调整模型参数
# 3. 便于进行A/B测试不同的系统提示词 
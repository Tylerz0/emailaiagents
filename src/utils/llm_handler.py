"""大模型处理模块

此模块提供邮件分类和回复生成的核心功能，包括：
- 邮件意图分类
- 上下文管理
- 自然语言回复生成
"""

from typing import List, Dict, Optional
from openai import OpenAI
import json
import logging
from datetime import datetime
from ..config.llm_config import LLM_CONFIG

# STEP1: 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMHandler:
    """大模型处理类，负责邮件分类和回复生成"""
    
    def __init__(self):
        """初始化大模型处理器"""
        self.config = LLM_CONFIG
        # STEP2: 正确初始化OpenAI客户端
        self.client = OpenAI(api_key=self.config['api_key'])
        
    def classify_intent(self, email_content: str) -> Dict:
        """分析邮件意图
        
        Args:
            email_content (str): 邮件内容
            
        Returns:
            Dict: 包含意图分类和关键信息的字典
        """
        try:
            # STEP3: 构建分类提示词
            classification_prompt = f"""请分析以下邮件内容，并给出：
1. 主要意图（如：咨询、投诉、建议等）
2. 情感倾向（积极、消极、中性）
3. 紧急程度（高、中、低）
4. 关键信息提取

邮件内容：
{email_content}

请以JSON格式回复。"""
            
            # STEP4: 调用API进行分类
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=[
                    {"role": "system", "content": "你是一个专业的邮件分析助手，负责分析邮件意图和关键信息。"},
                    {"role": "user", "content": classification_prompt}
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            # STEP5: 解析返回结果
            result = response.choices[0].message.content
            logger.info(f"邮件分类结果: {result}")
            try:
                return json.loads(result)
            except:
                return {
                    "intent": "unknown",
                    "sentiment": "neutral",
                    "urgency": "medium",
                    "key_info": []
                }
            
        except Exception as e:
            logger.error(f"邮件分类失败: {str(e)}")
            return {
                "intent": "unknown",
                "sentiment": "neutral",
                "urgency": "medium",
                "key_info": []
            }
            
    def generate_reply(self, 
                      email_content: str, 
                      intent_analysis: Dict,
                      history: Optional[List[Dict]] = None) -> str:
        """生成邮件回复
        
        Args:
            email_content (str): 原始邮件内容
            intent_analysis (Dict): 意图分析结果
            history (Optional[List[Dict]], optional): 历史对话记录
            
        Returns:
            str: 生成的回复内容
        """
        try:
            # STEP2: 构建上下文信息
            context = f"""邮件意图分析：
- 主要意图：{intent_analysis.get('intent', 'unknown')}
- 情感倾向：{intent_analysis.get('sentiment', 'neutral')}
- 紧急程度：{intent_analysis.get('urgency', 'medium')}
- 关键信息：{intent_analysis.get('key_info', [])}

原始邮件内容：
{email_content}"""

            # 如果有历史记录，添加到上下文
            if history:
                context += "\n\n历史对话记录："
                for msg in history[-3:]:  # 只使用最近3条记录
                    context += f"\n- {msg['date']}: {msg['body']}"

            # STEP3: 构建回复生成提示词
            reply_prompt = f"""基于以下信息生成一封专业的回复邮件：

{context}

请生成一封：
1. 符合邮件意图和情感倾向的回复
2. 针对关键信息给出具体回应
3. 保持专业、友好和同理心
4. 使用自然流畅的语言
5. 避免使用模板化的表达

请直接返回回复内容，不要包含任何其他信息。"""

            # STEP4: 调用API生成回复
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=[
                    {"role": "system", "content": self.config['system_prompt']},
                    {"role": "user", "content": reply_prompt}
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            # STEP5: 获取生成的回复
            reply = response.choices[0].message.content
            logger.info(f"成功生成回复，长度: {len(reply)}")
            return reply
            
        except Exception as e:
            logger.error(f"回复生成失败: {str(e)}")
            return "抱歉，我现在无法生成回复。请稍后再试。"
            
# WHY: 使用类封装大模型处理功能，便于管理状态和复用代码
# 添加了完整的错误处理和日志记录，提高系统稳定性 
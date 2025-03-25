"""
测试大模型处理功能
"""
from src.utils.llm_handler import LLMHandler
from openai import OpenAI
import os
from dotenv import load_dotenv

def test_openai_connection():
    """测试 OpenAI API 连接"""
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, this is a test message."}
            ]
        )
        print("API 连接测试成功！")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"API 连接测试失败: {str(e)}")
        return False

def test_llm_processing():
    """测试大模型处理功能"""
    # 首先测试 API 连接
    if not test_openai_connection():
        print("API 连接测试失败，跳过后续测试")
        return
        
    handler = LLMHandler()
    
    # 测试邮件分类
    print("\n测试邮件分类...")
    test_email = """
    尊敬的客服：
    
    我上周在贵店购买的商品至今未收到，订单号是123456。
    这已经严重影响了我的使用计划，请尽快处理。
    
    谢谢！
    """
    
    intent_analysis = handler.classify_intent(test_email)
    print(f"分类结果：{intent_analysis}")
    
    # 测试回复生成
    print("\n测试回复生成...")
    reply = handler.generate_reply(test_email, intent_analysis)
    print(f"生成的回复：\n{reply}")

if __name__ == "__main__":
    test_llm_processing() 
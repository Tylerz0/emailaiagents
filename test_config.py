"""
测试邮件配置是否正确
"""
from src.utils.email_handler import EmailHandler

def test_email_config():
    """测试邮件配置"""
    handler = EmailHandler()
    
    # 测试IMAP连接
    print("测试IMAP连接...")
    imap_success = handler.connect_imap()
    print(f"IMAP连接{'成功' if imap_success else '失败'}")
    
    # 测试发送邮件
    print("\n测试发送邮件...")
    send_success = handler.send_email(
        to_email="support@revalued.store",  # 发送给自己测试
        subject="测试邮件",
        body="这是一封测试邮件，用于验证邮件配置是否正确。"
    )
    print(f"邮件发送{'成功' if send_success else '失败'}")
    
    # 关闭连接
    handler.close_connections()

if __name__ == "__main__":
    test_email_config() 
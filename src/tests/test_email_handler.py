"""邮件处理器测试模块

此模块包含对EmailHandler类的单元测试
"""

import unittest
from ..utils.email_handler import EmailHandler

class TestEmailHandler(unittest.TestCase):
    """EmailHandler类的测试用例"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.email_handler = EmailHandler()
        
    def test_connect_imap(self):
        """测试IMAP连接"""
        result = self.email_handler.connect_imap()
        self.assertIsInstance(result, bool)
        
    def test_get_unread_emails(self):
        """测试获取未读邮件"""
        emails = self.email_handler.get_unread_emails()
        self.assertIsInstance(emails, list)
        
    def test_send_email(self):
        """测试发送邮件"""
        result = self.email_handler.send_email(
            to_email="test@example.com",
            subject="测试邮件",
            body="这是一封测试邮件"
        )
        self.assertIsInstance(result, bool)
        
    def tearDown(self):
        """测试后的清理工作"""
        self.email_handler.close_connections()

if __name__ == '__main__':
    unittest.main() 
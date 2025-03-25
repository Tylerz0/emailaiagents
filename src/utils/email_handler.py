"""邮件处理模块

此模块提供邮件接收和发送的核心功能，包括：
- 接收未读邮件
- 解析邮件内容
- 发送回复邮件
"""

from typing import List, Dict, Optional
import yagmail
from imbox import Imbox
from datetime import datetime
import logging
from ..config.email_config import EMAIL_CONFIG

# STEP1: 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailHandler:
    """邮件处理类，负责邮件的接收和发送"""
    
    def __init__(self):
        """初始化邮件处理器"""
        self.config = EMAIL_CONFIG
        self.imap_client = None
        self.smtp_client = None
        
    def connect_imap(self) -> bool:
        """连接IMAP服务器
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.imap_client = Imbox(
                hostname=self.config['imap_server'],
                username=self.config['email'],
                password=self.config['password'],
                port=self.config['imap_port'],
                ssl=self.config['use_ssl']
            )
            logger.info("IMAP服务器连接成功")
            return True
        except Exception as e:
            logger.error(f"IMAP连接失败: {str(e)}")
            return False
            
    def get_unread_emails(self) -> List[Dict]:
        """获取未读邮件列表
        
        Returns:
            List[Dict]: 未读邮件列表，每个邮件包含发件人、主题、正文等信息
        """
        if not self.imap_client:
            if not self.connect_imap():
                return []
                
        try:
            unread_messages = self.imap_client.messages(unread=True)
            emails = []
            
            for uid, message in unread_messages:
                email_data = {
                    'uid': uid,
                    'from': message.sent_from[0]['email'],
                    'subject': message.subject,
                    'body': message.body['plain'][0] if message.body['plain'] else '',
                    'date': message.date,
                    'attachments': message.attachments
                }
                emails.append(email_data)
                
            logger.info(f"成功获取 {len(emails)} 封未读邮件")
            return emails
            
        except Exception as e:
            logger.error(f"获取未读邮件失败: {str(e)}")
            return []
            
    def send_email(self, to_email: str, subject: str, body: str, 
                   attachments: Optional[List[str]] = None) -> bool:
        """发送邮件
        
        Args:
            to_email (str): 收件人邮箱
            subject (str): 邮件主题
            body (str): 邮件正文
            attachments (Optional[List[str]], optional): 附件路径列表
            
        Returns:
            bool: 发送是否成功
        """
        try:
            if not self.smtp_client:
                self.smtp_client = yagmail.SMTP(
                    user=self.config['email'],
                    password=self.config['password'],
                    host=self.config['smtp_server'],
                    port=self.config['smtp_port'],
                    smtp_ssl=self.config['use_ssl']
                )
                
            self.smtp_client.send(
                to=to_email,
                subject=subject,
                contents=body,
                attachments=attachments
            )
            
            logger.info(f"邮件发送成功: {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False
            
    def close_connections(self):
        """关闭所有连接"""
        if self.imap_client:
            self.imap_client.logout()
        if self.smtp_client:
            self.smtp_client.close()
            
# WHY: 使用类封装邮件处理功能，便于管理状态和复用代码
# 添加了完整的错误处理和日志记录，提高系统稳定性 
"""邮件服务器配置模块

此模块包含邮件服务器的配置信息，包括SMTP和IMAP服务器的设置。
使用环境变量来保护敏感信息。
"""

import os
from dotenv import load_dotenv

# STEP1: 加载环境变量
load_dotenv()

# STEP2: 从环境变量中读取配置
EMAIL_CONFIG = {
    'imap_server': os.getenv('IMAP_SERVER'),
    'imap_port': int(os.getenv('IMAP_PORT', 993)),
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT', 465)),
    'email': os.getenv('EMAIL_USERNAME'),
    'password': os.getenv('EMAIL_PASSWORD'),
    'use_ssl': os.getenv('EMAIL_USE_SSL', 'True').lower() == 'true'
}

# WHY: 使用环境变量可以：
# 1. 保护敏感信息不被意外提交到代码仓库
# 2. 方便在不同环境中切换配置
# 3. 符合12要素应用的配置管理原则

# WHY: 使用字典存储配置便于管理和修改
# 注意：实际使用时请替换为真实的服务器信息 
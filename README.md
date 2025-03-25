# AI 邮件自动回复系统

## 项目简介
基于大模型的轻量化邮件自动回复系统，支持客户需求分类、上下文管理、工具调用及可视化界面。

## 功能特点
- 自动接收和处理邮件
- 智能分类客户需求
- 自动生成个性化回复
- 支持上下文管理
- 可视化配置界面

## 安装说明
1. 克隆仓库
```bash
git clone YOUR_REPOSITORY_URL
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
- 复制 .env.example 为 .env
- 填写您的配置信息

## 使用说明
1. 启动服务
```bash
python main.py
```

2. 访问管理界面
打开浏览器访问 http://localhost:8501

## 开发文档
详细文档请参考 [docs/](docs/) 目录

## 技术栈
- Python 3.8+
- OpenAI GPT-4
- SMTP/IMAP 邮件协议
- Streamlit 可视化界面

## 注意事项
- 请确保正确配置 .env 文件中的敏感信息
- 建议在测试环境中先进行充分测试
- 定期备份客户数据 
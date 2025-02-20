from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建基类
Base = declarative_base()

# 创建数据库连接（SQLite 数据库存储聊天记录）
engine = create_engine('sqlite:///chat_history.db', echo=False)  # echo=True 可开启 SQL 调试日志

# 创建会话工厂
Session = sessionmaker(bind=engine)


class ChatMessage(Base):
    """定义聊天消息表"""
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)  # 自增主键
    sender_id = Column(String(100), nullable=False)  # 发送者微信 ID
    sender_name = Column(String(100), nullable=False)  # 发送者昵称
    message = Column(Text, nullable=False)  # 用户发送的消息内容
    reply = Column(Text, nullable=False)  # 机器人回复的消息内容
    created_at = Column(DateTime, default=datetime.utcnow)  # 消息创建时间（使用 UTC 时间）


# 创建数据库表（如果不存在则创建）
Base.metadata.create_all(engine)

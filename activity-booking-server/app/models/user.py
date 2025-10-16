from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True, nullable=False, comment="微信openid")
    unionid = Column(String(100), index=True, comment="微信unionid")
    nickname = Column(String(100), comment="昵称")
    avatar = Column(String(500), comment="头像")
    phone = Column(String(20), comment="手机号")
    gender = Column(Integer, default=0, comment="性别 0-未知 1-男 2-女")
    country = Column(String(50), comment="国家")
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    language = Column(String(20), comment="语言")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    bookings = relationship("Booking", back_populates="user")


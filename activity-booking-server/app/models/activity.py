from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Activity(Base):
    """活动模型"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="活动标题")
    description = Column(Text, comment="活动描述")
    cover_image = Column(String(500), comment="封面图片")
    location = Column(String(200), comment="活动地点")
    organizer = Column(String(100), comment="主办方")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    price = Column(Float, default=0, comment="价格")
    max_participants = Column(Integer, default=100, comment="最大参与人数")
    booked_count = Column(Integer, default=0, comment="已预约人数")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    bookings = relationship("Booking", back_populates="activity")


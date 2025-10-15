from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base


class BookingStatus(str, Enum):
    """预约状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    """预约模型"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, comment="活动ID")
    name = Column(String(100), nullable=False, comment="预约人姓名")
    phone = Column(String(20), nullable=False, comment="联系电话")
    participants = Column(Integer, default=1, comment="参与人数")
    remark = Column(String(500), comment="备注")
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.CONFIRMED, comment="状态")
    checked_in = Column(Integer, default=0, comment="是否签到")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="bookings")
    activity = relationship("Activity", back_populates="bookings")


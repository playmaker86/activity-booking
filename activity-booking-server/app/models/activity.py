from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class Activity(Base):
    """活动模型"""
    __tablename__ = "activities"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="活动标题")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="活动描述")
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), comment="封面图片")
    location: Mapped[Optional[str]] = mapped_column(String(200), comment="活动地点")
    organizer: Mapped[Optional[str]] = mapped_column(String(100), comment="主办方")
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="开始时间")
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="结束时间")
    price: Mapped[float] = mapped_column(Float, default=0, comment="价格")
    max_participants: Mapped[int] = mapped_column(Integer, default=100, comment="最大参与人数")
    booked_count: Mapped[int] = mapped_column(Integer, default=0, comment="已预约人数")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="activity")


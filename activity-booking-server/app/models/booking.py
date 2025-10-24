from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum
from app.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.activity import Activity


class BookingStatus(str, Enum):
    """预约状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    """预约模型"""
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    activity_id: Mapped[int] = mapped_column(Integer, ForeignKey("activities.id"), nullable=False, comment="活动ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="预约人姓名")
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="联系电话")
    participants: Mapped[int] = mapped_column(Integer, default=1, comment="参与人数")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    status: Mapped[BookingStatus] = mapped_column(SQLEnum(BookingStatus), default=BookingStatus.CONFIRMED, comment="状态")
    checked_in: Mapped[int] = mapped_column(Integer, default=0, comment="是否签到")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    activity: Mapped["Activity"] = relationship("Activity", back_populates="bookings")


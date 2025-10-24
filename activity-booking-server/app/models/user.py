from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    openid: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="微信openid")
    unionid: Mapped[Optional[str]] = mapped_column(String(100), index=True, comment="微信unionid")
    nickname: Mapped[Optional[str]] = mapped_column(String(100), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(500), comment="头像")
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment="手机号")
    gender: Mapped[int] = mapped_column(Integer, default=0, comment="性别 0-未知 1-男 2-女")
    country: Mapped[Optional[str]] = mapped_column(String(50), comment="国家")
    province: Mapped[Optional[str]] = mapped_column(String(50), comment="省份")
    city: Mapped[Optional[str]] = mapped_column(String(50), comment="城市")
    language: Mapped[Optional[str]] = mapped_column(String(20), comment="语言")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="user")


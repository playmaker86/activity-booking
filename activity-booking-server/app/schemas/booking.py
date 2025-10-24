from datetime import datetime
from typing import Optional, List

from app.models.booking import BookingStatus
from app.schemas.activity import Activity
from app.schemas.base import CamelCaseModel


class BookingBase(CamelCaseModel):
    """预约基础模型"""
    activity_id: int
    name: str
    phone: str
    participants: int = 1
    remark: Optional[str] = None


class BookingCreate(BookingBase):
    """创建预约模型"""
    pass


class BookingUpdate(CamelCaseModel):
    """更新预约模型"""
    name: Optional[str] = None
    phone: Optional[str] = None
    participants: Optional[int] = None
    remark: Optional[str] = None
    status: Optional[BookingStatus] = None


class Booking(BookingBase):
    """预约模型"""
    id: int
    user_id: int
    status: BookingStatus
    checked_in: int
    created_at: datetime
    updated_at: datetime
    activity: Optional[Activity] = None


class BookingList(CamelCaseModel):
    """预约列表模型"""
    items: List[Booking]
    total: int


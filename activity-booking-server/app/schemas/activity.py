from datetime import datetime
from typing import Optional, List
from app.schemas.base import CamelCaseModel


class ActivityBase(CamelCaseModel):
    """活动基础模型"""
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    start_time: datetime
    end_time: datetime
    price: float = 0
    max_participants: int = 100


class ActivityCreate(ActivityBase):
    """创建活动模型"""
    pass


class ActivityUpdate(CamelCaseModel):
    """更新活动模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None


class Activity(ActivityBase):
    """活动模型"""
    id: int
    booked_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ActivityList(CamelCaseModel):
    """活动列表模型"""
    items: List[Activity]
    total: int
    page: int
    page_size: int


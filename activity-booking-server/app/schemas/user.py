from datetime import datetime
from typing import Optional
from app.schemas.base import CamelCaseModel


class UserBase(CamelCaseModel):
    """用户基础模型"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """创建用户模型"""
    openid: str


class UserUpdate(UserBase):
    """更新用户模型"""
    pass


class User(UserBase):
    """用户模型"""
    id: int
    openid: str
    created_at: datetime
    updated_at: datetime


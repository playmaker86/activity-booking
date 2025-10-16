from datetime import datetime
from typing import Optional
from app.schemas.base import CamelCaseModel


class UserBase(CamelCaseModel):
    """用户基础模型"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[int] = 0
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None


class UserCreate(UserBase):
    """创建用户模型"""
    openid: str
    unionid: Optional[str] = None


class UserUpdate(UserBase):
    """更新用户模型"""
    pass


class User(UserBase):
    """用户模型"""
    id: int
    openid: str
    unionid: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class WechatUserInfo(CamelCaseModel):
    """微信用户信息"""
    openid: str
    unionid: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[int] = 0
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None


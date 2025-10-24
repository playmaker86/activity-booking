from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问层"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_openid(self, openid: str) -> Optional[User]:
        """根据微信 openid 获取用户"""
        query = select(User).where(User.openid == openid)
        return self.db.scalar(query)
    
    def get_by_wechat_unionid(self, unionid: str) -> Optional[User]:
        """根据微信 unionid 获取用户"""
        query = select(User).where(User.wechat_unionid == unionid)
        return self.db.scalar(query)
    
    def create_user_from_wechat(self, openid: str, user_data: dict) -> User:
        """从微信信息创建用户"""
        user_data['openid'] = openid
        return self.create(user_data)
    
    def update_user_info(self, user_id: int, user_data: dict) -> Optional[User]:
        """更新用户信息"""
        user = self.get_by_id(user_id)
        if user:
            return self.update(user, user_data)
        return None

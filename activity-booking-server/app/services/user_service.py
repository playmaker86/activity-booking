from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    """用户业务逻辑层"""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_openid(self, openid: str) -> Optional[User]:
        """根据微信 openid 获取用户"""
        return self.user_repo.get_by_openid(openid)
    
    def create_user_from_wechat(self, openid: str, user_data: dict) -> User:
        """从微信信息创建用户"""
        return self.user_repo.create_user_from_wechat(openid, user_data)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        update_data = user_update.model_dump(exclude_unset=True)
        return self.user_repo.update_user_info(user_id, update_data)

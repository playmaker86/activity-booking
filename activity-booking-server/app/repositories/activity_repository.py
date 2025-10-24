from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.repositories.base import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    """活动数据访问层"""

    def __init__(self, db: Session):
        super().__init__(Activity, db)

    def get_active_activities(self, skip: int = 0, limit: int = 100) -> List[Activity]:
        """获取启用的活动列表"""
        query = select(Activity).where(Activity.is_active).offset(skip).limit(limit)
        result = self.db.scalars(query).all()
        return list(result)

    def count_active_activities(self) -> int:
        """获取启用的活动总数"""
        query = select(Activity).where(Activity.is_active)
        return self.db.scalar(select(func.count()).select_from(query.subquery()))
    
    def search_by_title(self, keyword: str) -> List[Activity]:
        """根据标题搜索活动"""
        query = select(Activity).where(
            Activity.is_active,
            Activity.title.contains(keyword)
        )
        result = self.db.scalars(query).all()
        return list(result)
    
    def get_hot_activities(self, limit: int = 10) -> List[Activity]:
        """获取热门活动（按预约人数排序）"""
        query = select(Activity).where(
            Activity.is_active
        ).order_by(Activity.booked_count.desc()).limit(limit)
        result = self.db.scalars(query).all()
        return list(result)

    def increment_booked_count(self, activity_id: int, count: int = 1) -> bool:
        """增加活动预约人数"""
        activity = self.get_by_id(activity_id)
        if activity:
            activity.booked_count += count
            self.db.commit()
            return True
        return False

    def decrement_booked_count(self, activity_id: int, count: int = 1) -> bool:
        """减少活动预约人数"""
        activity = self.get_by_id(activity_id)
        if activity:
            activity.booked_count -= count
            self.db.commit()
            return True
        return False

    def get_activity_with_bookings(self, activity_id: int) -> Optional[Activity]:
        """获取活动及其预约信息"""
        query = select(Activity).where(Activity.id == activity_id)
        return self.db.scalar(query)

    def soft_delete(self, activity_id: int) -> bool:
        """软删除活动（设置为不启用）"""
        activity = self.get_by_id(activity_id)
        if activity:
            activity.is_active = False
            self.db.commit()
            return True
        return False

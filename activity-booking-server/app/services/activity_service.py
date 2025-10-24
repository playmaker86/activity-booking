from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityList
from app.repositories.activity_repository import ActivityRepository

class ActivityService:
    """活动业务逻辑层"""
    
    def __init__(self, db: Session):
        self.activity_repo = ActivityRepository(db)
    
    def get_activities(self, page: int = 1, page_size: int = 10, keyword: Optional[str] = None) -> ActivityList:
        """获取活动列表"""
        skip = (page - 1) * page_size
        
        if keyword:
            activities = self.activity_repo.search_by_title(keyword)
            total = len(activities)
        else:
            activities = self.activity_repo.get_active_activities(skip, page_size)
            total = self.activity_repo.count_active_activities()
        
        return ActivityList(
            items=activities,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def get_activity_by_id(self, activity_id: int) -> Optional[Activity]:
        """根据 ID 获取活动详情"""
        return self.activity_repo.get_by_id(activity_id)
    
    def create_activity(self, activity_create: ActivityCreate) -> Activity:
        """创建活动"""
        return self.activity_repo.create(activity_create.model_dump())
    
    def update_activity(self, activity_id: int, activity_update: ActivityUpdate) -> Optional[Activity]:
        """更新活动"""
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            return None
        
        update_data = activity_update.model_dump(exclude_unset=True)
        return self.activity_repo.update(activity, update_data)
    
    def delete_activity(self, activity_id: int) -> bool:
        """删除活动（软删除）"""
        return self.activity_repo.soft_delete(activity_id)
    
    def get_hot_activities(self, limit: int = 10) -> List[Activity]:
        """获取热门活动"""
        return self.activity_repo.get_hot_activities(limit)
    
    def search_activities(self, keyword: str) -> ActivityList:
        """搜索活动"""
        activities = self.activity_repo.search_by_title(keyword)
        return ActivityList(
            items=activities,
            total=len(activities),
            page=1,
            page_size=len(activities)
        )
    
    def increment_booking_count(self, activity_id: int, count: int = 1) -> bool:
        """增加活动预约人数"""
        return self.activity_repo.increment_booked_count(activity_id, count)
    
    def decrement_booking_count(self, activity_id: int, count: int = 1) -> bool:
        """减少活动预约人数"""
        return self.activity_repo.decrement_booked_count(activity_id, count)

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingList
from app.repositories.booking_repository import BookingRepository
from app.repositories.activity_repository import ActivityRepository

class BookingService:
    """预约业务逻辑层"""
    
    def __init__(self, db: Session):
        self.booking_repo = BookingRepository(db)
        self.activity_repo = ActivityRepository(db)
    
    def create_booking(self, booking_create: BookingCreate, user_id: int) -> Optional[Booking]:
        """创建预约"""
        # 检查活动是否存在
        activity = self.activity_repo.get_by_id(booking_create.activity_id)
        if not activity:
            return None
        
        # 检查是否已满员
        if activity.booked_count >= activity.max_participants:
            return None
        
        # 创建预约
        booking_data = booking_create.model_dump()
        booking_data['user_id'] = user_id
        booking = self.booking_repo.create(booking_data)
        
        # 更新活动已预约人数
        self.activity_repo.increment_booked_count(activity.id, booking_create.participants)
        
        return booking
    
    def get_user_bookings(self, user_id: int) -> BookingList:
        """获取用户的预约列表"""
        bookings = self.booking_repo.get_user_bookings(user_id)
        return BookingList(items=bookings, total=len(bookings))
    
    def get_user_booking(self, booking_id: int, user_id: int) -> Optional[Booking]:
        """获取用户特定的预约"""
        return self.booking_repo.get_user_booking(booking_id, user_id)
    
    def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        """取消预约"""
        booking = self.booking_repo.get_user_booking(booking_id, user_id)
        if not booking:
            return False
        
        if booking.status != BookingStatus.CONFIRMED:
            return False
        
        # 更新预约状态
        success = self.booking_repo.cancel_booking(booking_id)
        if success:
            # 更新活动已预约人数
            self.activity_repo.decrement_booked_count(booking.activity_id, booking.participants)
        
        return success
    
    def checkin_booking(self, booking_id: int, user_id: int) -> bool:
        """签到预约"""
        booking = self.booking_repo.get_user_booking(booking_id, user_id)
        if not booking:
            return False
        
        if booking.status != BookingStatus.CONFIRMED:
            return False
        
        if booking.checked_in:
            return False
        
        # 更新签到状态
        return self.booking_repo.checkin_booking(booking_id)

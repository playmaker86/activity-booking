from sqlalchemy import select, func
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus
from app.repositories.base import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    """预约数据访问层"""
    
    def __init__(self, db: Session):
        super().__init__(Booking, db)
    
    def get_user_bookings(self, user_id: int) -> List[Booking]:
        """获取用户的预约列表"""
        query = select(Booking).where(
            Booking.user_id == user_id
        ).order_by(Booking.created_at.desc())
        result = self.db.scalars(query).all()
        return list(result)
    
    def get_user_booking(self, booking_id: int, user_id: int) -> Optional[Booking]:
        """获取用户特定的预约"""
        query = select(Booking).where(
            Booking.id == booking_id,
            Booking.user_id == user_id
        )
        return self.db.scalar(query)
    
    def get_activity_bookings(self, activity_id: int) -> List[Booking]:
        """获取活动的所有预约"""
        query = select(Booking).where(Booking.activity_id == activity_id)
        result = self.db.scalars(query).all()
        return list(result)
    
    def count_activity_bookings(self, activity_id: int) -> int:
        """统计活动的预约数量"""
        query = select(Booking).where(
            Booking.activity_id == activity_id,
            Booking.status == BookingStatus.CONFIRMED
        )
        return self.db.scalar(select(func.count()).select_from(query.subquery()))
    
    def update_booking_status(self, booking_id: int, status: BookingStatus) -> bool:
        """更新预约状态"""
        booking = self.get_by_id(booking_id)
        if booking:
            booking.status = status
            self.db.commit()
            return True
        return False
    
    def checkin_booking(self, booking_id: int) -> bool:
        """签到预约"""
        booking = self.get_by_id(booking_id)
        if booking:
            booking.checked_in = 1
            booking.status = BookingStatus.COMPLETED
            self.db.commit()
            return True
        return False
    
    def cancel_booking(self, booking_id: int) -> bool:
        """取消预约"""
        booking = self.get_by_id(booking_id)
        if booking:
            booking.status = BookingStatus.CANCELLED
            self.db.commit()
            return True
        return False
    
    def get_confirmed_bookings_by_activity(self, activity_id: int) -> List[Booking]:
        """获取活动已确认的预约"""
        query = select(Booking).where(
            Booking.activity_id == activity_id,
            Booking.status == BookingStatus.CONFIRMED
        )
        result = self.db.scalars(query).all()
        return list(result)

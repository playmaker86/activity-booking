from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.models.activity import Activity
from app.schemas.booking import (
    Booking as BookingSchema,
    BookingCreate,
    BookingUpdate,
    BookingList
)

router = APIRouter()


@router.post("", response_model=BookingSchema)
async def create_booking(
    booking_create: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建预约"""
    # 检查活动是否存在
    activity = db.query(Activity).filter(Activity.id == booking_create.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    # 检查是否已满员
    if activity.booked_count >= activity.max_participants:
        raise HTTPException(status_code=400, detail="活动已满员")
    
    # 创建预约
    booking = Booking(
        **booking_create.model_dump(),
        user_id=current_user.id
    )
    db.add(booking)
    
    # 更新活动已预约人数
    activity.booked_count += booking_create.participants
    
    db.commit()
    db.refresh(booking)
    
    return booking


@router.get("/my", response_model=BookingList)
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我的预约列表"""
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.created_at.desc()).all()
    
    return BookingList(items=bookings, total=len(bookings))


@router.get("/{booking_id}", response_model=BookingSchema)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取预约详情"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    return booking


@router.put("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消预约"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(status_code=400, detail="该预约无法取消")
    
    # 更新预约状态
    booking.status = BookingStatus.CANCELLED
    
    # 更新活动已预约人数
    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    if activity:
        activity.booked_count -= booking.participants
    
    db.commit()
    
    return {"message": "取消成功"}


@router.put("/{booking_id}/checkin")
async def checkin_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """签到"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(status_code=400, detail="该预约无法签到")
    
    if booking.checked_in:
        raise HTTPException(status_code=400, detail="已签到")
    
    # 更新签到状态
    booking.checked_in = 1
    booking.status = BookingStatus.COMPLETED
    
    db.commit()
    
    return {"message": "签到成功"}


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.booking import (
    Booking as BookingSchema,
    BookingCreate,
    BookingList
)
from app.schemas.response import ApiResponse, ResponseCode
from app.services.booking_service import BookingService
from app.utils.response import create_success_response, create_error_response

router = APIRouter()


@router.post("", response_model=ApiResponse[BookingSchema])
async def create_booking(
    booking_create: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建预约"""
    try:
        booking_service = BookingService(db)
        booking = booking_service.create_booking(booking_create, current_user.id)
        
        if not booking:
            return create_error_response(
                code=ResponseCode.BAD_REQUEST,
                message="活动不存在或已满员",
                error="Activity not found or fully booked"
            )
        
        return create_success_response(
            data=booking,
            message="创建预约成功",
            code=ResponseCode.CREATED
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="创建预约失败",
            error=str(e)
        )


@router.get("/my", response_model=ApiResponse[BookingList])
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我的预约列表"""
    try:
        booking_service = BookingService(db)
        bookings = booking_service.get_user_bookings(current_user.id)
        return create_success_response(
            data=bookings,
            message="获取预约列表成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取预约列表失败",
            error=str(e)
        )


@router.get("/{booking_id}", response_model=ApiResponse[BookingSchema])
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取预约详情"""
    try:
        booking_service = BookingService(db)
        booking = booking_service.get_user_booking(booking_id, current_user.id)
        
        if not booking:
            return create_error_response(
                code=ResponseCode.NOT_FOUND,
                message="预约不存在",
                error=f"Booking with id {booking_id} not found"
            )
        
        return create_success_response(
            data=booking,
            message="获取预约详情成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取预约详情失败",
            error=str(e)
        )


@router.put("/{booking_id}/cancel", response_model=ApiResponse[None])
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消预约"""
    try:
        booking_service = BookingService(db)
        success = booking_service.cancel_booking(booking_id, current_user.id)
        
        if not success:
            return create_error_response(
                code=ResponseCode.BAD_REQUEST,
                message="预约不存在或无法取消",
                error="Booking not found or cannot be cancelled"
            )
        
        return create_success_response(
            data=None,
            message="取消预约成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="取消预约失败",
            error=str(e)
        )


@router.put("/{booking_id}/checkin", response_model=ApiResponse[None])
async def checkin_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """签到"""
    try:
        booking_service = BookingService(db)
        success = booking_service.checkin_booking(booking_id, current_user.id)
        
        if not success:
            return create_error_response(
                code=ResponseCode.BAD_REQUEST,
                message="预约不存在或无法签到",
                error="Booking not found or cannot be checked in"
            )
        
        return create_success_response(
            data=None,
            message="签到成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="签到失败",
            error=str(e)
        )


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.schemas.response import ApiResponse, ResponseCode
from app.services.user_service import UserService
from app.utils.response import create_success_response, create_error_response

router = APIRouter()


@router.get("/me", response_model=ApiResponse[UserSchema])
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        return create_success_response(
            data=current_user,
            message="获取用户信息成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取用户信息失败",
            error=str(e)
        )


@router.put("/me", response_model=ApiResponse[UserSchema])
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    try:
        user_service = UserService(db)
        updated_user = user_service.update_user(current_user.id, user_update)
        if not updated_user:
            return create_error_response(
                code=ResponseCode.NOT_FOUND,
                message="用户不存在",
                error=f"User with id {current_user.id} not found"
            )
        return create_success_response(
            data=updated_user,
            message="更新用户信息成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="更新用户信息失败",
            error=str(e)
        )


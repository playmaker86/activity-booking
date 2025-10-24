from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_db
from app.models.activity import Activity
from app.schemas.activity import (
    Activity as ActivitySchema,
    ActivityCreate,
    ActivityUpdate,
    ActivityList
)
from app.services.activity_service import ActivityService
from app.schemas.response import ApiResponse, ResponseCode
from app.utils.response import create_success_response, create_error_response

router = APIRouter()


@router.get("", response_model=ApiResponse[ActivityList])
async def get_activities(
    page: int = Query(1, ge=1, alias="page"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    keyword: Optional[str] = Query(None, alias="keyword"),
    db: Session = Depends(get_db)
):
    """获取活动列表"""
    try:
        activity_service = ActivityService(db)
        activities = activity_service.get_activities(page, page_size, keyword)
        return create_success_response(
            data=activities,
            message="获取活动列表成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取活动列表失败",
            error=str(e)
        )


@router.get("/{activity_id}", response_model=ApiResponse[ActivitySchema])
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """获取活动详情"""
    try:
        activity_service = ActivityService(db)
        activity = activity_service.get_activity_by_id(activity_id)
        if not activity:
            return create_error_response(
                code=ResponseCode.NOT_FOUND,
                message="活动不存在",
                error=f"Activity with id {activity_id} not found"
            )
        return create_success_response(
            data=activity,
            message="获取活动详情成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取活动详情失败",
            error=str(e)
        )


@router.post("", response_model=ApiResponse[ActivitySchema])
async def create_activity(
    activity_create: ActivityCreate,
    db: Session = Depends(get_db)
):
    """创建活动"""
    try:
        activity_service = ActivityService(db)
        activity = activity_service.create_activity(activity_create)
        return create_success_response(
            data=activity,
            message="创建活动成功",
            code=ResponseCode.CREATED
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="创建活动失败",
            error=str(e)
        )


@router.put("/{activity_id}", response_model=ApiResponse[ActivitySchema])
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db)
):
    """更新活动"""
    try:
        activity_service = ActivityService(db)
        activity = activity_service.update_activity(activity_id, activity_update)
        if not activity:
            return create_error_response(
                code=ResponseCode.NOT_FOUND,
                message="活动不存在",
                error=f"Activity with id {activity_id} not found"
            )
        return create_success_response(
            data=activity,
            message="更新活动成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="更新活动失败",
            error=str(e)
        )


@router.delete("/{activity_id}", response_model=ApiResponse[None])
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """删除活动（软删除）"""
    try:
        activity_service = ActivityService(db)
        success = activity_service.delete_activity(activity_id)
        if not success:
            return create_error_response(
                code=ResponseCode.NOT_FOUND,
                message="活动不存在",
                error=f"Activity with id {activity_id} not found"
            )
        return create_success_response(
            data=None,
            message="删除活动成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="删除活动失败",
            error=str(e)
        )


@router.get("/search", response_model=ApiResponse[ActivityList])
async def search_activities(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """搜索活动"""
    try:
        activity_service = ActivityService(db)
        activities = activity_service.search_activities(keyword)
        return create_success_response(
            data=activities,
            message="搜索活动成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="搜索活动失败",
            error=str(e)
        )


@router.get("/hot", response_model=ApiResponse[ActivityList])
async def get_hot_activities(db: Session = Depends(get_db)):
    """获取热门活动"""
    try:
        activity_service = ActivityService(db)
        activities = activity_service.get_hot_activities(10)
        activity_list = ActivityList(
            items=activities,
            total=len(activities),
            page=1,
            page_size=len(activities)
        )
        return create_success_response(
            data=activity_list,
            message="获取热门活动成功"
        )
    except Exception as e:
        return create_error_response(
            code=ResponseCode.INTERNAL_ERROR,
            message="获取热门活动失败",
            error=str(e)
        )


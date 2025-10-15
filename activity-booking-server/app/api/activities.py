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

router = APIRouter()


@router.get("", response_model=ActivityList)
async def get_activities(
    page: int = Query(1, ge=1, alias="page"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    keyword: Optional[str] = Query(None, alias="keyword"),
    db: Session = Depends(get_db)
):
    """获取活动列表"""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # 搜索
    if keyword:
        query = query.filter(Activity.title.contains(keyword))
    
    # 总数
    total = query.count()
    
    # 分页
    activities = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ActivityList(
        items=activities,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{activity_id}", response_model=ActivitySchema)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """获取活动详情"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    return activity


@router.post("", response_model=ActivitySchema)
async def create_activity(
    activity_create: ActivityCreate,
    db: Session = Depends(get_db)
):
    """创建活动"""
    activity = Activity(**activity_create.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db)
):
    """更新活动"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    for field, value in activity_update.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """删除活动（软删除）"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    activity.is_active = False
    db.commit()
    
    return {"message": "删除成功"}


@router.get("/search", response_model=ActivityList)
async def search_activities(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """搜索活动"""
    activities = db.query(Activity).filter(
        Activity.is_active == True,
        Activity.title.contains(keyword)
    ).all()
    
    return ActivityList(
        items=activities,
        total=len(activities),
        page=1,
        page_size=len(activities)
    )


@router.get("/hot", response_model=ActivityList)
async def get_hot_activities(db: Session = Depends(get_db)):
    """获取热门活动"""
    activities = db.query(Activity).filter(
        Activity.is_active == True
    ).order_by(Activity.booked_count.desc()).limit(10).all()
    
    return ActivityList(
        items=activities,
        total=len(activities),
        page=1,
        page_size=len(activities)
    )


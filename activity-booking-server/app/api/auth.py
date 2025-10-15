from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.schemas.token import Token
from app.utils.security import create_access_token
from app.utils.wechat import get_wechat_openid
from pydantic import BaseModel

router = APIRouter()


class WxLoginRequest(BaseModel):
    """微信登录请求"""
    code: str


@router.post("/wx-login", response_model=Token)
async def wx_login(request: WxLoginRequest, db: Session = Depends(get_db)):
    """微信小程序登录"""
    # 获取openid
    openid = await get_wechat_openid(request.code)
    if not openid:
        raise HTTPException(status_code=400, detail="登录失败，请重试")
    
    # 查找或创建用户
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        user = User(openid=openid)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 创建token
    access_token = create_access_token({"user_id": user.id})
    
    return Token(token=access_token)


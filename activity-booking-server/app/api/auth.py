import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import User
from app.schemas.token import Token
from app.utils.security import create_access_token
from app.utils.wechat import (
    get_wechat_openid,
    get_wechat_access_token,
    get_wechat_user_info,
    get_wechat_web_login_url
)

router = APIRouter()


class WxLoginRequest(BaseModel):
    """微信小程序登录请求"""
    code: str


class WxWebLoginRequest(BaseModel):
    """微信网页登录请求"""
    code: str
    state: Optional[str] = None


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


@router.post("/wx-web-login", response_model=Token)
async def wx_web_login(request: WxWebLoginRequest, db: Session = Depends(get_db)):
    """微信网页授权登录"""
    # 获取access_token
    token_data = await get_wechat_access_token(request.code)
    if not token_data:
        raise HTTPException(status_code=400, detail="授权失败，请重试")
    
    access_token = token_data.get("access_token")
    openid = token_data.get("openid")
    unionid = token_data.get("unionid")
    
    if not access_token or not openid:
        raise HTTPException(status_code=400, detail="获取用户信息失败")
    
    # 获取微信用户详细信息
    user_info = await get_wechat_user_info(access_token, openid)
    
    # 查找或创建用户
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        # 创建新用户
        user = User(
            openid=openid,
            unionid=unionid,
            nickname=user_info.get("nickname") if user_info else None,
            avatar=user_info.get("headimgurl") if user_info else None,
            gender=user_info.get("sex", 0) if user_info else 0,
            country=user_info.get("country") if user_info else None,
            province=user_info.get("province") if user_info else None,
            city=user_info.get("city") if user_info else None,
            language=user_info.get("language") if user_info else None
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # 更新用户信息
        if user_info:
            user.nickname = user_info.get("nickname") or user.nickname
            user.avatar = user_info.get("headimgurl") or user.avatar
            user.gender = user_info.get("sex", user.gender)
            user.country = user_info.get("country") or user.country
            user.province = user_info.get("province") or user.province
            user.city = user_info.get("city") or user.city
            user.language = user_info.get("language") or user.language
            if unionid and not user.unionid:
                user.unionid = unionid
            db.commit()
    
    # 创建token
    access_token = create_access_token({"user_id": user.id})
    
    return Token(token=access_token)


@router.get("/wx-web-login-url")
async def get_wx_web_login_url(redirect_uri: str, request: Request):
    """获取微信网页授权登录URL"""
    # 生成state参数用于防止CSRF攻击
    state = secrets.token_urlsafe(32)
    
    # 生成微信授权URL
    auth_url = get_wechat_web_login_url(redirect_uri, state)
    
    return {
        "auth_url": auth_url,
        "state": state
    }


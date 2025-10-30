from typing import Optional, Dict, Any

import httpx

from app.core.config import settings


async def get_wechat_openid(code: str) -> Optional[str]:
    """获取微信小程序openid"""
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        if "openid" in data:
            return data["openid"]
        else:
            return None


async def get_wechat_access_token(code: str) -> Optional[Dict[str, Any]]:
    """获取微信网页授权access_token"""
    url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {
        "appid": settings.WECHAT_WEB_APPID,
        "secret": settings.WECHAT_WEB_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        if "access_token" in data:
            return data
        else:
            return None


async def get_wechat_user_info(access_token: str, openid: str) -> Optional[Dict[str, Any]]:
    """获取微信用户信息"""
    url = "https://api.weixin.qq.com/sns/userinfo"
    params = {
        "access_token": access_token,
        "openid": openid,
        "lang": "zh_CN"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        if "openid" in data:
            return data
        else:
            return None


def get_wechat_web_login_url(redirect_uri: str, state: str = "") -> str:
    """生成微信网页授权登录URL"""
    url = "https://open.weixin.qq.com/connect/qrconnect"
    params = {
        "appid": settings.WECHAT_WEB_APPID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "snsapi_login",
        "state": state
    }
    
    param_str = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{url}?{param_str}#wechat_redirect"


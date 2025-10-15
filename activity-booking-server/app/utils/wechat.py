import httpx
from typing import Optional
from app.config import settings


async def get_wechat_openid(code: str) -> Optional[str]:
    """获取微信openid"""
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


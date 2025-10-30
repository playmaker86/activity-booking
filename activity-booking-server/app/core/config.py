from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "活动预约系统"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # 数据库配置
    DATABASE_URL: str
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    
    # 微信网页应用配置
    WECHAT_WEB_APPID: str = ""
    WECHAT_WEB_SECRET: str = ""
    
    class Config:
        # 项目根目录的 .env 文件路径（app/core/config.py → 项目根目录上两级）
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()


settings = get_settings()

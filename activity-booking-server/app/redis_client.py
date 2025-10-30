from typing import Optional

import redis

from app.core.config import settings

# Redis连接池
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=10
)


def get_redis() -> redis.Redis:
    """获取Redis客户端"""
    return redis.Redis(connection_pool=redis_pool)


class RedisCache:
    """Redis缓存工具类"""
    
    def __init__(self):
        self.client = get_redis()
    
    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        return self.client.get(key)
    
    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """设置缓存"""
        return self.client.setex(key, expire, value)
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        return self.client.delete(key) > 0
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return self.client.exists(key) > 0


cache = RedisCache()


from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar('T')

class ResponseCode(int, Enum):
    """业务状态码枚举"""
    SUCCESS = 200  # 成功
    CREATED = 201  # 创建成功
    BAD_REQUEST = 400  # 请求参数错误
    UNAUTHORIZED = 401  # 未授权
    FORBIDDEN = 403  # 禁止访问
    NOT_FOUND = 404  # 资源不存在
    CONFLICT = 409  # 冲突（如重复创建）
    INTERNAL_ERROR = 500  # 服务器内部错误
    SERVICE_UNAVAILABLE = 503  # 服务不可用

class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: ResponseCode = Field(..., description="业务状态码")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="错误信息")
    timestamp: int = Field(..., description="响应时间戳")
    
    @classmethod
    def success(
        cls, 
        data: T = None, 
        message: str = "操作成功",
        code: ResponseCode = ResponseCode.SUCCESS
    ) -> "ApiResponse[T]":
        """成功响应"""
        import time
        return cls(
            code=code,
            message=message,
            data=data,
            error=None,
            timestamp=int(time.time())
        )
    
    @classmethod
    def error(
        cls,
        code: ResponseCode,
        message: str,
        error: str = None,
        data: T = None
    ) -> "ApiResponse[T]":
        """错误响应"""
        import time
        return cls(
            code=code,
            message=message,
            data=data,
            error=error,
            timestamp=int(time.time())
        )
    
    @classmethod
    def bad_request(
        cls,
        message: str = "请求参数错误",
        error: str = None
    ) -> "ApiResponse[None]":
        """400 错误响应"""
        return cls.error(
            code=ResponseCode.BAD_REQUEST,
            message=message,
            error=error
        )
    
    @classmethod
    def unauthorized(
        cls,
        message: str = "未授权访问",
        error: str = None
    ) -> "ApiResponse[None]":
        """401 错误响应"""
        return cls.error(
            code=ResponseCode.UNAUTHORIZED,
            message=message,
            error=error
        )
    
    @classmethod
    def forbidden(
        cls,
        message: str = "禁止访问",
        error: str = None
    ) -> "ApiResponse[None]":
        """403 错误响应"""
        return cls.error(
            code=ResponseCode.FORBIDDEN,
            message=message,
            error=error
        )
    
    @classmethod
    def not_found(
        cls,
        message: str = "资源不存在",
        error: str = None
    ) -> "ApiResponse[None]":
        """404 错误响应"""
        return cls.error(
            code=ResponseCode.NOT_FOUND,
            message=message,
            error=error
        )
    
    @classmethod
    def conflict(
        cls,
        message: str = "资源冲突",
        error: str = None
    ) -> "ApiResponse[None]":
        """409 错误响应"""
        return cls.error(
            code=ResponseCode.CONFLICT,
            message=message,
            error=error
        )
    
    @classmethod
    def internal_error(
        cls,
        message: str = "服务器内部错误",
        error: str = None
    ) -> "ApiResponse[None]":
        """500 错误响应"""
        return cls.error(
            code=ResponseCode.INTERNAL_ERROR,
            message=message,
            error=error
        )

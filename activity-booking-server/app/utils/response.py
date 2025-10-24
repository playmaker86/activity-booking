from typing import Any, Optional
from fastapi import HTTPException
from app.schemas.response import ApiResponse, ResponseCode

def create_success_response(
    data: Any = None,
    message: str = "操作成功",
    code: ResponseCode = ResponseCode.SUCCESS
) -> ApiResponse[Any]:
    """创建成功响应"""
    return ApiResponse.success(data=data, message=message, code=code)

def create_error_response(
    code: ResponseCode,
    message: str,
    error: Optional[str] = None
) -> ApiResponse[None]:
    """创建错误响应"""
    return ApiResponse.error(code=code, message=message, error=error)

def raise_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[dict] = None
):
    """抛出 HTTP 异常"""
    raise HTTPException(status_code=status_code, detail=detail, headers=headers)

def handle_service_error(error: Exception) -> ApiResponse[None]:
    """处理服务层错误"""
    if isinstance(error, ValueError):
        return ApiResponse.bad_request(
            message=str(error),
            error="参数验证失败"
        )
    elif isinstance(error, PermissionError):
        return ApiResponse.forbidden(
            message=str(error),
            error="权限不足"
        )
    elif isinstance(error, FileNotFoundError):
        return ApiResponse.not_found(
            message=str(error),
            error="资源不存在"
        )
    else:
        return ApiResponse.internal_error(
            message="服务器内部错误",
            error=str(error)
        )

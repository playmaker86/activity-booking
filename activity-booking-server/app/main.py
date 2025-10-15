import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api import auth, users, activities, bookings

# 创建应用实例
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    # 使用 ORJSONResponse 提高性能，并确保正确序列化
    default_response_class=ORJSONResponse,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 静态文件服务
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["认证"])
app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["用户"])
app.include_router(activities.router, prefix=f"{settings.API_PREFIX}/activities", tags=["活动"])
app.include_router(bookings.router, prefix=f"{settings.API_PREFIX}/bookings", tags=["预约"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用活动预约系统API",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


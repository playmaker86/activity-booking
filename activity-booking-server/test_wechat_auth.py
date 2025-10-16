#!/usr/bin/env python3
"""
微信授权登录功能测试脚本
"""
import asyncio
import httpx
from app.utils.wechat import (
    get_wechat_openid,
    get_wechat_access_token,
    get_wechat_user_info,
    get_wechat_web_login_url
)


async def test_wechat_functions():
    """测试微信相关函数"""
    print("🧪 开始测试微信授权登录功能...")
    
    # 测试获取扫码登录URL
    print("\n1. 测试生成微信扫码登录URL")
    try:
        redirect_uri = "http://localhost:3000/auth/callback"
        auth_url = get_wechat_web_login_url(redirect_uri, "test_state")
        print(f"✅ 授权URL生成成功: {auth_url[:100]}...")
    except Exception as e:
        print(f"❌ 授权URL生成失败: {e}")
    
    # 测试API接口连通性
    print("\n2. 测试API接口连通性")
    try:
        async with httpx.AsyncClient() as client:
            # 测试获取授权URL接口
            response = await client.get(
                "http://localhost:8000/api/auth/wx-web-login-url",
                params={"redirect_uri": "http://localhost:3000/auth/callback"}
            )
            if response.status_code == 200:
                print("✅ 获取授权URL接口正常")
                data = response.json()
                print(f"   返回数据: {data}")
            else:
                print(f"❌ 获取授权URL接口异常: {response.status_code}")
                
    except Exception as e:
        print(f"❌ API接口测试失败: {e}")
    
    print("\n🎉 微信授权登录功能测试完成")


async def test_user_model():
    """测试用户模型"""
    print("\n3. 测试用户模型")
    try:
        from app.models.user import User
        from app.schemas.user import UserCreate, WechatUserInfo
        
        # 测试用户创建模型
        user_create = UserCreate(
            openid="test_openid_123",
            unionid="test_unionid_123",
            nickname="测试用户",
            avatar="https://example.com/avatar.jpg",
            gender=1,
            country="中国",
            province="广东省",
            city="深圳市"
        )
        print("✅ 用户创建模型正常")
        
        # 测试微信用户信息模型
        wechat_info = WechatUserInfo(
            openid="test_openid_123",
            unionid="test_unionid_123",
            nickname="测试用户",
            avatar="https://example.com/avatar.jpg",
            gender=1
        )
        print("✅ 微信用户信息模型正常")
        
    except Exception as e:
        print(f"❌ 用户模型测试失败: {e}")


async def main():
    """主函数"""
    print("=" * 50)
    print("微信授权登录功能测试")
    print("=" * 50)
    
    await test_wechat_functions()
    await test_user_model()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

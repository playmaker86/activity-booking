# 微信授权登录功能使用指南

## 功能概述

本系统已成功集成微信授权登录功能，支持以下两种登录方式：

1. **微信小程序授权登录** - 适用于微信小程序环境
2. **微信扫码登录** - 适用于web端，用户使用微信扫描二维码登录

## 系统架构

### 后端API接口

#### 1. 小程序登录接口
```
POST /api/auth/wx-login
Content-Type: application/json

{
  "code": "微信登录码"
}
```

#### 2. Web端扫码登录接口
```
POST /api/auth/wx-web-login
Content-Type: application/json

{
  "code": "授权码",
  "state": "状态参数"
}
```

#### 3. 获取扫码登录URL接口
```
GET /api/auth/wx-web-login-url?redirect_uri=回调地址
```

### 数据库结构更新

用户表新增字段：
- `unionid` - 微信unionid
- `gender` - 性别
- `country` - 国家
- `province` - 省份
- `city` - 城市
- `language` - 语言
- `is_active` - 是否激活

## 配置说明

### 1. 环境变量配置

在 `.env` 文件中添加：

```bash
# 微信小程序配置
WECHAT_APPID=your-wechat-miniapp-appid
WECHAT_SECRET=your-wechat-miniapp-secret

# 微信网页应用配置
WECHAT_WEB_APPID=your-wechat-web-appid
WECHAT_WEB_SECRET=your-wechat-web-secret
```

### 2. 微信应用配置

#### 小程序配置
1. 在微信公众平台注册小程序
2. 获取AppID和AppSecret
3. 配置服务器域名白名单

#### 网页应用配置
1. 在微信开放平台注册网站应用
2. 获取AppID和AppSecret
3. 配置授权回调域名

## 使用方法

### 小程序端使用

1. **页面跳转**
   ```javascript
   // 跳转到登录页面
   uni.navigateTo({
     url: '/pages/login/login'
   })
   ```

2. **登录逻辑**
   ```javascript
   // 在登录页面点击微信授权登录
   const { login } = useUser()
   const success = await login()
   ```

3. **用户授权**
   - 系统会自动调用 `uni.getUserProfile()` 获取用户授权
   - 调用 `uni.login()` 获取登录码
   - 发送请求到后端完成登录

### Web端使用

1. **显示扫码登录页面**
   ```javascript
   // 跳转到扫码登录页面
   window.location.href = '/pages/web-login/web-login'
   ```

2. **扫码登录流程**
   - 页面自动生成微信授权二维码
   - 用户使用微信扫描二维码
   - 在微信中确认登录
   - 系统处理回调并完成登录

## 页面结构

### 新增页面

1. **登录页面** (`/pages/login/login`)
   - 微信授权登录按钮
   - 隐私政策和用户协议

2. **扫码登录页面** (`/pages/web-login/web-login`)
   - 二维码显示
   - 登录状态提示
   - 刷新和取消按钮

3. **回调处理页面** (`/pages/auth/callback`)
   - 处理微信授权回调
   - 显示登录结果

## 数据库迁移

运行数据库迁移脚本：

```bash
cd activity-booking-server
python scripts/db/migrations/add_wechat_fields.py upgrade
```

## 测试

运行测试脚本验证功能：

```bash
cd activity-booking-server
python test_wechat_auth.py
```

## 安全考虑

1. **CSRF防护** - 使用state参数防止跨站请求伪造
2. **Token安全** - JWT token存储在安全位置
3. **用户隐私** - 只获取必要的用户信息
4. **错误处理** - 完善的错误处理和用户提示

## 常见问题

### Q: 用户拒绝授权怎么办？
A: 系统会显示提示信息，引导用户重新授权。

### Q: 扫码后没有反应？
A: 检查回调域名配置和网络连接，确保微信应用配置正确。

### Q: 登录后用户信息不完整？
A: 系统会逐步完善用户信息，首次登录可能只有基础信息。

## 技术支持

如有问题，请检查：
1. 微信应用配置是否正确
2. 域名白名单是否配置
3. 网络连接是否正常
4. 环境变量是否正确设置

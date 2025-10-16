# 微信授权登录配置说明

## 环境变量配置

需要在 `.env` 文件中添加以下微信相关配置：

```bash
# 微信小程序配置
WECHAT_APPID=your-wechat-miniapp-appid
WECHAT_SECRET=your-wechat-miniapp-secret

# 微信网页应用配置（用于web端扫码登录）
WECHAT_WEB_APPID=your-wechat-web-appid
WECHAT_WEB_SECRET=your-wechat-web-secret
```

## 微信应用配置

### 1. 微信小程序配置

1. 在微信公众平台注册小程序
2. 获取小程序的 AppID 和 AppSecret
3. 配置服务器域名白名单

### 2. 微信网页应用配置

1. 在微信开放平台注册网站应用
2. 获取网页应用的 AppID 和 AppSecret
3. 配置授权回调域名

## API接口说明

### 小程序登录
- **接口**: `POST /api/auth/wx-login`
- **参数**: `{ "code": "微信登录码" }`
- **说明**: 适用于微信小程序环境

### Web端扫码登录
- **接口**: `POST /api/auth/wx-web-login`
- **参数**: `{ "code": "授权码", "state": "状态参数" }`
- **说明**: 适用于web端微信扫码登录

### 获取扫码URL
- **接口**: `GET /api/auth/wx-web-login-url`
- **参数**: `redirect_uri` (回调地址)
- **说明**: 获取微信授权登录二维码URL

## 数据库迁移

运行以下命令更新数据库结构：

```bash
python scripts/db/migrations/add_wechat_fields.py upgrade
```

## 使用说明

### 小程序端
1. 用户点击"微信授权登录"按钮
2. 调用 `uni.getUserProfile()` 获取用户授权
3. 调用 `uni.login()` 获取登录码
4. 发送登录请求到后端

### Web端
1. 显示微信扫码登录页面
2. 生成授权二维码
3. 用户扫码后在微信中确认
4. 微信回调到指定地址
5. 处理回调并完成登录

## 注意事项

1. 确保微信应用的域名配置正确
2. 注意处理用户拒绝授权的情况
3. 实现合适的错误处理和重试机制
4. 考虑token过期和刷新逻辑

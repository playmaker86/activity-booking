# 图标使用指南

## 已集成的图标库

项目已集成 **uni-icons** 图标组件，这是 uni-app 官方推荐的图标库。

## 使用方法

### 基本使用

```vue
<template>
  <uni-icons type="search" size="20" color="#999"></uni-icons>
</template>
```

### 属性说明

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| type | String | - | 图标类型（必填） |
| size | Number | 24 | 图标大小（rpx） |
| color | String | #333 | 图标颜色 |

## 常用图标类型

### 基础图标
- `search` - 搜索
- `home` - 首页
- `star` - 星标
- `heart` - 喜欢
- `more` - 更多
- `settings` - 设置

### 箭头图标
- `arrowright` - 右箭头
- `arrowleft` - 左箭头
- `arrowup` - 上箭头
- `arrowdown` - 下箭头
- `back` - 返回

### 操作图标
- `checkmarkempty` - 空勾选框
- `checkbox` - 勾选框
- `close` - 关闭
- `plus` - 加号
- `minus` - 减号
- `refreshempty` - 刷新

### 内容图标
- `calendar` - 日历
- `location` - 定位
- `email` - 邮件
- `phone` - 电话
- `person` - 用户
- `personadd` - 添加用户
- `image` - 图片
- `camera` - 相机

### 提示图标
- `info` - 信息
- `help` - 帮助
- `circle` - 圆圈
- `chatboxes` - 对话框

## 项目中的使用示例

### 1. 搜索框图标

```vue
<view class="search-box">
  <uni-icons type="search" size="20" color="#999"></uni-icons>
  <input class="search-input" type="text" placeholder="搜索活动" />
</view>
```

### 2. 列表项图标

```vue
<view class="meta-item">
  <uni-icons type="calendar" size="14" color="#999"></uni-icons>
  <text>2024-10-14 10:00</text>
</view>

<view class="meta-item">
  <uni-icons type="location" size="14" color="#999"></uni-icons>
  <text>北京市朝阳区</text>
</view>
```

### 3. 菜单项图标

```vue
<view class="menu-item">
  <view class="menu-left">
    <uni-icons type="calendar" size="20" color="#666"></uni-icons>
    <text>我的预约</text>
  </view>
  <uni-icons type="arrowright" size="16" color="#999"></uni-icons>
</view>
```

## 更多图标

完整图标列表请访问：
- uni-icons 官方文档：https://uniapp.dcloud.net.cn/component/uniui/uni-icons.html
- 在线预览：https://hellouniapp.dcloud.net.cn/pages/extUI/icons/icons

## 其他推荐图标库

如果 uni-icons 不能满足需求，还可以使用：

1. **iconfont（阿里巴巴矢量图标库）**
   - 网址：https://www.iconfont.cn/
   - 可以下载SVG或生成字体文件

2. **Iconify**
   - 网址：https://iconify.design/
   - 支持200,000+开源图标
   - 可以导出SVG使用

3. **Flaticon**
   - 网址：https://www.flaticon.com/
   - 大量免费图标资源

## TabBar 图标设置

### 问题说明

当前 tabBar 配置中引用的图标文件不存在，导致显示为破损状态。

### 解决方案

#### 方案1：使用现成的图标资源（推荐）

1. **从以下网站下载图标：**
   - [Icons8](https://icons8.com/icons) - 免费图标
   - [Flaticon](https://www.flaticon.com/) - 免费图标
   - [Iconify](https://iconify.design/) - 开源图标

2. **图标要求：**
   - 格式：PNG
   - 尺寸：建议 48x48 像素
   - 颜色：灰色（未选中）和绿色（选中）

#### 方案2：使用在线图标生成器

1. 访问 [Canva](https://www.canva.com/) 或 [Figma](https://www.figma.com/)
2. 创建 48x48 像素的画布
3. 设计简单的首页和用户图标
4. 导出为 PNG 格式

#### 方案3：使用 AI 生成图标

1. 使用 ChatGPT、Midjourney 等 AI 工具
2. 提示词示例：
   - "Simple home icon, 48x48 pixels, gray color, minimal style"
   - "Simple user profile icon, 48x48 pixels, gray color, minimal style"

### 当前配置

```json
{
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "iconPath": "static/tabbar/home.png",        // 需要创建
        "selectedIconPath": "static/tabbar/home-active.png", // 需要创建
        "text": "首页"
      },
      {
        "pagePath": "pages/my/my", 
        "iconPath": "static/tabbar/user.png",        // 需要创建
        "selectedIconPath": "static/tabbar/user-active.png", // 需要创建
        "text": "我的"
      }
    ]
  }
}
```

### 快速解决方案

#### 临时方案：使用文字图标

修改 `pages.json` 中的 tabBar 配置，暂时移除图标：

```json
{
  "tabBar": {
    "color": "#7A7E83",
    "selectedColor": "#3cc51f", 
    "borderStyle": "black",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页"
      },
      {
        "pagePath": "pages/my/my",
        "text": "我的"
      }
    ]
  }
}
```

#### 永久方案：添加图标文件

1. 下载或创建以下 4 个图标文件：
   - `static/tabbar/home.png` - 首页图标（灰色）
   - `static/tabbar/home-active.png` - 首页选中图标（绿色）
   - `static/tabbar/user.png` - 用户图标（灰色）
   - `static/tabbar/user-active.png` - 用户选中图标（绿色）

2. 将文件放入 `src/static/tabbar/` 目录

### 推荐图标样式

#### 首页图标
- 简单的房子形状
- 线条风格或填充风格
- 颜色：灰色 (#7A7E83) / 绿色 (#3cc51f)

#### 用户图标  
- 简单的人形轮廓
- 圆形头像 + 身体轮廓
- 颜色：灰色 (#7A7E83) / 绿色 (#3cc51f)

### 注意事项

1. 图标文件必须放在 `src/static/tabbar/` 目录下
2. 文件名必须与 `pages.json` 中的配置完全一致
3. 建议使用 PNG 格式，支持透明背景
4. 图标尺寸建议为 48x48 像素

## 自定义图标

如果需要使用自定义图标，可以：

1. 将 SVG 文件放到 `src/assets/images/icons/` 目录
2. 使用 `<image>` 标签引用

```vue
<image src="@/assets/images/icons/custom-icon.svg" class="icon" />
```


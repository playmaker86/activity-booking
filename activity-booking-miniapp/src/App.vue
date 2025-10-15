<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

// 应用启动
onLaunch(() => {
  console.log('App Launch')
  // 初始化应用配置
  initApp()
})

// 应用显示
onShow(() => {
  console.log('App Show')
})

// 应用隐藏
onHide(() => {
  console.log('App Hide')
})

// 初始化应用
function initApp() {
  // 设置状态栏样式（只在支持的平台调用）
  // #ifdef MP-WEIXIN || APP-PLUS
  uni.setNavigationBarColor({
    frontColor: '#000000',
    backgroundColor: '#ffffff'
  })
  // #endif
  
  // 检查更新
  checkUpdate()
}

// 检查小程序更新
function checkUpdate() {
  // #ifdef MP-WEIXIN
  if (uni.canIUse('getUpdateManager')) {
    const updateManager = uni.getUpdateManager()
    
    updateManager.onCheckForUpdate((res) => {
      if (res.hasUpdate) {
        console.log('发现新版本')
      }
    })
    
    updateManager.onUpdateReady(() => {
      uni.showModal({
        title: '更新提示',
        content: '新版本已经准备好，是否重启应用？',
        success: (res) => {
          if (res.confirm) {
            updateManager.applyUpdate()
          }
        }
      })
    })
  }
  // #endif
}
</script>

<style lang="scss">
// 导入全局样式
@use '@/styles/global.scss';

// 全局样式重置
page {
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

// 通用类
.flex {
  display: flex;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.text-center {
  text-align: center;
}

.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>


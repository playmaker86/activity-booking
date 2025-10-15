# 组件目录

这里存放可复用的 Vue 组件。

## 组件开发规范

1. 组件命名使用 PascalCase，如 `ActivityCard.vue`
2. 组件文件名与组件名保持一致
3. 每个组件应该职责单一，便于维护和复用
4. 组件应该有清晰的 props 定义和类型说明
5. 使用组合式 API（Composition API）编写组件

## 示例组件结构

```vue
<template>
  <view class="component-name">
    <!-- 组件内容 -->
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props 定义
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

// Emits 定义
const emit = defineEmits(['click'])

// 组件逻辑
</script>

<style lang="scss" scoped>
.component-name {
  /* 样式 */
}
</style>
```


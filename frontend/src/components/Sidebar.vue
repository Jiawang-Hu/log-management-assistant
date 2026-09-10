<script setup>
import { FileText, Database, ChevronDown } from '@lucide/vue'
</script>

<template>
  <aside class="sidebar">
    <div class="brand"><span class="brand-mark">⌘</span><strong>AI 日志管理</strong></div>
    <nav>
      <RouterLink to="/logs"><FileText :size="21" />服务日志</RouterLink>
      <RouterLink to="/services"><Database :size="21" />服务管理</RouterLink>
    </nav>
    <div class="profile">
      <span class="avatar">M</span>
      <span><b>管理员</b><small>admin@example.com</small></span>
      <ChevronDown :size="15" />
    </div>
  </aside>
</template>

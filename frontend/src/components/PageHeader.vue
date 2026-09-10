<script setup>
import { Plus } from '@lucide/vue'
defineProps({ title: String, subtitle: String, addButton: { type: Boolean, default: true } })
defineEmits(['add'])
</script>

<template>
  <header class="page-header">
    <div><h1>{{ title }}</h1><p v-if="subtitle">{{ subtitle }}</p></div>
    <div class="header-actions">
      <slot />
      <button v-if="addButton" class="primary-button" @click="$emit('add')"><Plus :size="19" />添加服务</button>
    </div>
  </header>
</template>

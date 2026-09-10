<script setup>
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="app-shell">
    <Sidebar />
    <main class="main-content"><RouterView /></main>
  </div>
</template>

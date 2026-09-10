<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { AlertCircle, AlertTriangle, CircleDot, Download, Info, Search } from '@lucide/vue'
import DatePicker from '../components/DatePicker.vue'
import PageHeader from '../components/PageHeader.vue'
import { api } from '../api'
import { demoLogs } from '../demo'

const router = useRouter(), route = useRoute()
const activeLevel = ref('ALL')
function todayText() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}
const selectedDate = ref(todayText())
const keyword = ref('')
const logs = ref(demoLogs)
const summary = ref({ error_count: 12, warn_count: 4, error_delta: -3, warn_delta: -2 })
const loading = ref(false)
const offline = ref(false)
let timer

function trendText(delta) {
  if (delta > 0) return `↑ 上升 ${delta} 条`
  if (delta < 0) return `↓ 下降 ${Math.abs(delta)} 条`
  return '持平 0 条'
}

const visibleLogs = computed(() => logs.value.filter(log => {
  const levelOk = activeLevel.value === 'ALL' || log.level === activeLevel.value
  const q = keyword.value.trim().toLowerCase()
  return levelOk && (!q || `${log.message} ${log.trace_id} ${log.service}`.toLowerCase().includes(q))
}))

async function load() {
  loading.value = true
  try {
    const [logData, stats] = await Promise.all([
      api.logs({ date: selectedDate.value, level: activeLevel.value === 'ALL' ? '' : activeLevel.value, keyword: keyword.value, service_id: route.query.service_id || '', limit: 500 }),
      api.summary(selectedDate.value)
    ])
    logs.value = logData.items
    summary.value = stats
    offline.value = false
  } catch (_) {
    offline.value = true
  } finally { loading.value = false }
}

function download() {
  window.location.href = api.downloadUrl({ date: selectedDate.value, level: activeLevel.value === 'ALL' ? '' : activeLevel.value, keyword: keyword.value, service_id: route.query.service_id || '' })
}

watch([selectedDate, activeLevel], load)
let debounce
watch(keyword, () => { clearTimeout(debounce); debounce = setTimeout(load, 350) })
onMounted(() => { load(); timer = setInterval(() => activeLevel.value === 'ALL' && load(), 8000) })
onBeforeUnmount(() => { clearInterval(timer); clearTimeout(debounce) })
</script>

<template>
  <section>
    <PageHeader title="服务日志" @add="router.push('/services/new')" />
    <div class="page-body log-page">
      <div class="stat-row compact-stats">
        <article class="stat-card error-stat">
          <span class="stat-icon"><AlertCircle :size="35" /></span>
          <div><b>错误日志数量</b><strong>{{ summary.error_count }}</strong><small>较昨日 <em :class="summary.error_delta > 0 ? 'up' : summary.error_delta < 0 ? 'down' : 'flat'">{{ trendText(summary.error_delta) }}</em></small></div>
        </article>
        <article class="stat-card warn-stat">
          <span class="stat-icon"><AlertTriangle :size="35" /></span>
          <div><b>警告日志数量</b><strong>{{ summary.warn_count }}</strong><small>较昨日 <em :class="summary.warn_delta > 0 ? 'up' : summary.warn_delta < 0 ? 'down' : 'flat'">{{ trendText(summary.warn_delta) }}</em></small></div>
        </article>
      </div>

      <div class="log-toolbar">
        <div class="tabs">
          <button :class="{active:activeLevel==='ALL'}" @click="activeLevel='ALL'"><CircleDot :size="16" />实时日志</button>
          <button :class="{active:activeLevel==='ERROR'}" @click="activeLevel='ERROR'"><Info :size="16" />错误日志</button>
          <button :class="{active:activeLevel==='WARN'}" @click="activeLevel='WARN'"><AlertTriangle :size="15" />警告日志</button>
        </div>
        <DatePicker v-model="selectedDate" />
        <label class="search-control"><Search :size="18" /><input v-model="keyword" placeholder="搜索日志内容、traceId、服务名称..." /></label>
        <button class="outline-button download-button" @click="download"><Download :size="17" />下载日志</button>
      </div>

      <div class="log-console" :class="{loading}">
        <div v-if="!visibleLogs.length" class="empty-state">暂无符合条件的日志</div>
        <div v-for="log in visibleLogs" :key="`${log.timestamp}-${log.trace_id}`" class="log-line">
          <span>{{ log.timestamp }}</span><b :class="`level-${log.level.toLowerCase()}`">{{ log.level }}</b><span>[{{ log.service }}]</span><span class="log-message">{{ log.message }}</span><span class="trace">traceId={{ log.trace_id }}</span>
        </div>
      </div>
      <p v-if="offline" class="offline-note">演示数据 · 启动后端后将自动显示真实日志</p>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { AlertTriangle, Boxes, Cloud, Database, Eye, PauseCircle, Pencil, PlayCircle, Search, Trash2 } from '@lucide/vue'
import PageHeader from '../components/PageHeader.vue'
import { api } from '../api'
import { demoServices } from '../demo'

const router = useRouter()
const services = ref(demoServices)
const keyword = ref('')
const status = ref('')
const enabled = ref('')
const offline = ref(false)

const filtered = computed(() => services.value.filter(s =>
  (!keyword.value || s.service_name.toLowerCase().includes(keyword.value.toLowerCase())) &&
  (!status.value || s.status === status.value) &&
  (enabled.value === '' || String(s.enabled) === enabled.value)
))
const counts = computed(() => ({ total: services.value.length, collecting: services.value.filter(s=>s.status==='collecting').length, error: services.value.filter(s=>s.status==='error').length, disabled: services.value.filter(s=>!s.enabled).length }))

async function load() {
  try { services.value = (await api.services()).items; offline.value = false } catch (_) { offline.value = true }
}
async function toggle(item) {
  if (offline.value) { item.enabled = !item.enabled; item.status = item.enabled ? 'collecting' : 'disabled'; return }
  await api.toggleService(item.id); await load()
}
async function remove(item) {
  if (!confirm(`确认删除“${item.service_name}”吗？相关统计和读取位置也会删除。`)) return
  if (offline.value) services.value = services.value.filter(s=>s.id!==item.id)
  else { await api.removeService(item.id); await load() }
}
function viewLogs(item) { router.push({ path:'/logs', query:{ service_id:item.id } }) }
function formatDate(value) { return value ? value.replace('T', ' ').split('.')[0] : '-' }
onMounted(load)
</script>

<template>
  <section>
    <PageHeader title="服务管理" subtitle="管理和配置已接入的服务，支持查看服务日志、运行状态等信息。" @add="router.push('/services/new')" />
    <div class="page-body services-page">
      <div class="stat-row service-stats">
        <article class="mini-stat"><span class="blue"><Boxes /></span><div><small>全部服务</small><b>{{ counts.total }}</b></div></article>
        <article class="mini-stat"><span class="green"><PlayCircle /></span><div><small>采集中</small><b>{{ counts.collecting }}</b></div></article>
        <article class="mini-stat"><span class="orange"><AlertTriangle /></span><div><small>读取异常</small><b>{{ counts.error }}</b></div></article>
        <article class="mini-stat"><span class="slate"><PauseCircle /></span><div><small>停用</small><b>{{ counts.disabled }}</b></div></article>
      </div>

      <div class="table-card">
        <div class="table-filters">
          <label class="search-control service-search"><Search :size="18" /><input v-model="keyword" placeholder="搜索服务名称..." /></label>
          <label class="select-control"><b>采集状态:</b><select v-model="status"><option value="">全部</option><option value="collecting">采集中</option><option value="error">读取异常</option><option value="disabled">停用</option></select></label>
          <label class="select-control"><b>已启用:</b><select v-model="enabled"><option value="">全部</option><option value="true">是</option><option value="false">否</option></select></label>
        </div>
        <div class="service-table-wrap">
          <table class="service-table">
            <thead><tr><th>服务名称</th><th>日志路径</th><th>采集状态</th><th>上次读取日志</th><th>操作</th></tr></thead>
            <tbody>
              <tr v-for="item in filtered" :key="item.id">
                <td><div class="service-name"><span :class="item.source_type"><Cloud v-if="item.source_type==='cloud'"/><Boxes v-else-if="item.source_type==='k8s'"/><Database v-else /></span><p><b>{{ item.service_name }}</b></p></div></td>
                <td>{{ item.log_path }}</td>
                <td><span class="status-pill" :class="item.status"><i></i>{{ item.status==='collecting'?'采集中':item.status==='error'?'读取异常':'停用' }}</span></td>
                <td>{{ formatDate(item.last_read_at) }}</td>
                <td><div class="row-actions"><button @click="viewLogs(item)"><Eye/>查看日志</button><button @click="router.push(`/services/${item.id}/edit`)"><Pencil/>修改</button><button class="danger" @click="remove(item)"><Trash2/>删除</button><button @click="toggle(item)"><PauseCircle v-if="item.enabled"/><PlayCircle v-else/>{{ item.enabled?'停用':'启用' }}</button></div></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="pagination"><span>共 {{ filtered.length }} 条</span><div><button>‹</button><button class="current">1</button><button>›</button><select><option>10 条/页</option></select></div></div>
      </div>
      <p v-if="offline" class="offline-note">演示数据 · 启动后端后可进行持久化管理</p>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ClipboardPen, Folder, Info, LayoutGrid } from '@lucide/vue'
import { api } from '../api'

const route = useRoute(), router = useRouter()
const editing = computed(() => Boolean(route.params.id))
const loading = ref(false), saving = ref(false), error = ref('')
const form = reactive({ service_name:'', log_path:'', enabled:true, source_type:'app' })
onMounted(async () => {
  if (!editing.value) return
  loading.value = true
  try { Object.assign(form, await api.service(route.params.id)) }
  catch (e) { error.value = e.message }
  finally { loading.value = false }
})
async function save() {
  error.value = ''
  if (!form.service_name.trim() || !form.log_path.trim()) { error.value='请填写服务名称和日志路径'; return }
  saving.value = true
  const payload = { ...form }
  try {
    if (editing.value) await api.updateService(route.params.id, payload); else await api.createService(payload)
    router.push('/services')
  } catch (e) { error.value = e.message }
  finally { saving.value = false }
}
</script>

<template>
  <section class="form-page">
    <header class="form-header"><div><p>服务管理　/　{{ editing ? '修改服务' : '增加服务' }}</p><h1>{{ editing ? '修改服务' : '增加服务' }}</h1><span>{{ editing ? '修改服务的配置信息，用于更新日志采集和展示的相关设置' : '填写服务的配置信息，用于配置日志采集和展示的相关设置' }}</span></div><div class="form-actions"><button class="outline-button cancel-button" type="button" :disabled="saving" @click="router.push('/services')">取消</button><button class="primary-button save-button" :disabled="loading || saving" @click="save">{{ loading?'加载中...':saving?'保存中...':'保存' }}</button></div></header>
    <div class="form-content">
      <article class="form-card">
        <div class="section-title"><span><ClipboardPen/></span><div><h2>基本信息</h2><p>设置服务的基本信息，用于识别和管理</p></div></div>
        <label class="field"><b><i>*</i> 服务名称</b><div class="input-count"><input v-model="form.service_name" maxlength="50" placeholder="请输入服务名称"/><span>{{ form.service_name.length }}/50</span></div></label>
      </article>
      <article class="form-card">
        <div class="section-title"><span><LayoutGrid/></span><div><h2>日志路径配置</h2><p>设置日志所在的本地路径</p></div></div>
        <label class="field"><b><i>*</i> 日志路径</b><div class="path-input"><input v-model="form.log_path" placeholder="/var/log/app/"/><button><Folder/></button></div><small>示例：/var/log/app/</small></label>
        <div class="info-banner"><Info/>日志文件规则已固定：今日日志为 *.log，历史日志为 *.log.gz，无需额外配置。</div>
      </article>
      <p v-if="error" class="form-error">{{ error }}</p>
    </div>
  </section>
</template>

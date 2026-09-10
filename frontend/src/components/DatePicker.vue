<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { CalendarDays, ChevronLeft, ChevronRight, Info, X } from '@lucide/vue'

const props = defineProps({ modelValue: { type: String, required: true } })
const emit = defineEmits(['update:modelValue'])
const open = ref(false)
const root = ref(null)

function atMidnight(value = new Date()) {
  const date = new Date(value)
  date.setHours(0, 0, 0, 0)
  return date
}
function addDays(value, amount) {
  const date = new Date(value)
  date.setDate(date.getDate() + amount)
  return date
}
function format(value) {
  const year = value.getFullYear()
  const month = String(value.getMonth() + 1).padStart(2, '0')
  const day = String(value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
function parse(value) {
  const [year, month, day] = value.split('-').map(Number)
  return new Date(year, month - 1, day)
}

const maximum = atMidnight()
const minimum = addDays(maximum, -7)
const viewDate = ref(parse(props.modelValue))
const weekdays = ['日', '一', '二', '三', '四', '五', '六']
const title = computed(() => `${viewDate.value.getFullYear()} 年 ${viewDate.value.getMonth() + 1} 月`)
const rangeText = `${format(minimum)} - ${format(maximum)}`

const days = computed(() => {
  const year = viewDate.value.getFullYear()
  const month = viewDate.value.getMonth()
  const first = new Date(year, month, 1)
  const start = addDays(first, -first.getDay())
  return Array.from({ length: 42 }, (_, index) => {
    const date = addDays(start, index)
    return {
      key: format(date),
      label: date.getDate(),
      outside: date.getMonth() !== month,
      disabled: date < minimum || date > maximum,
      selected: format(date) === props.modelValue,
      today: format(date) === format(maximum)
    }
  })
})

const canPrevious = computed(() => new Date(viewDate.value.getFullYear(), viewDate.value.getMonth(), 0) >= minimum)
const canNext = computed(() => new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + 1, 1) <= maximum)

function toggle() {
  open.value = !open.value
  if (open.value) viewDate.value = parse(props.modelValue)
}
function choose(day) {
  if (day.disabled) return
  emit('update:modelValue', day.key)
  open.value = false
}
function changeMonth(amount) {
  if ((amount < 0 && !canPrevious.value) || (amount > 0 && !canNext.value)) return
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + amount, 1)
}
function resetToday(event) {
  event.stopPropagation()
  emit('update:modelValue', format(maximum))
  open.value = false
}
function closeOutside(event) {
  if (root.value && !root.value.contains(event.target)) open.value = false
}

watch(() => props.modelValue, value => { if (!open.value) viewDate.value = parse(value) })
nextTick(() => document.addEventListener('pointerdown', closeOutside))
onBeforeUnmount(() => document.removeEventListener('pointerdown', closeOutside))
</script>

<template>
  <div ref="root" class="date-picker">
    <button class="date-control" type="button" :aria-expanded="open" @click="toggle">
      <CalendarDays :size="18" />
      <span>{{ modelValue }}</span>
      <X :size="17" aria-label="回到今天" @click="resetToday" />
    </button>
    <div v-if="open" class="calendar-popover">
      <div class="calendar-header">
        <button type="button" :disabled="!canPrevious" @click="changeMonth(-1)"><ChevronLeft /></button>
        <b>{{ title }}</b>
        <button type="button" :disabled="!canNext" @click="changeMonth(1)"><ChevronRight /></button>
      </div>
      <div class="calendar-grid weekdays"><span v-for="day in weekdays" :key="day">{{ day }}</span></div>
      <div class="calendar-grid calendar-days">
        <button v-for="day in days" :key="day.key" type="button" :disabled="day.disabled" :class="{ outside: day.outside, selected: day.selected, today: day.today }" @click="choose(day)">{{ day.label }}</button>
      </div>
      <div class="calendar-tip"><Info :size="17" /><span><b>可选择最近 7 天的日期</b><small>{{ rangeText }}</small></span></div>
    </div>
  </div>
</template>

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import LogView from './views/LogView.vue'
import ServicesView from './views/ServicesView.vue'
import ServiceForm from './views/ServiceForm.vue'
import './styles.css'
import './overrides.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/logs' },
    { path: '/logs', component: LogView },
    { path: '/services', component: ServicesView },
    { path: '/services/new', component: ServiceForm },
    { path: '/services/:id/edit', component: ServiceForm }
  ]
})

createApp(App).use(router).mount('#app')

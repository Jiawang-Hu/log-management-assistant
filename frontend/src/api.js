const API_ROOT = import.meta.env.VITE_API_ROOT || '/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_ROOT}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options
  })
  if (!response.ok) {
    let message = `请求失败 (${response.status})`
    try { message = (await response.json()).detail || message } catch (_) {}
    throw new Error(message)
  }
  if (response.status === 204) return null
  return response.json()
}
export const api = {
  logs: (params) => request(`/logs?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null))}`),
  summary: (date) => request(`/statistics/summary?date=${date}`),
  services: (params = {}) => request(`/services?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null))}`),
  service: (id) => request(`/services/${id}`),
  createService: (data) => request('/services', { method: 'POST', body: JSON.stringify(data) }),
  updateService: (id, data) => request(`/services/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  removeService: (id) => request(`/services/${id}`, { method: 'DELETE' }),
  toggleService: (id) => request(`/services/${id}/toggle`, { method: 'PATCH' }),
  downloadUrl: (params) => `${API_ROOT}/logs/download?${new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null))}`
}

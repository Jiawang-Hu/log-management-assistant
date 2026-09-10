export const demoLogs = [
  ['16:42:31','ERROR','user-service','用户登录失败，userId: 10086，ip: 10.1.2.3','8d4f2c3c9a7b4e1f9c3d9e0a8b6f7c3e'],
  ['16:42:28','WARN','order-service','订单创建失败，orderId: 202409120001，isPaid: false','6a7b3c9d8e2f4d6b1c3ff9e0a8b2c8d1'],
  ['16:42:26','INFO','user-service','用户注册失败，userId: 10087','d4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4'],
  ['16:42:23','INFO','payment-service','支付失败，orderId: 202409120001，amount: 199.00','7c6d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3'],
  ['16:42:17','ERROR','gateway','请求超时，目标服务：order-service','9e8f7d6b5c4aa3e2f1d0c9b8a7f6e5d4c3'],
  ['16:42:13','WARN','user-service','用户身份校验丢失，userId: 10086','a8b1c2a3e4f5a6b7c8d9e0f1a2b3c4d5'],
  ['16:42:07','INFO','system','系统启动完成，耗时：2.45s','3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9'],
  ['16:42:03','ERROR','order-service','订单状态更新失败，orderId: 202609070001','1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7'],
  ['16:41:58','INFO','user-service','获取用户信息失败，userId: 10087','2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8'],
  ['16:41:52','WARN','payment-service','金额不足，userId: 10086，amount: 500.00','d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1'],
  ['16:41:46','INFO','order-service','订单取消成功，orderId: 202609070002','4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0'],
  ['16:41:39','ERROR','gateway','连接超时，服务：payment-service','9f8e7d6c5b4a3e2f1d0c9b8a7f6e5d4c3']
].map((x, i) => ({ id: i + 1, timestamp: `2026/09/07 ${x[0]}`, level: x[1], service: x[2], message: x[3], trace_id: x[4], raw: '' }))

export const demoServices = [
  { id:1, service_name:'生产环境应用日志', log_path:'/var/log/app/*.log', status:'collecting', enabled:true, last_read_at:'2024-05-20 14:32:21', source_type:'app' },
  { id:2, service_name:'Kubernetes 集群日志', log_path:'/var/log/containers/*.log', status:'collecting', enabled:true, last_read_at:'2024-05-20 14:32:18', source_type:'k8s' },
  { id:3, service_name:'阿里云 SLS', log_path:'/project/logs/app', status:'error', enabled:true, last_read_at:'2024-05-20 14:28:09', source_type:'cloud' },
  { id:4, service_name:'测试环境日志', log_path:'/var/log/test/*.log', status:'disabled', enabled:false, last_read_at:null, source_type:'test' }
]

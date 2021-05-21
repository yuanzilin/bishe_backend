broker_url = 'redis://localhost:6379/8' # Broker配置，使用Redis作为消息中间件
result_backend = 'redis://localhost:6379/8' # BACKEND配置，这里使用redis
result_serializer = 'json' # 结果序列化方案
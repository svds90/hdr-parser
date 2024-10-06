from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType

# Создаем KafkaAdminClient, указывая адрес брокера
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")

# Указываем ресурс конфигурации для брокера (id брокера = 1)
broker_config = ConfigResource(ConfigResourceType.BROKER, "1")

# Получаем конфигурацию брокера
configs = admin_client.describe_configs([broker_config])

topics = admin_client.list_topics()
print(topics)

topics_info = admin_client.describe_topics(
    topics=["main_topic"]
)
for topic_info in topics_info:
    print(topic_info)

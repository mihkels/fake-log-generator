from kafka import KafkaConsumer


consumer = KafkaConsumer('demo_php_log', bootstrap_servers='sandbox.hortonworks.com:6667')
for msg in consumer:
    print(msg)
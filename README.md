# Pipeline

Start the containers

- **Postgres** 
Postgres is the source which is periodically populates with `pg_write.py`
- **Debezium**
The debezium connector produces a change event for every row-level insert, update, and delete operation that was captured and sends change event records for each table in a separate Kafka topic
- **Kafka + Zookeeper**
Connector pushed CDC changes here and kafka is maintained by zookeeeper cause its distributed (not in the latest versions tho)
- **Flink**
For real time aggregations on the kafka stream and push it to a sink

Flink is running on http://localhost:8081/

Pushing the aggregates data back to a sink kafka topic and maybe consume it with Druid ?


```bash
docker-compose -f docker-compose.yaml up
```

Start Postgres connector

```bash
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-postgres.json
```

Start consuming messages from a Debezium topic and listen to the transactions in the kafka topic

```bash
docker-compose exec kafka bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver1.public.test
python kafka_listen.py
```

Create a new topic
```bash
docker-compose exec kafka bin/kafka-topics.sh --create --topic sink --bootstrap-server kafka:9092
```

Keep inserting Record into the database

```bash
python pg_write.py
```

Submit Flink Job

```bash
docker-compose exec jobmanager ./bin/flink run -py /opt/pg-kafka-flink-druid/generate_aggregates.py -d
```


Shut this shit down

```bash
docker-compose -f docker-compose.yaml down
```


- https://noti.st/morsapaes/liQzgs/change-data-capture-with-flink-sql-and-debezium
# Kafka-Python guide

## Kafka key concepts

### Partitions

Kafka distributes messages across multiple partitions of a topic to improve performance and scalability. Each partition is an ordered, constantly-growing log.

### Replication

Partition replication ensures that if a partition fails, replicas of the partition exist on other brokers, which increases availability and fault tolerance.

### Offset

Kafka uses an offset to track messages within each partition. Consumers read messages starting from a specific offset. Offsets are unique per partition.

### Consumer Groups

Kafka allows multiple consumers to read from the same topic in parallel, with each consumer reading from a different partition. This is done via consumer groups.

### Stateless Producers and Consumers

Kafka is designed to be stateless for both producers and consumers. The producer does not know what other producers are publishing, and the consumer does not know in advance what other consumers are reading messages.

## Kafka setup and installation

### Step 1: Download kafka

- Visit the [official kafka website](https://kafka.apache.org/downloads) and download the latest version of Kafka.
- Extract the downloaded file to your preferred directory. 

### Step 2: Start zookeeper

Kafka depends on Zookeeper for managing the cluster and coordinating partitions. You must start Zookeeper before running Kafka.

`sh kafka_2.13-3.9.0/bin/zookeeper-server-start.sh kafka_2.3-3.9.0/config/zookeeper.properties`

This command will start the Zookeeper server with the default configuration.

### Step 3: Start kafka server

Once Zookeeper is up and running, you can start the Kafka server.

`sh kafka_2.13-3.9.0/bin/kafka-server-start.sh kafka_2.13-3.9.0/config/server.properties`

Kafka is now running and ready to accept producers and consumers.

### Step 4: Create a topic

To work with Kafka, you need to create a topic where producers will publish messages.

`sh kafka_2.13-3.9.0/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic neowstopic --partitions 1 --replication-factor 1`

- --bootstrap-server: Specifies the Kafka server.
- --create: Creates the topic.
- --topic: The name of the topic you are creating.
- --partitions: Number of partitions for the topic.
- --replication-factor: Replication factor for the topic. A value of 1 means no replicas.

### Step 5: List Topics

To list the topics you’ve created:
`sh kafka_2.13-3.9.0/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list`

## Useful Kafka Commands

### Describe a Topic

To describe the details of a topic, such as partitions, leader, and replicas:

`sh kafka_2.13-3.9.0/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic neowstopic`

### View Topic Logs

To read the logs of a topic from the beginning:

`sh kafka_2.13-3.9.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic neowstopic --from-beginning`

### Produce Messages from Console

If you want to send messages manually from the console to a topic:

`sh kafka_2.13-3.9.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic neowstopic`

This command allows you to type messages into the console and send them to neowstopic.

### Consume Messages from Console

To consume messages from the console:

`sh kafka_2.13-3.9.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic neowstopic --from-beginning`

### Delete a Topic

If you need to delete a topic:

`sh kafka_2.13-3.9.0/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic neowstopic`

## Producing and Consuming Messages with Kafka-Python

Now that your Kafka cluster is up and running, and the topic is created, you can start interacting with Kafka using Python. Here's how:

### Installing kafka-python

If you don't have the kafka-python library installed, you can install it with pip:

`pip install kafka-python`

### Create a Producer

A producer is responsible for sending messages to Kafka topics. Here's a basic Python producer example:

```from kafka import KafkaProducer
import json

Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializes the message to JSON
)

Send a message to the 'neowstopic' topic
producer.send('neowstopic', {'key': 'value'})
producer.flush()  # Ensure all messages are sent
producer.close()  # Close the producer
```

### Create a Consumer

A consumer reads messages from Kafka topics. Here's a basic Python consumer example:

```from kafka import KafkaConsumer
import json

# Create a Kafka consumer
consumer = KafkaConsumer(
    'neowstopic',
    bootstrap_servers='localhost:9092',
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserializes the message from JSON
)

# Read messages from the topic
for message in consumer:
    print(f"Message received: {message.value}")
```
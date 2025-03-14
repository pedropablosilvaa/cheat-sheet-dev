# How to install kafka using Docker

This guide is based in [official documentation](https://docs.confluent.io/platform/current/installation/docker/config-reference.html) of confluent platform.

## Docker image configuration

It is possible to specify configuration values in Docker image using environment variables wuith ```-e``` or ```--env``` variables.

### Kafka standars

Confluent has three differents images to deploy kafka using Docker:

- ```cp-kafka```: Includes kafka.
- ```cp-server```: Includes RBAC, self-balancing clusters, and other features in addition to kafka it self (licenced).
- ```confluent-local```: Includes kafka and Confluent Rest Proxy. Default to running KRaft mode.

It is necessary to use the following rules and use them as Docker environment variables.

- Use ```KAFKA_``` as a prefix to component properties. For example, ```metric.reporters``` sould be converted to ```KAFKA_METRIC_REPORTERS```.
- Use ```CONFLUENT_``` prefix for ```cp-server```. For example, ```confluent.metrics.reporter.bootstrap.servers``` sould be converted to ```CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS```.
- Convert to upper-case.
- Replace a dot (```.```) with a single underscore (```_```)
- Replace a underscore (```_```) with a double underscore (```__```)
- Replace a dash (```-```) with a triple underscore (```___```)

Just to remember: 

- A ***Kafka broker*** is a fundamental unit of kafka cluster, they store and serve data, receiving message from producers and delivering them to consumers. Each broker manage a set of patitions. Brokcer also are resposible for handling the storage and retrieval of data within their assigned partitions. Brokers can be physical or containerized servers.

- ***Kafka controller*** es un broker que es elegito para manegar la metadata del cluster y ejecutar tareas administrativas. Sus principales tareas son manage the states of partitions an replicas, the electer partition leaders when broker leave or join the cluster, perform administrative task like reassigning partitions, monitor broker health and handling failures and comunnicate with KRaftt and others brokers.

In KRaft mode, a kafka node can act as either brokers, controllers, or both, with controllers managing metadata and leader elections, and brokers handling message storage and retrieval, replacing ZooKeeper's role. Also in KRaft, a group of controllers (controllers quorum) replicates the metadata log, ensuring high availability and fault tolerance.

In development is recommended to use combined mode (broker and controllers on the same node) for testing and development, but in production environment the isolate mode is recommended.

### Configuration for KRaft mode

- ```KAFKA_PROCESS_ROLES```: The role of the server (```controller```, ```broker``` or ```broker, controller```).
- ```KAFKA_NODE_ID```: The unique idenfigier of the server.
- ```KAFKA_CONTROLLER_QUORUM_VOTERS```: List separated by commas of quorum voters. Each controlller is identified using their id, host and port information in the format {id}@{host}:{port}
- ```KAFKA_CONTROLLER_LISTENER_NAMES```: List separated by commas of the listeners used by each controller. On a node with ```process.roles=broker```, only the first listener in the list will be used by broker. If you are using **ZooKeeper-mode, brokers should not set this value**. For KRaft controllers in isolated or combined mode, the node will listen as a KRaft controller on all listener that are listed for this property, an each one must appear in the ```listeners``` property.
- Each KRaft cluster must hace a unique cluster ID assigned to its CLUSTER_ID variable or ```KAFKA_CLUSTER_ID```. ```kafka-storage``` is a tool of kafka that allow to generate a unque ID.

### Kafka in KRaft mode configuration

In a production environment, there should be a minimum of three brokers and three controllers.

Go to Kafka properties file for KRaft in ```/etc/kafka/kraft``` and customize it with the following:

- Configure ```process.roles``` to ```broker``` or ```controller```.
- Set a unique id for ```node.id``` for earch broker/controller.
- Set ```controller.quorum.voters``` with a comma-separated list of controllers.

Here a example from the official documentation:

```bash
############################# Server Basics #############################

# The role of this server. Setting this puts us in KRaft mode
process.roles=broker

# The node id associated with this instance's roles
node.id=2

# The connect string for the controller quorum
controller.quorum.voters=1@controller1:9093,3@controller3:9093,5@controller5:9093
```

Also configure how brokers and clients communicate with broker using ```listeners``` and where controllers listen with ```controller.listener.names```

- ```listeners```: Comma-separated list of URIs and listener names to listen on in the format ```listener_name://hostname:port```
- ```controller.listener.names```: Comma-separated list of ```listener_name``` entries for listeners used by the controller.

After create a random uuid as cluster id, you need to format a storage for each node in cluster with ```kafka-storage``` tool and the ```format``` command especifying the properties file for a controller.

```bash
bin/kafka-storage format -t <KAFKA_CLUSTER_ID> -c etc/kafka/kraft/controller.properties
```

Kafka previously auto-formatted empty storage directories and generated a new cluster ID automatically. However, this could hide errors—especially in the metadata log used by controllers and brokers. If most controllers started with an empty log directory, a leader might be elected without all the committed data. Now, you must explicitly set the log directory using either ```metadata.log.dir``` or ```log.dirs```.

#### Logs and partitions

Each Kafka partitions is a log file stored in the directory specified at ```log.dirs```. These settings determine the number of partitions ofr a topic and the log storage location.

```log.dirs```: The directories in which the kafka log data is located (High importance).
- Type: string
- Default: "tmp/kafka-logs"

```num.partitions``` Is the default number of log partitions for auto-created topics. It is recommended to increase this because is better over-partition a topic and this allow a better data balancing and consume parallelism (Avoid this if your are using keyed data). This is a medium importance setting.
- Type: int
- Default: 1
- Valid Values: Positive integers

### Example

This is an example to run a kafka with in a single node instance using docker. 

```bash
docker run -d \
--name=kafka-kraft \
-h kafka-kraft \
-p 9101:9101 \
-e KAFKA_NODE_ID=1 \
-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP='CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT' \
-e KAFKA_ADVERTISED_LISTENERS='PLAINTEXT://kafka-kraft:29092,PLAINTEXT_HOST://localhost:9092' \
-e KAFKA_JMX_PORT=9101 \
-e KAFKA_JMX_HOSTNAME=localhost \
-e KAFKA_PROCESS_ROLES='broker,controller' \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
-e KAFKA_CONTROLLER_QUORUM_VOTERS='1@kafka-kraft:29093' \
-e KAFKA_LISTENERS='PLAINTEXT://kafka-kraft:29092,CONTROLLER://kafka-kraft:29093,PLAINTEXT_HOST://0.0.0.0:9092' \
-e KAFKA_INTER_BROKER_LISTENER_NAME='PLAINTEXT' \
-e KAFKA_CONTROLLER_LISTENER_NAMES='CONTROLLER' \
-e CLUSTER_ID='MkU3OEVBNTcwNTJENDM2Qk' \
confluentinc/cp-kafka:7.9.0
```

Explanation environmental variables one by one:

- ```KAFKA_LISTENER_SECURITY_PROTOCOL_MAP='CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'```
  - This variable map each listener name to a seted security protocol. Clients and other brokers rely on these advertised addresses to know where to send and receive messages.
    - ```CONTROLLER:PLAINTEXT``` indicates that the controller communication will be unsecured (plaintext).
    - ```PLAINTEXT:PLAINTEXT``` is used for internal broker communication.
    - ```PLAINTEXT_HOST:PLAINTEXT``` is set for client connection.
- ```KAFKA_ADVERTISED_LISTENERS='PLAINTEXT://kafka-kraft:29092,PLAINTEXT_HOST://localhost:9092'```
  - Defines the network endpoint that Kafka advertises to clients and other brokers.
    - ```PLAINTEXT://kafka-kraft:29092``` is the address other brokers (or internal processes) use to reach this broker.
    - ```PLAINTEXT_HOST://localhost:9092``` is the endpoint that external clients (producers/consumeres) will use to connect
- ```KAFKA_PROCESS_ROLES='broker,controller'```
  - Tells Kafka that this process should perform both, the broker and controlers roles. This configuration doesn't should be used in production environment.
- ```KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1```
  - Sets the replication factor for internal offsets topic. A replication factor of 1 means that the offsets is not replicated, which is acceptable for testing cluster, but in production should be higher for fault tolerance purpose.
- ```KAFKA_CONTROLLER_QUORUM_VOTERS='1@kafka-kraft:29093'``` 
  - specifies which nodes are participating in metadata management using the Raft consensus algorithm.
    - ```<node_id>@<hostname>:<port>``` is the formate used. In this case, tells Kafka that node 1, reachable at kafka-kraft on port 29093, is a voter in the controller quorum.
- ```KAFKA_LISTENERS='PLAINTEXT://kafka-kraft:29092,CONTROLLER://kafka-kraft:29093,PLAINTEXT_HOST://0.0.0.0:9092'```
  - This define the actual endpoint on which Kafka will listen for incoming connections. This setting determines where Kafka accepts connections from both internal components and external clients. The ```0.0.0.0``` binding for ```PLAINTEXT_HOST``` means it's accessible on any network interface of the container.
    - ```PLAINTEXT://kafka-kraft:29092``` listens for internal broker-to-broker communication using the PLAINTEXT protocol.
    - ```CONTROLLER://kafka-kraft:29093``` listens for controller-specific tasks (like metadata management).
    - ```PLAINTEXT_HOST://0.0.0.0:9092``` listens on all network interfaces on port 9092 for external client connection.
- ```KAFKA_INTER_BROKER_LISTENER_NAME='PLAINTEXT'```
  - This specifies wich of the defined listeners should be used for communication between brokers. This ensure that when brokers talk to each others (for example, during replication or leader election), they use the PLAINTEXT listener configured at ```kafka-kraft:29092```.
- ```KAFKA_CONTROLLER_LISTENER_NAMES='CONTROLLER'```
  - Tells Kafka wich listener is reserver for controller communications. With this Kafka knows to use it for internal controller tasks, wich helps in maintaining a consistent cluster state.
  
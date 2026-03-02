# Apache Kafka Notes

## 1. Windows Setup (Docker)

### Setup Docker 
  1. Go to [Docker Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
  2. Download `Docker Desktop` and Install it
  3. Make sure that `Docker` is added to Window's `System Environment Variables Path`

### Setup Kafka
  1. Go to `C:\Docker` directory
  2. Create a directory named `kafka`
  3. Inside `kafka` directory create a file named `docker-compose.yml`
  4. Open file and add below YAML code <br><br>
      ``` yml
      version: '3.8'
      
      services:
        kafka:
          image: apache/kafka:4.2.0
          container_name: kafka-local
          ports:
            - "9092:9092"
          environment:
            # 1. Define the node and its KRaft roles (Combined mode)
            KAFKA_NODE_ID: 1
            KAFKA_PROCESS_ROLES: broker,controller
      
            # 2. Network and listener configuration
            KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
            KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      
            # 3. Tell the node how to vote in the KRaft quorum (it votes for itself)
            KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      
            # 4. Single-node cluster optimizations
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
            KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
            KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      
            # 5. Our custom 10MB message size limits
            KAFKA_MESSAGE_MAX_BYTES: 10485760
            KAFKA_REPLICA_FETCH_MAX_BYTES: 10485760 
      ```

  5. Save the file and Open `cmd` and cd to `C:\Docker\kafka`
  6. Execute the following command: `docker-compose up -d` (It will download and start the Kafka server)

## 2. Python (FastAPI) and Kafka Integration
  1. Run `pip install confluent-kafka` in cmd to install the Kafka Utility Package for Python
  1. Check `main.py` to setup the Kafka Producer
  2. Check `consumer.py` to setup the Kafka Consumer

## 3. Note
  1. Based on this setup Kafka runs on Port: `9092`
  2. We have updated the Kafka configuration to allow Maximum Message Bytes to 10 MB (`KAFKA_MESSAGE_MAX_BYTES: 10485760` and `KAFKA_REPLICA_FETCH_MAX_BYTES: 10485760`), So that Large size Image Base64 can be stored in the Queue.
  3. Gemini Reference: [Kafka & MinIO](https://gemini.google.com/share/45540eda06c7)
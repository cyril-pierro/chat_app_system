# Backend workflow

This part of the project consists of the following:

- Dependencies ( Contains other applications that support the back-end functionality)
- Docs (Code Documentation of the codebase)
- Services (Backend Services like API's, Websockets and Plugins to other Services)
- Streams (Kafka Stream Connectors and Ksql Stream queries)





### **GENERAL WORKFLOW**



![WORKFLOW](https://github.com/cyril-pierro/chat_app_system/blob/main/backend/resources/worfklow.jpg)





## **TECH STACKS**

![Tech Stack](https://github.com/cyril-pierro/chat_app_system/blob/main/backend/resources/resources.jpg)


## **Guidelines on how to start the application**

**NOTE** This project assumes you have docker already installed and have 12G storage space

- Navigate to the dependencies directory or folder and run the following command
  ```bash
     $ docker compose up 
  ```
  
- Navigate to the streams directory and perform the following
   - Send a post request to the kafka connect service using the sink connector json file
   
     ```bash
     $ curl --location 'http://localhost:9095/connectors/' --header 'Content-Type: application/json'
             --data '{
         "name": "elasticsearch-sink",
          "config": {
             "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
             "tasks.max": "1",
             "topics": "elasticsearch_users",
             "key.ignore": "true",
             "connection.url": "http://elasticsearch:9200",
             "type.name": "_doc",
             "value.converter": "org.apache.kafka.connect.json.JsonConverter",
             "value.converter.schemas.enable": "false",
        		"schema.ignore": "true"
      
        }
      }'
     
     
     ```
   
     
   
   - Send a post request to the kafka connect service using the source connector json file
   
     ```bash
     $  $ curl --location 'http://localhost:9095/connectors/' --header 'Content-Type: application/json' --data '{
     	 	"name": "postgres-source-connector",
     		"config": {						
     			"connector.class": "io.debezium.connector.postgresql.PostgresConnector",
             	"tasks.max": "1",
                 "database.hostname": "postgres",
                 "database.port": "5432",
                 "database.user": "admin",
                 "database.password": "admin",
                 "database.dbname": "chat_app_database",
                 "database.server.id": "184054",
                 "topic.prefix": "users_topic",
                 "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
                 "schema.history.internal.kafka.topic": "schema-changes.chat_app_database",
     			"value.converter": "io.apicurio.registry.utils.converter.AvroConverter",
      			"value.converter.apicurio.registry.url": "http://apicurio:8080/apis /registry/v2",
                 "value.converter.apicurio.registry.auto-register": true,
                 "value.converter.apicurio.registry.find-latest": true,
                 "value.converter.apicurio.registry.as-confluent": true,
                 "value.converter.apicurio.registry.use-id": "contentId",
                 "value.converter.apicurio.registry.headers.enabled": false
       }
     }'
     ```
     
     
     
     **Note** Before you send the post request using the sink connector make sure you have elasticsearch connector jar file downloaded
      You can copy the binaries of the jar file to kafka connect using this copy
     
      ```bash
          docker cp {elasticsearch connector jar lib folder} kafka_connect:/kafka/lib
      ```
   
- Enter into the ksqldb server using the following command
  ```bash
      docker compose exec -it ksql_server bash ksql
  ```

- Copy  the contents of the streams.sql file in the sql directory and paste it in the ksql

**NOTE** Make sure to check the logs of the dependencies services running if anything goes wrong using

```bash
    $ docker compose logs -f {service name}
```



For elastic search disk threshold Error, you can fix it with

```bash
$  curl -XPUT -H "Content-Type: application/json" http://localhost:6383/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
```


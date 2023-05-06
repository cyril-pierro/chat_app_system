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
   - Send a post request to the kafka connect service using the source connector json file
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

**NOTE** Make sure to check the logs of the dependencies if anything goes wrong using

```bash
    $ docker compose logs -f {service name}
```
  

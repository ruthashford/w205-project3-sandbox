# W205 Project 3


## Navigation
The key files for this project are described below: 

| File Name   | Description |
| ----------- | ----------- |
| [report.ipynb](report.ipynb)        | A python notebook containing a detailed description of the pipeline along with analysis of the data that is transported through the pipline       |
| [docker-compose.yml](docker-compose.yml)     | The docker compose file outlining the services needed to run this pipeline        |  
| [game_api.py](game_api.py)     | A flash application which decribes APIs for each event type and publishes received events to Kafka        |  
| [write_horse_events.py](write_horse_events.py)     | A python file that reads horse purchase events fromm Kafka and writes the to HDFS        |  
| [write_sword_events.py](write_sword_events.py)     | A python file that reads sword purchase events fromm Kafka and writes the to HDFS        |  
| [write_guild_events.py](write_guild_events.py)     | A python file that reads guild action events fromm Kafka and writes the to HDFS        |  
| [generate_data.sh](generate_data.sh)     | A script for generating sample data using Apache Bench        |  



**----I think we can remove below here----**
## Overview & Problem Statement

## Goals
With the tables we produce from this project, we want to be able to answer the following questions for the business:  
1. How many people are in the guild? 
2. How many people joined the guild over X time period? 
3. How many small, medium and large horses have been purchased? 
4. How many swords have been purchased by color?
5. How many swords were purchased over X time period? 
 
## Running the Project

Bring up docker
```
docker-compose up -d
```

Create the events topic
```
docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
```

Run the flask app
```
docker-compose exec mids env FLASK_APP=/w205/w205-project3-sandbox/game_api.py flask run --host 0.0.0.0
```

Use the [generate_data.sh file](https://github.com/ruthashford/w205-project3-sandbox/blob/main/generate_data.sh) to send standardized events in bulk via Apache Bench: 

```
sh generate_data.sh
```

*See below for preview of the generate_data.sh file:*
```
...
docker-compose exec mids ab -n 100 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/red/2
docker-compose exec mids ab -n 100 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_sword/red/3
docker-compose exec mids ab -n 500 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_sword/red/1
...
```

Check out the events in Kafka
```
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning
```

Submit the events to be written to HDFS

Each Python script filters and submits separated event tables to hdfs depending on the event type
```
docker-compose exec spark spark-submit /w205/w205-project3-sandbox/write_sword_events.py
docker-compose exec spark spark-submit /w205/w205-project3-sandbox/write_horse_events.py
docker-compose exec spark spark-submit /w205/w205-project3-sandbox/write_guild_events.py
```


Check out the files written to HDFS. Checkout each event table to verify the events landed successfully into hdfs.
```
docker-compose exec cloudera hadoop fs -ls /tmp/sword_purchases
docker-compose exec cloudera hadoop fs -ls /tmp/horse_purchases
docker-compose exec cloudera hadoop fs -ls /tmp/guild_actions
```

Bring up spark notebook (note that you need to have configured this first for your instance following the instructions from Shiraz):
```
docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 7000 --ip 0.0.0.0 --allow-root --notebook-dir=/w205/' pyspark
```
## Output 

![ERD Diagram](https://github.com/ruthashford/w205-project3-sandbox/blob/main/W205%20Project%203%20ERD.png)

### Example Queries 

Guild Stats - How many people are in the guild? 
```{sql}
WITH
  guild_headcount AS (
    SELECT
      CASE
        WHEN action = 'Join' THEN 1
        WHEN action = 'Leave' THEN - 1
        ELSE 0
      END AS guild_hc_change
    FROM event_guild )
    
SELECT
  SUM(guild_hc_change) AS guild_size
FROM guild_headcount; 
```

Guild Stats - How many people joined the guild in the past year? 
```{sql}
SELECT
  COUNT(*) AS num_guild_joins
FROM event_guild
WHERE
  action = 'Join'
  AND timestamp BETWEEN TIMESTAMP_SUB(timestamp, INTERVAL 365 DAY) AND CURRENT_TIMESTAMP();
```

Horse Stats - How many horses have been purchased by size? 
```{sql}
SELECT
  size AS horse_size,
  SUM(quantity) AS num_horses
FROM event_purchase_horse
GROUP BY 1;
```

Sword Stats - How many swords have been purchased by color? 
```{sql}
SELECT
  color AS sword_color,
  SUM(quantity) AS num_swords
FROM event_purchase_sword
GROUP BY 1;
```

Sword Stats - How many swords have been purchased in the past year? 
```{sql}
SELECT
  SUM(quantity) AS num_swords_purchased
FROM event_purchase_sword
WHERE
  timestamp BETWEEN TIMESTAMP_SUB(timestamp, INTERVAL 365 DAY) AND CURRENT_TIMESTAMP();
```

## Creating External Tables to Query in Presto
Presto is a query engine that is often used over spark because it scales well, can handle a variety of SQL syntaxes and can be easier to query than doing so in Spark. In order to make your tables available to query in Presto, you need to store your tables in the Hive metastore.

Open pyspark: 
```
docker-compose exec spark pyspark
```

Create external tables for each of the 3 events: 
```
df_sword = spark.read.parquet('/tmp/sword_purchases')
df_sword.registerTempTable(‘sword_purchases’)
sword_purchases_table = """
create external table swords_table
  stored as parquet
  location '/tmp/swords_table’
  as
  select * from sword_purchases
"""
spark.sql(sword_purchases_table)


df_horse = spark.read.parquet('/tmp/horse_purchases')
df_horse.registerTempTable(‘horse_purchases’)
horse_purchases_table = """
create external table horses_table
  stored as parquet
  location '/tmp/horses_table’
  as
  select * from horse_purchases
"""
spark.sql(horse_purchases_table)

df_guild = spark.read.parquet('/tmp/guild_actions’)
df_guild.registerTempTable(‘guild_actions’)
guild_action_table = """
create external table guild_table
  stored as parquet
  location '/tmp/guild_table’
  as
  select * from guild_actions
"""
spark.sql(guild_action_table)
```

Exit pyspark and open presto: 
```
exit()

docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
```

Check to see what tables are available in presto: 
```
presto:default> show tables;
```

You can run the example queries included above in presto, here is an example to show the syntax: 
```
presto:default> select * from sword_purchases_table;
```

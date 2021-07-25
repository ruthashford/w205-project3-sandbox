# W205 Project 3

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

Use Apache Bench to send some events in bulk:

First to the default endpoint
```
docker-compose exec mids ab -n 5 -H "Host: user1.comcast.com" http://localhost:5000/

```

Then to the purchase_sword endpoint
```
docker-compose exec mids ab -n 5 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/red/2
```

Then the horse and guild endpoints
```
docker-compose exec mids ab -n 10 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_horse/1/small/1
docker-compose exec mids ab -n 20 -m POST -H "Host: user1.comcast.com" http://localhost:5000/guild/join
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

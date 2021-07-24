# W205 Project 3

## Running the project

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
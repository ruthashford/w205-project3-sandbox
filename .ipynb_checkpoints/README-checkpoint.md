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
docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/

```

Then to the purchase_sword endpoint
```
docker-compose exec mids ab -n 10 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/red/2
```

Check out the events in Kafka
```
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning -e
```

Submit the events to be written to HDFS - note that this filters out and submits only the sword events

```
docker-compose exec spark spark-submit /w205/w205-project3-sandbox/write_sword_events.py
```

Check out the file written to HDFS - it should only contain the purchase sword events
```
docker-compose exec cloudera hadoop fs -ls /tmp/sword_purchases
```